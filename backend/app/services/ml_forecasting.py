import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')

class ForecastingService:
    def __init__(self):
        self.model = None
    
    def prepare_data(self, transactions: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Prepare transaction data for Prophet.
        Prophet requires columns: 'ds' (datestamp) and 'y' (value to forecast)
        """
        df = pd.DataFrame(transactions)
        if df.empty:
            return df
        
        # Filter only income transactions
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        df = df[df['transaction_type'] == 'income']
        
        # Group by date and sum amounts
        df = df.groupby(df['transaction_date'].dt.date)['amount'].sum().reset_index()
        df.columns = ['ds', 'y']  # Prophet requires these column names
        df['ds'] = pd.to_datetime(df['ds'])
        df = df.sort_values('ds')
        
        return df
    
    def forecast_revenue(self, transactions: List[Dict[str, Any]], periods: int = 30) -> Dict[str, Any]:
        """
        Forecast revenue using Facebook Prophet.
        Returns actual data + predictions for visualization.
        """
        df = self.prepare_data(transactions)
        
        if len(df) < 7:
            return {
                "status": "insufficient_data",
                "message": "Minimal 7 hari data diperlukan untuk forecasting",
                "actual": [],
                "forecast": [],
                "chart_data": []
            }
        
        try:
            # Initialize and train Prophet model
            model = Prophet(
                daily_seasonality=True,
                weekly_seasonality=True,
                yearly_seasonality=False,  # Not enough data for yearly patterns
                changepoint_prior_scale=0.05,  # Flexibility of trend changes
                seasonality_prior_scale=10.0,  # Strength of seasonality
                interval_width=0.95  # 95% confidence interval
            )
            
            model.fit(df)
            
            # Create future dataframe for predictions
            future = model.make_future_dataframe(periods=periods, freq='D')
            forecast = model.predict(future)
            
            # Ensure predictions are non-negative
            forecast['yhat'] = forecast['yhat'].clip(lower=0)
            forecast['yhat_lower'] = forecast['yhat_lower'].clip(lower=0)
            forecast['yhat_upper'] = forecast['yhat_upper'].clip(lower=0)
            
            # Separate actual and predicted data
            actual_data = []
            for _, row in df.iterrows():
                actual_data.append({
                    "date": row['ds'].strftime("%Y-%m-%d"),
                    "actual_amount": float(row['y']),
                    "type": "actual"
                })
            
            # Get only future predictions (after last actual date)
            last_actual_date = df['ds'].max()
            future_forecast = forecast[forecast['ds'] > last_actual_date]
            
            forecast_data = []
            for _, row in future_forecast.iterrows():
                forecast_data.append({
                    "date": row['ds'].strftime("%Y-%m-%d"),
                    "predicted_amount": float(row['yhat']),
                    "lower_bound": float(row['yhat_lower']),
                    "upper_bound": float(row['yhat_upper']),
                    "type": "forecast"
                })
            
            # Combine for chart visualization (actual + forecast)
            chart_data = []
            
            # Add actual data
            for item in actual_data:
                chart_data.append({
                    "date": item["date"],
                    "actual": item["actual_amount"],
                    "predicted": None,
                    "lower_bound": None,
                    "upper_bound": None
                })
            
            # Add forecast data
            for item in forecast_data:
                chart_data.append({
                    "date": item["date"],
                    "actual": None,
                    "predicted": item["predicted_amount"],
                    "lower_bound": item["lower_bound"],
                    "upper_bound": item["upper_bound"]
                })
            
            # Calculate statistics
            avg_actual = float(df['y'].mean())
            avg_forecast = float(future_forecast['yhat'].mean())
            trend = "increasing" if avg_forecast > avg_actual else "decreasing"
            
            return {
                "status": "success",
                "model": "prophet",
                "actual": actual_data,
                "forecast": forecast_data,
                "chart_data": chart_data,  # Combined data for easy charting
                "metadata": {
                    "training_samples": len(df),
                    "forecast_period_days": periods,
                    "average_actual_revenue": avg_actual,
                    "average_forecast_revenue": avg_forecast,
                    "trend": trend,
                    "confidence_interval": "95%",
                    "first_date": df['ds'].min().strftime("%Y-%m-%d"),
                    "last_actual_date": last_actual_date.strftime("%Y-%m-%d"),
                    "last_forecast_date": future_forecast['ds'].max().strftime("%Y-%m-%d")
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error during forecasting: {str(e)}",
                "actual": [],
                "forecast": [],
                "chart_data": []
            }

forecasting_service = ForecastingService()
