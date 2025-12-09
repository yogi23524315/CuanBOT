# CuanBOT
## Getting started

<<<<<<< HEAD
## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
=======
## 📱 Cara Menggunakan Bot

### Mencatat Transaksi

Cukup chat dengan bahasa natural:

```
✅ "Terima pembayaran dari customer 500rb"
✅ "Bayar listrik 300 ribu"
✅ "Piutang si Budi 1 juta"
✅ "Hutang ke supplier 2 juta untuk stok barang"
✅ "Dapat transfer dari customer A sebesar 1.5 juta untuk pembelian produk X"
```

### Commands

- `/start` - Mulai bot & lihat panduan
- `/help` - Bantuan lengkap
- `/summary` - Ringkasan keuangan Anda

### Bertanya

```
"Bagaimana cara menghitung laba rugi?"
"Apa itu arus kas?"
"Jelaskan tentang piutang dan hutang"
```

## 🎨 Dashboard Features

### 1. Overview Cards
- Total Pemasukan
- Total Pengeluaran
- Saldo
- Jumlah Transaksi

### 2. Charts & Analytics
- **Daily Transaction Chart**: Trend harian income vs expense
- **Category Breakdown**: Pie chart pengeluaran per kategori
- **Revenue Forecast**: Prediksi 30 hari ke depan (ML)
- **Anomaly Detection**: Transaksi mencurigakan (ML)

### 3. Bot Monitoring
- Real-time logs
- Activity tracking
- Error monitoring

## 🔧 Development

### Project Structure

```
CuanBOTv3/
├── backend/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── models/            # SQLAlchemy models
│   │   ├── services/          # Business logic
│   │   │   ├── telegram_bot.py
│   │   │   ├── llm_service.py
│   │   │   ├── ml_forecasting.py
│   │   │   └── ml_anomaly.py
│   │   ├── api/               # REST API endpoints
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
│
├── dashboard/                  # Next.js Dashboard
│   ├── src/
│   │   ├── app/               # Next.js 14 App Router
│   │   ├── components/        # React components
│   │   └── lib/               # Utilities & API client
│   ├── package.json
│   └── Dockerfile
│
├── init-db/                    # Database initialization
│   └── init.sql
│
├── docker-compose.yml          # Docker orchestration
├── .env.example               # Environment template
└── README.md
```

### Running Locally (Development)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Dashboard:**
```bash
cd dashboard
npm install
npm run dev
```

### API Documentation

Setelah backend running, akses:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

### Manual Testing Telegram Bot

1. Start bot dengan `/start`
2. Test pencatatan transaksi:
   ```
   "Terima uang 500rb dari customer"
   "Bayar gaji 2 juta"
   ```
3. Check dengan `/summary`

### Testing Dashboard

1. Access http://localhost:3000
2. Verify semua cards menampilkan data
3. Test ML features:
   - Click "Generate Forecast"
   - Click "Detect Anomalies"

## 📊 Database Schema

### Tables

- **users**: Telegram user data
- **transactions**: Financial transactions
- **bot_logs**: Bot interaction logs
- **predictions**: ML prediction results

## 🔐 Security Notes

⚠️ **Important for Production:**

1. Change all default passwords
2. Use strong SECRET_KEY
3. Enable HTTPS for webhook
4. Implement authentication for dashboard
5. Add rate limiting
6. Regular database backups

## 🐛 Troubleshooting

### Webhook Issues

```bash
# Check ngrok status
curl http://localhost:4040/api/tunnels

# Manually set webhook
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook?url=<NGROK_URL>/webhook/telegram"
```

### Database Connection Issues

```bash
# Check PostgreSQL
docker-compose exec postgres psql -U cuanbot -d cuanbot_db -c "\dt"

# Reset database
docker-compose down -v
docker-compose up -d
```

### Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f dashboard
```

## 🚀 Deployment (Production)

### Quick Deploy to ubuntu@vm-4-97-ubuntu

```bash
cd deployment
cp .env.example .env
nano .env  # Configure your production credentials
./deploy-to-server.sh latest
```

**Complete Deployment Documentation:**
- 📖 [deployment/DEPLOY_README.md](deployment/DEPLOY_README.md) - Step-by-step deployment guide
- ⚡ [deployment/QUICK_REFERENCE.md](deployment/QUICK_REFERENCE.md) - Quick reference commands
- ✅ [deployment/DEPLOYMENT_CHECKLIST.md](deployment/DEPLOYMENT_CHECKLIST.md) - Deployment checklist

**Management Commands:**
```bash
./server-commands.sh logs      # View logs
./server-commands.sh status    # Check status
./server-commands.sh restart   # Restart services
./server-commands.sh backup    # Backup database
./server-commands.sh monitor   # Real-time monitoring
```

### Using Docker Compose (Manual)

1. Update `.env` dengan production credentials
2. Use production-grade secrets
3. Setup proper domain & SSL
4. Use managed PostgreSQL (e.g., AWS RDS, Google Cloud SQL)
5. Deploy to cloud (AWS, GCP, Azure)

### Recommendations

- Use Kubernetes for scalability
- Implement CI/CD pipeline
- Setup monitoring (Prometheus, Grafana)
- Add backup automation
- Implement proper logging (ELK stack)

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ for Indonesian UMKM**
# CuanBOT
>>>>>>> 3753bb1 (first commit)
