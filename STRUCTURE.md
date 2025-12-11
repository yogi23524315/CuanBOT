# 📂 CuanBot Project Structure

```
CuanBOTv3/
│
├── 📄 README.md                    # Main documentation
├── 📄 QUICKSTART.md                # Quick start guide (5 minutes)
├── 📄 DEPLOYMENT.md                # Production deployment guide
├── 📄 STRUCTURE.md                 # This file - project structure
│
├── 🐳 docker-compose.yml           # Docker orchestration
├── 🔧 .env.example                 # Environment template
├── 🚫 .gitignore                   # Git ignore rules
├── 🚀 setup.sh                     # Quick setup script
│
├── 📁 backend/                     # Python FastAPI Backend
│   ├── 🐳 Dockerfile               # Backend container config
│   ├── 📦 requirements.txt         # Python dependencies
│   │
│   └── 📁 app/                     # Main application
│       ├── 🔧 config.py            # Configuration & settings
│       ├── 🗄️ database.py          # Database connection
│       ├── 🚀 main.py              # FastAPI app entry point
│       │
│       ├── 📁 models/              # SQLAlchemy ORM Models
│       │   ├── __init__.py
│       │   ├── user.py             # User model (Telegram users)
│       │   ├── transaction.py      # Transaction model
│       │   ├── bot_log.py          # Bot interaction logs
│       │   └── prediction.py       # ML prediction results
│       │
│       ├── 📁 services/            # Business Logic Layer
│       │   ├── __init__.py
│       │   ├── telegram_bot.py     # Telegram bot handler
│       │   ├── llm_service.py      # Gemini LLM integration
│       │   ├── ml_forecasting.py   # Revenue forecasting ML
│       │   └── ml_anomaly.py       # Anomaly detection ML
│       │
│       └── 📁 api/                 # REST API Endpoints
│           ├── __init__.py
│           ├── transactions.py     # Transaction endpoints
│           ├── predictions.py      # ML prediction endpoints
│           └── bot_logs.py         # Bot logs endpoints
│
├── 📁 dashboard/                   # Next.js Dashboard Frontend
│   ├── 🐳 Dockerfile               # Dashboard container config
│   ├── 📦 package.json             # Node.js dependencies
│   ├── 🔧 next.config.js           # Next.js configuration
│   ├── 🎨 tailwind.config.js       # Tailwind CSS config
│   ├── 📝 tsconfig.json            # TypeScript config
│   ├── 🎨 postcss.config.js        # PostCSS config
│   │
│   └── 📁 src/                     # Source code
│       ├── 📁 app/                 # Next.js 14 App Router
│       │   ├── layout.tsx          # Root layout
│       │   ├── page.tsx            # Main dashboard page
│       │   └── globals.css         # Global styles
│       │
│       ├── 📁 components/          # React Components
│       │   ├── StatsCards.tsx      # Financial stats cards
│       │   ├── TransactionChart.tsx # Daily transaction chart
│       │   ├── CategoryChart.tsx   # Category pie chart
│       │   ├── ForecastChart.tsx   # ML forecast chart
│       │   ├── AnomalyList.tsx     # Anomaly detection list
│       │   └── BotLogs.tsx         # Bot activity logs
│       │
│       └── 📁 lib/                 # Utilities & helpers
│           └── api.ts              # API client functions
│
├── 📁 init-db/                     # Database Initialization
│   └── init.sql                    # PostgreSQL init script
│
└── 📁 scripts/                     # Utility Scripts
    ├── set_webhook.sh              # Set Telegram webhook
    └── check_health.sh             # Health check script

```

## 🔍 Key Components

