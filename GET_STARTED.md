# 🚀 Getting Started with CuanBot

Complete step-by-step guide untuk mulai menggunakan CuanBot dari nol.

## 📚 Navigation

- **Quick Start (5 menit)** → Baca [QUICKSTART.md](QUICKSTART.md)
- **Full Documentation** → Baca [README.md](README.md)
- **Production Deployment** → Baca [DEPLOYMENT.md](DEPLOYMENT.md)
- **Project Structure** → Baca [STRUCTURE.md](STRUCTURE.md)
- **Testing Guide** → Baca [TESTING.md](TESTING.md)

## 🎯 Before You Start

### What is CuanBot?

CuanBot adalah aplikasi chatbot akunting untuk UMKM Indonesia yang memungkinkan:

✅ **Pencatatan transaksi via chat Telegram** dengan bahasa natural  
✅ **Dashboard web beautiful** dengan visualisasi data real-time  
✅ **AI-powered** dengan Gemini 2.5 Flash untuk parsing & Q&A  
✅ **Machine Learning** untuk forecasting & anomaly detection  
✅ **Production-ready** dengan Docker & PostgreSQL  

### What You Need

**Required:**
- [ ] Computer dengan Docker installed
- [ ] Telegram account
- [ ] Internet connection

**API Keys (gratis):**
- [ ] Telegram Bot Token (dari @BotFather)
- [ ] Gemini API Key (dari Google AI Studio)  
- [ ] Ngrok Authtoken (dari ngrok.com) - untuk development

**Estimated Time:** 10-15 menit untuk first-time setup

## 🛠️ Step-by-Step Setup

### Step 1: Install Docker

**MacOS:**
```bash
# Install Docker Desktop
brew install --cask docker
# Atau download dari: https://www.docker.com/products/docker-desktop
```

**Linux:**
```bash
# Install Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt install docker-compose -y

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

**Windows:**
```
Download & install Docker Desktop:
https://www.docker.com/products/docker-desktop
```

**Verify Installation:**
```bash
docker --version
docker-compose --version
```

### Step 2: Get API Keys

#### 2.1 Telegram Bot Token

1. Buka Telegram dan search `@BotFather`
2. Send `/newbot`
3. Follow instructions:
   - Bot name: `CuanBot UMKM` (atau nama lain)
   - Username: `cuanbot_umkm_bot` (harus unik, akhiran _bot)
4. Copy token yang diberikan: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
5. Save token ini, akan digunakan di Step 4

**Tips:** Test bot dengan send `/start`, seharusnya belum respon.

#### 2.2 Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Login dengan Google account
3. Click **"Create API Key"**
4. Select **"Create API key in new project"** 
5. Copy API key: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXX`
6. Save key ini

**Free Tier:** 60 requests per minute, cukup untuk testing.

#### 2.3 Ngrok Authtoken

