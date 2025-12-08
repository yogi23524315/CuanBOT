# ML Forecasting dengan Prophet - Documentation

## 🎯 Overview

Forecasting service telah di-upgrade dari **Linear Regression** ke **Facebook Prophet** untuk prediksi yang lebih akurat dengan fitur:
- ✅ Seasonality detection (daily & weekly patterns)
- ✅ Trend analysis
- ✅ Confidence intervals (95%)
- ✅ Automatic handling of missing data
- ✅ Better accuracy for time series data

---

## 📊 Perbandingan: Before vs After

### **SEBELUM (Linear Regression)**
```python
model = LinearRegression()
model.fit(X, y)
predictions = model.predict(future_days)
```

**Kekurangan:**
- ❌ Tidak mendeteksi seasonality
- ❌ Tidak ada confidence interval
- ❌ Hanya trend linear sederhana
- ❌ Tidak cocok untuk time series

### **SESUDAH (Prophet)**
```python
model = Prophet(
    daily_seasonality=True,
    weekly_seasonality=True,
    interval_width=0.95
)
model.fit(df)
forecast = model.predict(future)
```

**Keunggulan:**
- ✅ Deteksi pola harian & mingguan
- ✅ Confidence interval 95%
- ✅ Trend yang lebih akurat
- ✅ Dirancang khusus untuk time series

---

## 🔧 Technical Implementation

### 1. Backend Service (`ml_forecasting.py`)

**Data Preparation:**
```python
def prepare_data(self, transactions):
    # Prophet requires columns: 'ds' (date) and 'y' (value)
    df = pd.DataFrame(transactions)
    df = df[df['transaction_type'] == 'income']
    df = df.groupby(date)['amount'].sum()
    df.columns = ['ds', 'y']  # Prophet format
    return df
```

**Model Training:**
```python
model = Prophet(
    daily_seasonality=True,      # Detect daily patterns
    weekly_seasonality=True,     # Detect weekly patterns
    yearly_seasonality=False,    # Not enough data
    changepoint_prior_scale=0.05,  # Trend flexibility
    seasonality_prior_scale=10.0,  # Seasonality strength
    interval_width=0.95          # 95% confidence
)
model.fit(df)
```

**Forecasting:**
```python
future = model.make_future_dataframe(periods=30, freq='D')
forecast = model.predict(future)

# Ensure non-negative predictions
forecast['yhat'] = forecast['yhat'].clip(lower=0)
forecast['yhat_lower'] = forecast['yhat_lower'].clip(lower=0)
forecast['yhat_upper'] = forecast['yhat_upper'].clip(lower=0)
```

### 2. API Response Structure

```json
{
  "status": "success",
  "model": "prophet",
  "actual": [
    {
      "date": "2025-11-01",
      "actual_amount": 250000,
      "type": "actual"
    }
  ],
  "forecast": [
    {
      "date": "2025-12-01",
      "predicted_amount": 280000,
      "lower_bound": 220000,
      "upper_bound": 340000,
      "type": "forecast"
    }
  ],
  "chart_data": [
    {
      "date": "2025-11-01",
      "actual": 250000,
      "predicted": null,
      "lower_bound": null,
      "upper_bound": null
    },
    {
      "date": "2025-12-01",
      "actual": null,
      "predicted": 280000,
      "lower_bound": 220000,
      "upper_bound": 340000
    }
  ],
  "metadata": {
    "training_samples": 30,
    "forecast_period_days": 30,
    "average_actual_revenue": 250000,
    "average_forecast_revenue": 280000,
    "trend": "increasing",
    "confidence_interval": "95%",
    "first_date": "2025-11-01",
    "last_actual_date": "2025-11-30",
    "last_forecast_date": "2025-12-30"
  }
}
```

### 3. Frontend Visualization (`ForecastChart.tsx`)

**Chart Components:**
```tsx
<ComposedChart data={chart_data}>
  {/* Confidence Interval - Shaded Area */}
  <Area
    dataKey="upper_bound"
    fill="url(#confidenceGradient)"
    fillOpacity={0.3}
  />
  <Area
    dataKey="lower_bound"
    fill="#fff"
  />
  
  {/* Actual Data - Green Solid Line */}
  <Line 
    dataKey="actual" 
    stroke="#10b981" 
    strokeWidth={3}
    dot={{ fill: '#10b981', r: 4 }}
  />
  
  {/* Predicted Data - Purple Dashed Line */}
  <Line 
    dataKey="predicted" 
    stroke="#8b5cf6" 
    strokeWidth={3}
    strokeDasharray="5 5"
    dot={{ fill: '#8b5cf6', r: 4 }}
  />
</ComposedChart>
```

