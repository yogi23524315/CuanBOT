# ⚡ CuanBot Quick Start Guide

Panduan cepat untuk memulai CuanBot dalam 5 menit!

## 🎯 Prerequisites Checklist

Sebelum mulai, pastikan Anda sudah punya:

- [ ] Docker & Docker Compose installed
- [ ] Telegram Bot Token dari @BotFather
- [ ] Gemini API Key dari Google AI Studio
- [ ] Ngrok Authtoken dari ngrok.com (untuk development)

## 🚀 Setup dalam 5 Langkah

### 1️⃣ Clone & Setup Environment

```bash
git clone <repository-url>
cd CuanBOTv3
cp .env.example .env
```

### 2️⃣ Edit File .env

Buka `.env` dan isi credentials Anda:

```env
# WAJIB DIISI:
TELEGRAM_BOT_TOKEN=paste_token_dari_botfather
GEMINI_API_KEY=paste_api_key_dari_google
NGROK_AUTHTOKEN=paste_authtoken_dari_ngrok

# Generate secret key:
SECRET_KEY=paste_hasil_dari_command_di_bawah

# OPTIONAL (gunakan default untuk testing):
POSTGRES_PASSWORD=ganti_dengan_password_aman_untuk_production
```

Generate secret key:
```bash
openssl rand -base64 32
```

### 3️⃣ Start Application

```bash
# Jalankan setup script
chmod +x setup.sh
./setup.sh

# Atau manual:
docker-compose up -d
```

Tunggu 30 detik sampai semua service siap.

### 4️⃣ Setup Webhook

```bash
# 1. Buka ngrok dashboard
open http://localhost:4040
# Atau: curl http://localhost:4040/api/tunnels

# 2. Copy URL yang ada (contoh: https://abc123.ngrok.io)

# 3. Update .env
nano .env
# Tambahkan/update line:
TELEGRAM_WEBHOOK_URL=https://abc123.ngrok.io/webhook/telegram

# 4. Restart backend
docker-compose restart backend

# 5. Set webhook (optional, otomatis by backend)
./scripts/set_webhook.sh YOUR_BOT_TOKEN https://abc123.ngrok.io/webhook/telegram
```

### 5️⃣ Test & Enjoy! 🎉

**Test Telegram Bot:**
1. Buka Telegram
2. Cari bot Anda (nama yang Anda set di BotFather)
3. Send `/start`
4. Test transaction: "Terima uang 500 ribu dari customer"

**Buka Dashboard:**
```bash
open http://localhost:3000
```

## 📱 Contoh Penggunaan Bot

### Mencatat Transaksi

```
✅ "Terima pembayaran 500rb"
✅ "Bayar listrik 300 ribu"  
✅ "Piutang Toko A 1 juta"
✅ "Hutang supplier 2 juta untuk stok"
✅ "Dapat transfer 1.5 juta dari customer B untuk produk X"
```

Bot akan otomatis:
- Parse natural language
- Ekstrak jumlah, tipe, kategori
- Simpan ke database
- Reply konfirmasi

### Commands

```
/start   - Mulai & lihat panduan
/help    - Bantuan lengkap
/summary - Ringkasan keuangan
```

### Tanya Jawab Akunting

```
"Bagaimana cara menghitung laba rugi?"
"Apa itu arus kas?"
"Jelaskan tentang piutang dan hutang"
```

## 📊 Dashboard Features

**URL:** http://localhost:3000

**Features:**
- 💰 Stats Cards: Income, Expense, Balance, Count
- 📈 Daily Transaction Chart (line chart)
- 🥧 Category Breakdown (pie chart)
- 🔮 Forecast Revenue (ML prediction - 30 days)
- 🚨 Anomaly Detection (ML fraud detection)
- 📝 Bot Activity Logs (real-time)

**Generate Predictions:**
1. Click "Generate Forecast" → prediksi 30 hari
2. Click "Detect Anomalies" → cek transaksi janggal

## 🔧 Useful Commands

```bash
# Check status semua services
docker-compose ps

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f dashboard

# Restart service
docker-compose restart backend

# Stop all services
docker-compose down

# Stop & remove all data (CAREFUL!)
docker-compose down -v

# Check health
./scripts/check_health.sh

# Access database
docker-compose exec postgres psql -U cuanbot -d cuanbot_db

# View backend API docs
open http://localhost:8000/docs
```

## 🌐 Access URLs

- 🤖 **Telegram Bot**: Your bot in Telegram app
- 📊 **Dashboard**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs
- 📡 **Ngrok Dashboard**: http://localhost:4040
- 🗄️ **PostgreSQL**: localhost:5432

## 🐛 Troubleshooting

### Bot tidak merespon

```bash
# 1. Check logs
docker-compose logs backend

# 2. Check webhook
curl https://api.telegram.org/botYOUR_TOKEN/getWebhookInfo

# 3. Check ngrok
curl http://localhost:4040/api/tunnels

# 4. Restart & set webhook ulang
docker-compose restart backend
./scripts/set_webhook.sh YOUR_TOKEN YOUR_NGROK_URL/webhook/telegram
```

### Dashboard tidak load data

```bash
# 1. Check backend API
curl http://localhost:8000/health

# 2. Check database
docker-compose exec postgres pg_isready -U cuanbot

# 3. Check browser console (F12)

# 4. Restart services
docker-compose restart
```

### Ngrok URL berubah setiap restart

Ngrok free tier memberikan URL random setiap restart. Options:
1. Gunakan ngrok premium untuk fixed domain
2. Setup webhook manual setiap restart
3. Deploy ke production dengan domain sendiri

### Database error

```bash
# Check database connection
docker-compose exec postgres psql -U cuanbot -d cuanbot_db -c "SELECT version();"

# Reset database (CAUTION: deletes all data)
docker-compose down -v
docker-compose up -d
```

## 📖 Next Steps

**Untuk Development:**
1. Baca `README.md` untuk detail lengkap
2. Explore API docs di http://localhost:8000/docs
3. Customize bot messages di `backend/app/services/telegram_bot.py`
4. Customize dashboard di `dashboard/src/`

**Untuk Production:**
1. Baca `DEPLOYMENT.md` untuk panduan lengkap
2. Setup domain & SSL certificate
3. Use managed database
4. Implement proper security measures

## 💡 Tips

1. **Testing locally**: Gunakan ngrok untuk development
2. **Multiple users**: Bot support multiple users otomatis
3. **Data persistence**: Data disimpan di PostgreSQL volume
4. **Backup**: Setup auto backup untuk production
5. **Monitoring**: Check logs regularly

## 🎓 Learn More

- **Telegram Bot API**: https://core.telegram.org/bots/api
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Next.js Docs**: https://nextjs.org/docs
- **Gemini API**: https://ai.google.dev/

## 📞 Need Help?

1. Check logs: `docker-compose logs -f`
2. Run health check: `./scripts/check_health.sh`
3. Read full docs in `README.md`
4. Check `DEPLOYMENT.md` for production issues
5. Open issue on GitHub

---

**Selamat mencoba! Happy coding! 🚀**
