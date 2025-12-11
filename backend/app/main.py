from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .database import engine, SessionLocal, Base
from .models import User, Transaction, BotLog, Prediction
from .api import transactions, predictions, bot_logs, reports
from .services.telegram_bot import TelegramBotService
from .config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting CuanBot application...")
    
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    
    global bot_service
    bot_service = TelegramBotService(SessionLocal)
    await bot_service.initialize()
    logger.info("Telegram bot initialized")
    
    yield
    
    logger.info("Shutting down CuanBot application...")

app = FastAPI(
    title="CuanBot API",
    description="Akunting Chatbot API untuk UMKM",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router)
app.include_router(predictions.router)
app.include_router(bot_logs.router)
app.include_router(reports.router)

@app.get("/")
def read_root():
    return {
        "message": "CuanBot API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/health/llm")
def llm_health_check():
    """Check if LLM service is working"""
    try:
        from .services.llm_service import llm_service
        
        # Test simple parsing
        test_result = llm_service.parse_transaction("Beli beras 100 ribu")
        
        return {
            "status": "healthy" if "error" not in test_result else "error",
            "model_initialized": llm_service.model is not None,
            "test_result": test_result
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@app.post("/test/parse")
async def test_parse_transaction(request: Request):
    """Test endpoint for parsing transactions"""
    try:
        data = await request.json()
        text = data.get("text", "")
        
        if not text:
            return {"error": "No text provided"}
        
        from .services.llm_service import llm_service
        
        # Test both parsing methods
        single_result = llm_service.parse_transaction(text)
        multi_result = llm_service.parse_multiple_transactions(text)
        
        return {
            "input": text,
            "single_parsing": single_result,
            "multiple_parsing": multi_result,
            "model_initialized": llm_service.model is not None
        }
    except Exception as e:
        return {"error": str(e)}

@app.head("/webhook/telegram")
async def telegram_webhook_head():
    return {"ok": True}

@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    try:
        update_data = await request.json()
        logger.info(f"Received update: {update_data}")
        
        if bot_service:
            await bot_service.process_update(update_data)
        
        return {"ok": True}
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return {"ok": False, "error": str(e)}

@app.get("/api/dashboard/overview")
def get_dashboard_overview():
    db = SessionLocal()
    try:
        total_users = db.query(User).count()
        total_transactions = db.query(Transaction).count()
        total_logs = db.query(BotLog).count()
        
        return {
            "total_users": total_users,
            "total_transactions": total_transactions,
            "total_logs": total_logs,
            "bot_status": "active"
        }
    finally:
        db.close()