1. Sign up di [ngrok.com](https://dashboard.ngrok.com/signup)
2. Login ke dashboard
3. Go to [Your Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
4. Copy authtoken: `2abcdefGHIJKLMNOP_qrstuvwxyz123`
5. Save token ini

**Free Tier:** Random URL setiap restart (cukup untuk development).

### Step 3: Clone & Setup Project

```bash
# Clone repository
git clone https://github.com/your-username/CuanBOTv3.git
cd CuanBOTv3

# Create .env file
cp .env.example .env
```

### Step 4: Configure Environment

Edit file `.env`:

```bash
# Open with your favorite editor
nano .env
# atau: code .env
# atau: vim .env
```

**Fill in these values:**

```env
# Database (default sudah OK untuk testing)
POSTGRES_USER=cuanbot
POSTGRES_PASSWORD=cuanbot123  # ⚠️ CHANGE IN PRODUCTION!
POSTGRES_DB=cuanbot_db
DATABASE_URL=postgresql://cuanbot:cuanbot123@postgres:5432/cuanbot_db

# Telegram Bot (PASTE YOUR TOKEN)
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_WEBHOOK_URL=  # Will be filled in Step 6

# Gemini API (PASTE YOUR KEY)
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXX

# Ngrok (PASTE YOUR AUTHTOKEN)
NGROK_AUTHTOKEN=2abcdefGHIJKLMNOP_qrstuvwxyz123

# Backend Secret (GENERATE NEW ONE)
SECRET_KEY=your_secret_key_here_generate_below

# Dashboard
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Generate Secret Key:**

```bash
# Method 1: OpenSSL
openssl rand -base64 32

# Method 2: Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Copy output and paste to SECRET_KEY
```

**Save the file** (Ctrl+X, Y, Enter in nano)

### Step 5: Start Application

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# Should see:
# - cuanbot-postgres (healthy)
# - cuanbot-backend (running)
# - cuanbot-dashboard (running)
# - cuanbot-ngrok (running)
```

**First time will take 2-3 minutes** to download images and build.

**View logs:**
```bash
docker-compose logs -f
# Press Ctrl+C to exit logs (services keep running)
```

### Step 6: Configure Webhook

**Get Ngrok URL:**

```bash
# Open ngrok dashboard
open http://localhost:4040

# Or get URL via command
curl -s http://localhost:4040/api/tunnels | python3 -m json.tool | grep "public_url"
```

**Copy the HTTPS URL** (example: `https://abc123.ngrok.io`)

**Update .env:**

```bash
nano .env

# Update this line:
TELEGRAM_WEBHOOK_URL=https://abc123.ngrok.io/webhook/telegram

# Save and exit
```

**Restart Backend:**

```bash
docker-compose restart backend

# Wait 5 seconds, then check logs
docker-compose logs backend
```

**Verify webhook (optional):**

```bash
# Set webhook manually (if needed)
./scripts/set_webhook.sh YOUR_BOT_TOKEN https://abc123.ngrok.io/webhook/telegram

# Check webhook info
curl https://api.telegram.org/botYOUR_BOT_TOKEN/getWebhookInfo
```

### Step 7: Test Everything!

#### Test 1: Bot

1. **Open Telegram**
2. **Search your bot** (username dari Step 2.1)
3. **Send `/start`**
   - Should get welcome message 🎉
4. **Test transaction:**
   ```
   Terima uang 500 ribu dari customer
   ```
   - Should get confirmation ✅
5. **Check summary:**
   ```
   /summary
   ```
   - Should show stats with AI insights

#### Test 2: Dashboard

```bash
# Open dashboard
open http://localhost:3000
```

**Verify:**
- [ ] Bot status: Active (green)
- [ ] Stats cards show data
- [ ] Charts render
- [ ] No errors in browser console (F12)

**Test ML features:**
1. Click **"Generate Forecast"**
   - Should see prediction chart
2. Click **"Detect Anomalies"**
   - Should analyze transactions

#### Test 3: API

```bash
# Health check
curl http://localhost:8000/health

# Should return: {"status":"healthy"}

# API documentation
open http://localhost:8000/docs
```

## ✅ Success Checklist

You're ready if:

- [ ] Docker containers running (all 4 services)
- [ ] Bot responds to `/start` in Telegram
- [ ] Bot records transactions correctly
- [ ] Dashboard loads at http://localhost:3000
- [ ] Stats cards show correct data
- [ ] Charts display properly
- [ ] ML features work (forecast & anomaly)
- [ ] Bot logs appear in dashboard
- [ ] No errors in logs

## 🎓 Next Steps

### Learn the Basics

**Bot Commands:**
- `/start` - Welcome & help
- `/help` - Detailed guide
- `/summary` - Financial summary

**Transaction Formats:**
```
"Terima uang 500rb"           → Income
"Bayar listrik 300 ribu"      → Expense
"Piutang Toko A 1 juta"       → Receivable
"Hutang supplier 2 juta"      → Payable
```

**Ask Accounting Questions:**
```
"Bagaimana cara menghitung laba rugi?"
"Apa itu arus kas?"
```

### Explore Dashboard

1. **Overview Cards** - Quick stats
2. **Transaction Chart** - Daily trends
3. **Category Chart** - Spending breakdown
4. **Forecast** - ML revenue prediction
5. **Anomaly Detection** - Fraud detection
6. **Bot Logs** - Activity monitoring

### Customize

**Backend:**
- Edit bot messages: `backend/app/services/telegram_bot.py`
- Add categories: Modify LLM prompts
- Improve ML: `backend/app/services/ml_*.py`

**Dashboard:**
- Change colors: `dashboard/tailwind.config.js`
- Add charts: Create new components
- Modify layout: `dashboard/src/app/page.tsx`

## 🐛 Troubleshooting

### Bot Not Responding

**Problem:** Send message tapi bot tidak respon

**Solution:**
```bash
# 1. Check webhook
curl https://api.telegram.org/botYOUR_TOKEN/getWebhookInfo

# 2. Check backend logs
docker-compose logs backend | tail -50

# 3. Check ngrok
curl http://localhost:4040/api/tunnels

# 4. Restart & reset webhook
docker-compose restart backend
./scripts/set_webhook.sh YOUR_TOKEN YOUR_NGROK_URL/webhook/telegram
```

### Dashboard Not Loading

**Problem:** Dashboard blank atau stuck loading

**Solution:**
```bash
# 1. Check backend API
curl http://localhost:8000/health

# 2. Check browser console (F12) for errors

# 3. Restart services
docker-compose restart backend dashboard

# 4. Clear browser cache
```

### Port Already in Use

**Problem:** Error "port 3000/8000/5432 already in use"

**Solution:**
```bash
# Find and kill process
# MacOS/Linux:
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9

# Or change ports in docker-compose.yml
```

### Database Connection Error

**Problem:** Backend can't connect to database

**Solution:**
```bash
# 1. Check database
docker-compose exec postgres pg_isready -U cuanbot

# 2. Restart database first
docker-compose restart postgres

# 3. Wait 10 seconds
sleep 10

# 4. Restart backend
docker-compose restart backend
```

### Ngrok URL Changes

**Problem:** Bot stops working after computer restart

**Reason:** Ngrok free tier gives random URL each time

**Solution:**
```bash
# 1. Get new ngrok URL
curl http://localhost:4040/api/tunnels

# 2. Update .env
nano .env
# Update TELEGRAM_WEBHOOK_URL

# 3. Restart backend
docker-compose restart backend

# 4. Verify webhook
./scripts/set_webhook.sh YOUR_TOKEN NEW_NGROK_URL/webhook/telegram
```

**Long-term:** 
- Get ngrok paid plan for fixed domain
- Deploy to production with your domain

## 📖 Additional Resources

- **Full Documentation:** [README.md](README.md)
- **Quick Reference:** [QUICKSTART.md](QUICKSTART.md)
- **Deploy to Production:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Project Structure:** [STRUCTURE.md](STRUCTURE.md)
- **Testing Guide:** [TESTING.md](TESTING.md)

## 💬 Support

**Need Help?**

1. Check logs: `docker-compose logs -f`
2. Run health check: `./scripts/check_health.sh`
3. Read documentation
4. Open issue on GitHub
5. Check [TESTING.md](TESTING.md) for common issues

## 🎉 You're All Set!

Congratulations! CuanBot is now running. 

**Start recording your transactions and watch your business grow! 📈**

---

**Made with ❤️ for Indonesian UMKM**