### Backend (FastAPI)

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| **main.py** | Application entry point | FastAPI app, CORS, webhook endpoint |
| **telegram_bot.py** | Bot handler | Commands, message processing, NLP |
| **llm_service.py** | AI integration | Gemini API, transaction parsing, Q&A |
| **ml_forecasting.py** | Revenue prediction | Linear regression, time series |
| **ml_anomaly.py** | Fraud detection | Isolation Forest algorithm |
| **models/** | Database schema | SQLAlchemy ORM models |
| **api/** | REST endpoints | Transaction, prediction, logs APIs |

### Dashboard (Next.js)

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| **page.tsx** | Main dashboard | Layout, data fetching, state management |
| **StatsCards** | Financial overview | Income, expense, balance, count |
| **TransactionChart** | Trend visualization | Line chart, 30-day data |
| **CategoryChart** | Spending breakdown | Pie chart, category distribution |
| **ForecastChart** | ML predictions | Revenue forecast, 30 days ahead |
| **AnomalyList** | Fraud detection | Suspicious transactions |
| **BotLogs** | Activity monitor | Real-time bot interactions |
| **api.ts** | API client | Axios-based API calls |

## 🗄️ Database Schema

```sql
-- Users (Telegram users)
users
├── id (PK)
├── telegram_id (unique)
├── username
├── first_name
├── last_name
├── is_active
├── created_at
└── updated_at

-- Transactions (Financial records)
transactions
├── id (PK)
├── user_id (FK → users)
├── transaction_type (income/expense/receivable/payable)
├── amount
├── category
├── description
├── transaction_date
├── is_anomaly
├── anomaly_score
├── created_at
└── updated_at

-- Bot Logs (Interaction history)
bot_logs
├── id (PK)
├── user_id (FK → users)
├── level (info/warning/error/debug)
├── message
├── user_input
├── bot_response
└── created_at

-- Predictions (ML results)
predictions
├── id (PK)
├── prediction_type (forecast/anomaly)
├── prediction_data (JSON)
├── metadata (JSON)
└── created_at
```

## 🔄 Data Flow

### Transaction Recording Flow

```
User (Telegram)
    ↓ "Terima uang 500rb"
Telegram Bot (webhook)
    ↓
LLM Service (Gemini)
    ↓ Parse NLP → {type: income, amount: 500000}
Transaction Service
    ↓
PostgreSQL Database
    ↓
Dashboard (API) ← Real-time display
```

### ML Prediction Flow

```
Dashboard UI
    ↓ Click "Generate Forecast"
API Request (POST /api/predictions/forecast)
    ↓
Fetch Transactions from DB
    ↓
ML Forecasting Service (Linear Regression)
    ↓
Save Prediction to DB
    ↓
Return Results to Dashboard
    ↓
Display Chart
```

## 🐳 Docker Services

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| **postgres** | postgres:16-alpine | 5432 | PostgreSQL database |
| **backend** | Custom (Python) | 8000 | FastAPI backend |
| **dashboard** | Custom (Node) | 3000 | Next.js dashboard |
| **ngrok** | ngrok/ngrok | 4040 | Tunnel for webhooks |

## 📊 API Endpoints

### Transactions
- `GET /api/transactions/` - List transactions
- `GET /api/transactions/stats` - Get statistics
- `GET /api/transactions/daily` - Daily aggregates
- `GET /api/transactions/by-category` - Category breakdown

### Predictions
- `POST /api/predictions/forecast` - Generate forecast
- `POST /api/predictions/anomaly` - Detect anomalies
- `GET /api/predictions/history` - Prediction history

### Bot Logs
- `GET /api/bot-logs/` - List logs
- `GET /api/bot-logs/stats` - Bot statistics

### System
- `GET /` - API info
- `GET /health` - Health check
- `POST /webhook/telegram` - Telegram webhook
- `GET /api/dashboard/overview` - Dashboard overview

## 🔐 Environment Variables

### Required
- `TELEGRAM_BOT_TOKEN` - From @BotFather
- `GEMINI_API_KEY` - From Google AI Studio
- `NGROK_AUTHTOKEN` - From ngrok.com
- `SECRET_KEY` - Random secret key

### Database
- `POSTGRES_USER` - DB username
- `POSTGRES_PASSWORD` - DB password
- `POSTGRES_DB` - Database name
- `DATABASE_URL` - Full connection string

### Optional
- `TELEGRAM_WEBHOOK_URL` - Webhook URL (set after ngrok starts)
- `NEXT_PUBLIC_API_URL` - API URL for dashboard

## 📦 Dependencies

### Backend (Python)
- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **python-telegram-bot** - Telegram bot SDK
- **sqlalchemy** - ORM
- **psycopg2-binary** - PostgreSQL driver
- **google-generativeai** - Gemini API
- **pandas, numpy** - Data processing
- **scikit-learn** - ML models

### Dashboard (TypeScript)
- **next** - React framework
- **react** - UI library
- **recharts** - Charts library
- **axios** - HTTP client
- **tailwindcss** - CSS framework
- **lucide-react** - Icons

## 🚀 Getting Started

1. **Quick Start**: Read `QUICKSTART.md` (5 minutes)
2. **Full Guide**: Read `README.md` (comprehensive)
3. **Production**: Read `DEPLOYMENT.md` (deployment guide)

## 📝 Development Workflow

1. Clone repository
2. Setup environment (`.env`)
3. Start Docker services
4. Configure webhook (ngrok)
5. Test bot in Telegram
6. Monitor via dashboard
7. Check logs for debugging

## 🎯 Production Checklist

- [ ] Change default passwords
- [ ] Use strong SECRET_KEY
- [ ] Setup proper domain & SSL
- [ ] Use managed database
- [ ] Configure firewall
- [ ] Setup monitoring
- [ ] Configure backups
- [ ] Add authentication to dashboard
- [ ] Implement rate limiting
- [ ] Setup CI/CD

---

**For more details, see:**
- 📖 README.md - Full documentation
- ⚡ QUICKSTART.md - Quick start guide
- 🚀 DEPLOYMENT.md - Deployment guide