---

## 📈 Chart Features

### Visual Elements:

1. **Actual Data Line** (Green, Solid)
   - Shows historical revenue
   - Solid line with dots
   - Color: `#10b981` (Emerald green)

2. **Predicted Data Line** (Purple, Dashed)
   - Shows future predictions
   - Dashed line with dots
   - Color: `#8b5cf6` (Purple)

3. **Confidence Interval** (Purple Shaded Area)
   - Shows uncertainty range
   - Upper and lower bounds
   - 95% confidence level
   - Gradient fill

4. **Metadata Cards**
   - Training Data: Number of days used
   - Avg Actual: Average historical revenue
   - Avg Forecast: Average predicted revenue
   - Trend: Direction (📈 Naik / 📉 Turun)

---

## 🎨 Color Scheme

| Element | Color | Hex | Purpose |
|---------|-------|-----|---------|
| Actual Line | Green | `#10b981` | Historical data |
| Predicted Line | Purple | `#8b5cf6` | Future forecast |
| Confidence Area | Light Purple | `#8b5cf6` (30% opacity) | Uncertainty range |
| Grid | Light Gray | `#e5e7eb` | Background grid |

---

## 🚀 Usage

### Generate Forecast via API:
```bash
curl -X POST http://localhost:8000/api/predictions/forecast \
  -H "Content-Type: application/json" \
  -d '{"periods": 30}'
```

### Frontend Usage:
```tsx
const result = await api.generateForecast({ periods: 30 })
setData(result.chart_data)
setMetadata(result.metadata)
```

---

## 📊 Example Output

**Scenario:** 30 days of historical data, forecasting next 30 days

**Input:**
- Historical revenue: Nov 1-30 (30 days)
- Forecast period: Dec 1-30 (30 days)

**Output:**
- `actual`: 30 data points (Nov 1-30)
- `forecast`: 30 predictions (Dec 1-30)
- `chart_data`: 60 combined points for visualization
- `metadata`: Statistics and trend analysis

**Interpretation:**
- If `trend = "increasing"`: Revenue expected to grow
- If `trend = "decreasing"`: Revenue expected to decline
- Confidence interval shows range of possible outcomes

---

## ⚠️ Requirements

### Minimum Data:
- **7 days** of historical data required
- More data = better accuracy
- Recommended: 30+ days for reliable forecasts

### Dependencies:
```txt
prophet==1.1.5
pandas==2.1.4
numpy==1.26.3
```

---

## 🔍 Troubleshooting

### Error: "Insufficient Data"
```json
{
  "status": "insufficient_data",
  "message": "Minimal 7 hari data diperlukan untuk forecasting"
}
```
**Solution:** Add more transaction data (minimum 7 days)

### Error: Prophet Fitting Failed
```json
{
  "status": "error",
  "message": "Error during forecasting: ..."
}
```
**Solution:** Check data quality, ensure dates are valid

---

## 📝 Best Practices

1. **Data Quality:**
   - Ensure consistent daily data
   - Remove outliers if necessary
   - Fill missing dates with 0 or interpolation

2. **Forecast Period:**
   - Short-term (7-30 days): More accurate
   - Long-term (30+ days): Less reliable
   - Recommended: 30 days forecast

3. **Model Tuning:**
   - Adjust `changepoint_prior_scale` for trend flexibility
   - Adjust `seasonality_prior_scale` for pattern strength
   - Use `interval_width` for confidence level

---

## 🎯 Future Improvements

- [ ] Add monthly/yearly seasonality (when enough data)
- [ ] Custom holidays for Indonesian calendar
- [ ] Multiple forecast scenarios (optimistic/pessimistic)
- [ ] Automatic outlier detection and removal
- [ ] Model performance metrics (MAPE, RMSE)
- [ ] Export forecast to CSV/PDF

---

## 📚 References

- [Prophet Documentation](https://facebook.github.io/prophet/)
- [Prophet Paper](https://peerj.com/preprints/3190/)
- [Time Series Forecasting Best Practices](https://facebook.github.io/prophet/docs/quick_start.html)
