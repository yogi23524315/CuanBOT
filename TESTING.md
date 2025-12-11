# 🧪 CuanBot Testing Guide

Panduan lengkap untuk testing CuanBot.

## 📋 Table of Contents

1. [Manual Testing](#manual-testing)
2. [API Testing](#api-testing)
3. [Bot Testing](#bot-testing)
4. [Dashboard Testing](#dashboard-testing)
5. [ML Models Testing](#ml-models-testing)
6. [Integration Testing](#integration-testing)

## 🔧 Manual Testing

### Prerequisites

```bash
# Ensure all services are running
docker-compose ps

# Check health
./scripts/check_health.sh

# View logs
docker-compose logs -f
```

## 🤖 Bot Testing

### 1. Test Bot Commands

**Start Command:**
```
Input: /start
Expected: Welcome message dengan panduan lengkap
```

**Help Command:**
```
Input: /help
Expected: Panduan penggunaan bot
```

**Summary Command:**
```
Input: /summary
Expected: Ringkasan keuangan dengan AI insights
```

### 2. Test Transaction Recording

**Income Transactions:**
```
✅ Input: "Terima uang 500 ribu dari customer"
   Expected: Konfirmasi transaksi income 500000

✅ Input: "Dapat pembayaran 1.5 juta"
   Expected: Konfirmasi transaksi income 1500000

✅ Input: "Transfer masuk 750rb untuk produk X"
   Expected: Konfirmasi transaksi income 750000
```

**Expense Transactions:**
```
✅ Input: "Bayar listrik 300 ribu"
   Expected: Konfirmasi transaksi expense 300000

✅ Input: "Beli stok 2 juta"
   Expected: Konfirmasi transaksi expense 2000000

✅ Input: "Gaji karyawan 5 juta"
   Expected: Konfirmasi transaksi expense 5000000
```

**Receivable Transactions:**
```
✅ Input: "Piutang Toko A 1 juta"
   Expected: Konfirmasi transaksi receivable 1000000

✅ Input: "Customer B hutang 500rb"
   Expected: Konfirmasi transaksi receivable 500000
```

**Payable Transactions:**
```
✅ Input: "Hutang ke supplier 2 juta"
   Expected: Konfirmasi transaksi payable 2000000

✅ Input: "Hutang bank 10 juta"
   Expected: Konfirmasi transaksi payable 10000000
```

### 3. Test Natural Language Variations

```
✅ "dapat 500rb"
✅ "terima 500 ribu"
✅ "masuk 500000"
✅ "bayar 300rb"
✅ "keluar 300 ribu"
✅ "pengeluaran 300000"
```

### 4. Test Accounting Q&A

```
Input: "Bagaimana cara menghitung laba rugi?"
Expected: Penjelasan lengkap dari AI

Input: "Apa itu arus kas?"
Expected: Penjelasan tentang cash flow

Input: "Jelaskan tentang piutang"
Expected: Penjelasan tentang receivables
```

### 5. Test Edge Cases

```
❌ Input: "hello"
   Expected: AI response atau prompt untuk bertransaksi

❌ Input: "1234567"
   Expected: Tidak bisa parse, minta klarifikasi

❌ Input: Random text
   Expected: Graceful handling, tidak error
```

## 🌐 API Testing

### Using cURL

**1. Health Check:**
```bash
curl http://localhost:8000/health
```

**2. Dashboard Overview:**
```bash
curl http://localhost:8000/api/dashboard/overview | python3 -m json.tool
```

**3. Transaction Stats:**
```bash
curl http://localhost:8000/api/transactions/stats | python3 -m json.tool
```

**4. Daily Transactions:**
```bash
curl "http://localhost:8000/api/transactions/daily?days=30" | python3 -m json.tool
```

**5. Generate Forecast:**
```bash
curl -X POST http://localhost:8000/api/predictions/forecast \
  -H "Content-Type: application/json" \
  -d '{"periods": 30}' | python3 -m json.tool
```

**6. Detect Anomalies:**
```bash
curl -X POST http://localhost:8000/api/predictions/anomaly \
  -H "Content-Type: application/json" \
  -d '{}' | python3 -m json.tool
```

**7. Get Bot Logs:**
```bash
curl "http://localhost:8000/api/bot-logs?limit=10" | python3 -m json.tool
```

### Using API Documentation

```bash
# Open Swagger UI
open http://localhost:8000/docs

# Or ReDoc
open http://localhost:8000/redoc
```

Test all endpoints interactively.

## 📊 Dashboard Testing

### 1. Load Dashboard

```bash
open http://localhost:3000
```

**Verify:**
- [ ] Page loads without errors
- [ ] Bot status shows "Active"
- [ ] All stats cards display data
- [ ] No console errors (F12)

### 2. Test Stats Cards

**Expected Data:**
- Total Pemasukan: Sum of all income
- Total Pengeluaran: Sum of all expense
- Saldo: Income - Expense
- Total Transaksi: Count of all transactions

**Verify:**
- [ ] Numbers are formatted correctly (Rp x,xxx,xxx)
- [ ] Icons display correctly
- [ ] Hover effects work

### 3. Test Transaction Chart

**Expected:**
- Line chart with 30 days of data
- Green line: Income
- Red line: Expense
- X-axis: Dates
- Y-axis: Amounts
- Tooltip on hover

**Test:**
- [ ] Chart renders without errors
- [ ] Hover shows correct tooltips
- [ ] Lines are smooth
- [ ] Legend is correct

### 4. Test Category Chart

**Expected:**
- Pie chart showing expense categories
- Different colors per category
- Percentage labels
- Legend

**Test:**
- [ ] Chart renders
- [ ] Hover shows values
- [ ] Percentages add up to 100%
- [ ] Colors are distinct

### 5. Test Forecast Chart

**Test:**
```
1. Click "Generate Forecast" button
2. Wait for loading
3. Verify chart appears
4. Check 30 data points
5. Verify purple dashed line
6. Check tooltips
```

**Expected:**
- [ ] Button disabled during loading
- [ ] Chart displays predictions
- [ ] Dates are sequential
- [ ] Amounts are reasonable

### 6. Test Anomaly Detection

**Test:**
```
1. Create some normal transactions
2. Create outlier transaction (very high/low amount)
3. Click "Detect Anomalies"
4. Verify outlier is detected
```

**Expected:**
- [ ] Anomalies display in red cards
- [ ] Shows transaction details
- [ ] Shows reason for anomaly
- [ ] Amount and date correct

### 7. Test Bot Logs

**Expected:**
- Real-time log display
- Color coding by level (info/error/warning)
- User input and bot response
- Timestamps
- Auto-refresh every 10 seconds

**Test:**
- [ ] Logs display correctly
- [ ] Colors match log levels
- [ ] Truncation works for long messages
- [ ] Scrollable if many logs

### 8. Test Responsiveness

**Test on different screen sizes:**
- [ ] Desktop (1920x1080)
- [ ] Laptop (1366x768)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

## 🧠 ML Models Testing

### Forecasting Model

**Test Scenarios:**

**1. Insufficient Data:**
```python
# Less than 7 days of data
Expected: "insufficient_data" status
```

**2. Normal Forecast:**
```python
# 30+ days of income data
Expected: 30 forecast points with reasonable values
```

**3. Verify Algorithm:**
- Check if trend is captured
- Predictions should not be negative
- Confidence level present

### Anomaly Detection Model

**Test Scenarios:**

**1. Insufficient Data:**
```python
# Less than 10 transactions
Expected: "insufficient_data" status
```

**2. Normal Transactions:**
```python
# All transactions around same amount
Expected: Few or no anomalies
```

**3. Clear Outliers:**
```python
# One transaction 10x larger than others
Expected: Detected as anomaly
```

**4. Verify Features:**
- Amount deviation
- Time patterns
- Transaction type patterns

## 🔗 Integration Testing

### End-to-End Flow

**Test Complete Transaction Flow:**

```
1. Send message to bot: "Terima uang 500rb"
2. Verify bot response confirms transaction
3. Check database:
   docker-compose exec postgres psql -U cuanbot -d cuanbot_db -c "SELECT * FROM transactions ORDER BY created_at DESC LIMIT 1;"
4. Refresh dashboard
5. Verify transaction appears in stats
6. Check transaction chart updated
7. Verify bot log created
```

### Database Integration

**Test CRUD Operations:**

```bash
# Access database
docker-compose exec postgres psql -U cuanbot -d cuanbot_db

# Check users
SELECT * FROM users;

# Check transactions
SELECT * FROM transactions ORDER BY created_at DESC LIMIT 10;

# Check bot_logs
SELECT * FROM bot_logs ORDER BY created_at DESC LIMIT 10;

# Check predictions
SELECT * FROM predictions ORDER BY created_at DESC LIMIT 5;
```

### Webhook Integration

**Test Telegram Webhook:**

```bash
# 1. Check webhook status
curl https://api.telegram.org/bot<YOUR_TOKEN>/getWebhookInfo

# Expected output:
{
  "ok": true,
  "result": {
    "url": "https://your-ngrok-url.ngrok.io/webhook/telegram",
    "has_custom_certificate": false,
    "pending_update_count": 0,
    "last_error_date": 0
  }
}

# 2. Test webhook endpoint
curl -X POST http://localhost:8000/webhook/telegram \
  -H "Content-Type: application/json" \
  -d '{}'

# Should return: {"ok": true}
```

## 📝 Test Checklist

### Before Release

**Bot:**
- [ ] All commands work (/start, /help, /summary)
- [ ] Transaction parsing works for all types
- [ ] Natural language variations handled
- [ ] Error handling works
- [ ] Logs are created

**Dashboard:**
- [ ] All components render
- [ ] Data loads correctly
- [ ] Charts display properly
- [ ] ML features work
- [ ] Responsive on all devices
- [ ] No console errors

**API:**
- [ ] All endpoints return correct data
- [ ] Error handling works
- [ ] CORS configured
- [ ] Health check passes

**Database:**
- [ ] All tables exist
- [ ] Relationships work
- [ ] Data persists after restart
- [ ] Migrations work

**Infrastructure:**
- [ ] Docker containers start
- [ ] Services can communicate
- [ ] Volumes persist data
- [ ] Ngrok tunnel works

**Security:**
- [ ] Environment variables loaded
- [ ] No secrets in logs
- [ ] Database password works
- [ ] Bot token secure

## 🐛 Common Issues & Fixes

### Issue: Bot not responding

**Check:**
```bash
# Webhook status
curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo

# Backend logs
docker-compose logs backend

# Ngrok status
curl http://localhost:4040/api/tunnels
```

**Fix:**
```bash
# Reset webhook
./scripts/set_webhook.sh <TOKEN> <NGROK_URL>/webhook/telegram
docker-compose restart backend
```

### Issue: Dashboard not loading data

**Check:**
```bash
# Backend API
curl http://localhost:8000/health

# Browser console (F12)
```

**Fix:**
```bash
# Restart services
docker-compose restart backend dashboard
```

### Issue: Database connection error

**Check:**
```bash
# Database status
docker-compose exec postgres pg_isready -U cuanbot
```

**Fix:**
```bash
# Restart database
docker-compose restart postgres
# Wait 10 seconds
docker-compose restart backend
```

## 📊 Performance Testing

### Load Testing Bot

```bash
# Send multiple messages quickly
# Monitor response time
# Check memory usage: docker stats
```

### Load Testing API

```bash
# Use Apache Bench
ab -n 100 -c 10 http://localhost:8000/api/transactions/stats

# Or use wrk
wrk -t4 -c100 -d30s http://localhost:8000/api/transactions/
```

## ✅ Test Results Documentation

Document test results:

```markdown
## Test Results - [Date]

### Bot Tests
- [x] Commands: PASS
- [x] Transaction parsing: PASS
- [x] Q&A: PASS
- [x] Error handling: PASS

### Dashboard Tests
- [x] Load time: < 2s
- [x] All charts render: PASS
- [x] ML features: PASS
- [x] Responsive: PASS

### API Tests
- [x] All endpoints: PASS
- [x] Response time: < 500ms
- [x] Error handling: PASS

### Integration Tests
- [x] End-to-end flow: PASS
- [x] Database persistence: PASS
- [x] Webhook: PASS
```

---

**Happy Testing! 🧪**
