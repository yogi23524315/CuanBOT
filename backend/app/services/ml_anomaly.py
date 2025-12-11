import pandas as pd
import numpy as np
from typing import List, Dict, Any
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta
from collections import Counter
import pytz
import warnings
warnings.filterwarnings('ignore')

class AnomalyDetectionService:
    def __init__(self):
        # Isolation Forest with lower contamination for more precise detection
        self.model = IsolationForest(
            contamination=0.05,  # Expect 5% anomalies
            random_state=42,
            n_estimators=100,
            max_samples='auto'
        )
    
    def detect_anomalies(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Detect anomalies using Isolation Forest with comprehensive pattern analysis.
        
        Detects:
        - Duplicate transactions
        - Unusually large expenses
        - Transactions at odd hours (2 AM, etc)
        - Unusual categories
        - Frequent capital injections
        - Sudden salary spikes
        - Abnormal operational costs (gas, electricity, etc)
        """
        if len(transactions) < 10:
            return {
                "status": "insufficient_data",
                "message": "Minimal 10 transaksi diperlukan untuk deteksi anomali",
                "anomalies": [],
                "summary": {
                    "total_transactions": len(transactions),
                    "anomalies_detected": 0,
                    "anomaly_types": {}
                }
            }
        
        df = pd.DataFrame(transactions)
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        
        # Calculate statistics per category
        category_stats = df.groupby('category')['amount'].agg(['mean', 'std', 'count']).to_dict('index')
        
        # Analyze user's business patterns
        business_pattern = self._analyze_business_pattern(df)
        
        # Feature engineering for Isolation Forest
        features_list = []
        for idx, row in df.iterrows():
            # Convert to Jakarta timezone for consistent hour extraction
            jakarta_dt = self._convert_to_jakarta_timezone(row['transaction_date'])
            hour = jakarta_dt.hour
            day_of_week = jakarta_dt.weekday()
            
            # Get category statistics
            cat_stats = category_stats.get(row['category'], {'mean': 0, 'std': 1, 'count': 1})
            
            # Calculate hour deviation from user's normal pattern
            hour_deviation = self._calculate_hour_deviation(hour, business_pattern['hour_pattern'])
            
            features = [
                row['amount'],                          # Amount
                hour,                                   # Hour of day
                day_of_week,                           # Day of week
                1 if row['transaction_type'] == 'expense' else 0,  # Type
                row['amount'] / (cat_stats['mean'] + 1),  # Amount ratio to category mean
                cat_stats['count'],                    # Category frequency
                hour_deviation,                        # Hour deviation from normal pattern
            ]
            features_list.append(features)
        
        X = np.array(features_list)
        
        # Fit Isolation Forest
        predictions = self.model.fit_predict(X)
        scores = self.model.score_samples(X)
        
        df['is_anomaly'] = predictions
        df['anomaly_score'] = scores
        
        # Additional rule-based anomaly detection
        anomalies_detailed = []
        anomaly_types = {
            "duplicate": 0,
            "large_expense": 0,
            "odd_hours": 0,
            "unusual_category": 0,
            "frequent_capital": 0,
            "salary_spike": 0,
            "operational_spike": 0
        }
        
        # Detect duplicates
        duplicates = self._detect_duplicates(df)
        
        # Detect frequent capital injections
        frequent_capital = self._detect_frequent_capital(df)
        
        # Process anomalies
        anomalies = df[df['is_anomaly'] == -1].copy()
        
        for idx, row in df.iterrows():
            anomaly_reasons = []
            is_anomaly = row['is_anomaly'] == -1
            severity = "low"
            
            # Check duplicates
            if row['id'] in duplicates:
                anomaly_reasons.append({
                    "type": "duplicate",
                    "message": f"Duplikasi transaksi terdeteksi",
                    "severity": "high"
                })
                anomaly_types["duplicate"] += 1
                is_anomaly = True
                severity = "high"
            
            # Check odd hours - analyze user's transaction patterns first
            jakarta_dt = self._convert_to_jakarta_timezone(row['transaction_date'])
            hour = jakarta_dt.hour
            
            if self._is_unusual_hour(hour, business_pattern['hour_pattern']):
                common_hours = business_pattern['hour_pattern']['common_hours']
                business_type = business_pattern['business_type']
                
                # Customize message based on business type
                if business_type == "restaurant" and 22 <= hour <= 2:
                    # Restaurants might operate late, so be less strict
                    severity_level = "low"
                    message = f"Transaksi agak terlambat ({hour:02d}:00) - biasanya jam {common_hours}"
                elif business_type == "online" and 0 <= hour <= 6:
                    # Online businesses might have 24/7 transactions
                    severity_level = "low" 
                    message = f"Transaksi dini hari ({hour:02d}:00) - biasanya jam {common_hours}"
                else:
                    severity_level = "medium"
                    message = f"Transaksi pada jam tidak biasa ({hour:02d}:00) - biasanya jam {common_hours}"
                
                anomaly_reasons.append({
                    "type": "odd_hours",
                    "message": message,
                    "severity": severity_level
                })
                anomaly_types["odd_hours"] += 1
                is_anomaly = True
                if severity == "low":
                    severity = severity_level
            
            # Check large expenses
            if row['transaction_type'] == 'expense':
                cat_stats = category_stats.get(row['category'], {'mean': 0, 'std': 1})
                if cat_stats['mean'] > 0:
                    z_score = (row['amount'] - cat_stats['mean']) / (cat_stats['std'] + 1)
                    if z_score > 2.5:  # More than 2.5 standard deviations
                        normal_range = f"{int(cat_stats['mean'] - cat_stats['std']):,}–{int(cat_stats['mean'] + cat_stats['std']):,}"
                        anomaly_reasons.append({
                            "type": "large_expense",
                            "message": f"{row['category']} Rp {int(row['amount']):,} (biasanya {normal_range} ribu)",
                            "severity": "high"
                        })
                        anomaly_types["large_expense"] += 1
                        is_anomaly = True
                        severity = "high"
            
            # Check salary spikes
            if row['category'] and 'gaji' in row['category'].lower():
                cat_stats = category_stats.get(row['category'], {'mean': 0, 'std': 1})
                if cat_stats['mean'] > 0:
                    if row['amount'] > cat_stats['mean'] * 2:
                        anomaly_reasons.append({
                            "type": "salary_spike",
                            "message": f"Gaji crew Rp {int(row['amount']):,} (biasanya {int(cat_stats['mean']):,} ribu)",
                            "severity": "high"
                        })
                        anomaly_types["salary_spike"] += 1
                        is_anomaly = True
                        severity = "high"
            
            # Check operational spikes (gas, listrik, etc)
            operational_categories = ['gas', 'listrik', 'bensin', 'operasional']
            if row['category'] and any(cat in row['category'].lower() for cat in operational_categories):
                cat_stats = category_stats.get(row['category'], {'mean': 0, 'std': 1})
                if cat_stats['mean'] > 0:
                    if row['amount'] > cat_stats['mean'] * 2.5:
                        anomaly_reasons.append({
                            "type": "operational_spike",
                            "message": f"{row['category']} mendadak tinggi Rp {int(row['amount']):,} (biasanya {int(cat_stats['mean']):,})",
                            "severity": "medium"
                        })
                        anomaly_types["operational_spike"] += 1
                        is_anomaly = True
                        if severity == "low":
                            severity = "medium"
            
            # Check frequent capital injections
            if row['id'] in frequent_capital:
                anomaly_reasons.append({
                    "type": "frequent_capital",
                    "message": f"Setoran modal {frequent_capital[row['id']]} kali dalam {frequent_capital['days']} hari",
                    "severity": "medium"
                })
                anomaly_types["frequent_capital"] += 1
                is_anomaly = True
                if severity == "low":
                    severity = "medium"
            
            # Add to anomalies list if any reason found
            if is_anomaly and anomaly_reasons:
                anomalies_detailed.append({
                    "transaction_id": int(row.get('id', idx)),
                    "amount": float(row['amount']),
                    "transaction_type": row['transaction_type'],
                    "category": row.get('category', 'Unknown'),
                    "description": row.get('description', ''),
                    "date": self._format_date_indonesia(row['transaction_date']),
                    "anomaly_score": float(row['anomaly_score']),
                    "severity": severity,
                    "reasons": anomaly_reasons
                })
        
        # Sort by severity and anomaly score
        severity_order = {"high": 0, "medium": 1, "low": 2}
        anomalies_detailed.sort(key=lambda x: (severity_order[x['severity']], x['anomaly_score']))
        
        return {
            "status": "success",
            "model": "isolation_forest",
            "total_transactions": len(df),
            "anomalies_detected": len(anomalies_detailed),
            "anomalies": anomalies_detailed,
            "summary": {
                "total_transactions": len(df),
                "anomalies_detected": len(anomalies_detailed),
                "anomaly_types": anomaly_types,
                "high_severity": sum(1 for a in anomalies_detailed if a['severity'] == 'high'),
                "medium_severity": sum(1 for a in anomalies_detailed if a['severity'] == 'medium'),
                "low_severity": sum(1 for a in anomalies_detailed if a['severity'] == 'low')
            }
        }
    
    def _detect_duplicates(self, df: pd.DataFrame) -> List[int]:
        """Detect duplicate transactions (same amount, category, within 1 hour)"""
        duplicates = []
        df_sorted = df.sort_values('transaction_date')
        
        for i in range(len(df_sorted) - 1):
            current = df_sorted.iloc[i]
            next_row = df_sorted.iloc[i + 1]
            
            # Check if same amount and category within 1 hour
            if (current['amount'] == next_row['amount'] and 
                current['category'] == next_row['category'] and
                abs((next_row['transaction_date'] - current['transaction_date']).total_seconds()) < 3600):
                duplicates.extend([current['id'], next_row['id']])
        
        return list(set(duplicates))
    
    def _detect_frequent_capital(self, df: pd.DataFrame) -> Dict[int, int]:
        """Detect frequent capital injections (setoran modal)"""
        capital_transactions = df[
            (df['transaction_type'] == 'income') & 
            (df['category'].str.contains('modal|setoran', case=False, na=False))
        ].copy()
        
        if len(capital_transactions) < 2:
            return {}
        
        # Check for multiple capital injections within short period
        capital_transactions = capital_transactions.sort_values('transaction_date')
        frequent = {}
        
        for i in range(len(capital_transactions)):
            current_date = capital_transactions.iloc[i]['transaction_date']
            current_id = capital_transactions.iloc[i]['id']
            
            # Count capital injections within 3 days
            window_start = current_date - timedelta(days=3)
            window_end = current_date + timedelta(days=3)
            
            count = len(capital_transactions[
                (capital_transactions['transaction_date'] >= window_start) &
                (capital_transactions['transaction_date'] <= window_end)
            ])
            
            if count >= 3:  # 3 or more within 6 days
                frequent[current_id] = count
                frequent['days'] = 6
        
        return frequent
    
    def _analyze_user_hour_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze user's transaction hour patterns to determine what's normal for them
        """
        # Extract hours from all transactions (in Jakarta timezone)
        hours = []
        for _, row in df.iterrows():
            jakarta_dt = self._convert_to_jakarta_timezone(row['transaction_date'])
            hours.append(jakarta_dt.hour)
        
        if not hours:
            return {
                'common_hours': '08:00-18:00',
                'hour_distribution': {},
                'unusual_threshold': 0.05
            }
        
        # Count frequency of each hour
        hour_counts = Counter(hours)
        total_transactions = len(hours)
        
        # Calculate hour distribution percentages
        hour_distribution = {hour: count/total_transactions for hour, count in hour_counts.items()}
        
        # Find common hours (hours with >5% of transactions)
        common_hours = [hour for hour, pct in hour_distribution.items() if pct >= 0.05]
        common_hours.sort()
        
        # Format common hours for display
        if common_hours:
            if len(common_hours) <= 3:
                common_hours_str = ', '.join([f"{h:02d}:00" for h in common_hours])
            else:
                # Group consecutive hours
                ranges = []
                start = common_hours[0]
                end = start
                
                for i in range(1, len(common_hours)):
                    if common_hours[i] == end + 1:
                        end = common_hours[i]
                    else:
                        if start == end:
                            ranges.append(f"{start:02d}:00")
                        else:
                            ranges.append(f"{start:02d}:00-{end:02d}:00")
                        start = end = common_hours[i]
                
                # Add the last range
                if start == end:
                    ranges.append(f"{start:02d}:00")
                else:
                    ranges.append(f"{start:02d}:00-{end:02d}:00")
                
                common_hours_str = ', '.join(ranges)
        else:
            common_hours_str = '08:00-18:00'
        
        return {
            'common_hours': common_hours_str,
            'hour_distribution': hour_distribution,
            'unusual_threshold': 0.03,  # Less than 3% of transactions
            'common_hour_list': common_hours
        }
    
    def _is_unusual_hour(self, hour: int, hour_pattern: Dict[str, Any]) -> bool:
        """
        Determine if an hour is unusual based on user's historical patterns
        """
        hour_distribution = hour_pattern['hour_distribution']
        threshold = hour_pattern['unusual_threshold']
        
        # If we have no data for this hour, check if it's in typical business hours
        if hour not in hour_distribution:
            # Consider 2 AM - 6 AM as unusual only if:
            # 1. User has no history of transactions at these hours
            # 2. User has transactions during normal business hours
            # 3. User has sufficient transaction history (>20 transactions)
            if 2 <= hour <= 6:
                # Check if user has normal business hour transactions
                business_hours = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
                has_business_hours = any(h in hour_distribution for h in business_hours)
                total_transactions = sum(hour_distribution.values()) * len(hour_distribution)
                
                # Only flag as unusual if user has established business hours and sufficient data
                if has_business_hours and total_transactions > 20:
                    return True
            return False
        
        # If this hour has very few transactions compared to user's pattern
        hour_percentage = hour_distribution[hour]
        
        # If user consistently uses this hour (>2% of transactions), don't flag as unusual
        if hour_percentage >= 0.02:
            return False
            
        return hour_percentage < threshold
    
    def _analyze_business_pattern(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze business patterns to understand the type of business and normal operating hours
        """
        # Analyze categories to determine business type
        categories = df['category'].value_counts().to_dict()
        
        # Determine business type based on categories
        business_type = "general"
        if any(cat and ('makanan' in cat.lower() or 'menu' in cat.lower() or 'penjualan' in cat.lower()) for cat in categories.keys()):
            business_type = "restaurant"
        elif any(cat and ('toko' in cat.lower() or 'barang' in cat.lower() or 'stok' in cat.lower()) for cat in categories.keys()):
            business_type = "retail"
        elif any(cat and ('online' in cat.lower() or 'digital' in cat.lower()) for cat in categories.keys()):
            business_type = "online"
        
        # Get hour pattern
        hour_pattern = self._analyze_user_hour_patterns(df)
        
        return {
            'business_type': business_type,
            'hour_pattern': hour_pattern,
            'categories': categories
        }
    
    def _calculate_hour_deviation(self, hour: int, hour_pattern: Dict[str, Any]) -> float:
        """
        Calculate how much this hour deviates from the user's normal pattern
        """
        hour_distribution = hour_pattern['hour_distribution']
        
        if hour in hour_distribution:
            # Return the inverse of frequency (higher deviation for less frequent hours)
            return 1.0 - hour_distribution[hour]
        else:
            # Hour never used before
            return 1.0
    
    def _format_date_indonesia(self, dt) -> str:
        """
        Format datetime to Indonesia timezone and format
        """
        import pytz
        
        # If datetime is naive, assume it's UTC
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        
        # Convert to Jakarta timezone
        jakarta_tz = pytz.timezone('Asia/Jakarta')
        jakarta_dt = dt.astimezone(jakarta_tz)
        
        # Format as DD/MM/YYYY, HH.MM.SS
        return jakarta_dt.strftime("%d/%m/%Y, %H.%M.%S")
    
    def _convert_to_jakarta_timezone(self, dt):
        """
        Convert datetime to Jakarta timezone
        """
        # If datetime is naive, assume it's UTC
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        
        # Convert to Jakarta timezone
        jakarta_tz = pytz.timezone('Asia/Jakarta')
        return dt.astimezone(jakarta_tz)

anomaly_detection_service = AnomalyDetectionService()
