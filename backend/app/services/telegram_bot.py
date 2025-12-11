from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from sqlalchemy.orm import Session
from datetime import datetime
import pytz
from ..config import settings
from ..models.user import User
from ..models.transaction import Transaction, TransactionType
from ..models.bot_log import BotLog, LogLevel
from .llm_service import llm_service
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBotService:
    def __init__(self, db_session_factory):
        self.db_session_factory = db_session_factory
        self.application = None
    
    def get_or_create_user(self, db: Session, telegram_user) -> User:
        user = db.query(User).filter(User.telegram_id == str(telegram_user.id)).first()
        if not user:
            user = User(
                telegram_id=str(telegram_user.id),
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    
    def log_interaction(self, db: Session, user_id: int, user_input: str, bot_response: str, level: LogLevel = LogLevel.INFO):
        log = BotLog(
            user_id=user_id,
            level=level,
            message="User interaction",
            user_input=user_input,
            bot_response=bot_response
        )
        db.add(log)
        db.commit()
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        db = self.db_session_factory()
        try:
            user = self.get_or_create_user(db, update.effective_user)
            
            message = """
🤖 *Selamat datang di CuanBot!*

Bot akunting untuk UMKM yang memudahkan pencatatan keuangan-mu.

*Perintah:*
/start - Mulai bot
/help - Bantuan
/summary - Ringkasan keuangan
/report - Laporan lengkap

*Cara mencatat transaksi:*
Cukup chat dengan bahasa natural:
• "Terima pembayaran dari customer 500rb"
• "Bayar listrik 300 ribu"
• "Piutang si Budi 1 juta"
• "Hutang ke supplier 2 juta"

Saya akan membantu mencatat dan melacak keuangan-mu! 💰
"""
            
            await update.message.reply_text(message, parse_mode='Markdown')
            self.log_interaction(db, user.id, "/start", message)
        finally:
            db.close()
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        db = self.db_session_factory()
        try:
            user = self.get_or_create_user(db, update.effective_user)
            
            message = """
📚 *Panduan CuanBot*

*Mencatat Transaksi:*
Gunakan bahasa natural untuk mencatat:
• Pemasukan: "Dapat pembayaran 500rb dari customer A"
• Pengeluaran: "Bayar gaji karyawan 3 juta"
• Piutang: "Piutang ke Toko B sebesar 1 juta"
• Hutang: "Hutang supplier 2 juta untuk stok"

*Perintah:*
/summary - Ringkasan keuangan Anda
/report - Laporan detail
/help - Bantuan ini

*Bertanya:*
Tanyakan apapun tentang akunting, contoh:
"Bagaimana cara menghitung laba rugi?"
"Apa itu arus kas?"
"""
            
            await update.message.reply_text(message, parse_mode='Markdown')
            self.log_interaction(db, user.id, "/help", message)
        finally:
            db.close()
    
    async def summary_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        db = self.db_session_factory()
        try:
            user = self.get_or_create_user(db, update.effective_user)
            
            transactions = db.query(Transaction).filter(Transaction.user_id == user.id).all()
            
            if not transactions:
                message = "Belum ada transaksi yang tercatat. Mulai dengan mencatat transaksi Anda!"
                await update.message.reply_text(message)
                self.log_interaction(db, user.id, "/summary", message)
                return
            
            total_income = sum(t.amount for t in transactions if t.transaction_type == TransactionType.INCOME)
            total_expense = sum(t.amount for t in transactions if t.transaction_type == TransactionType.EXPENSE)
            total_receivable = sum(t.amount for t in transactions if t.transaction_type == TransactionType.RECEIVABLE)
            total_payable = sum(t.amount for t in transactions if t.transaction_type == TransactionType.PAYABLE)
            
            balance = total_income - total_expense
            
            trans_data = {
                "total_income": total_income,
                "total_expense": total_expense,
                "total_receivable": total_receivable,
                "total_payable": total_payable,
                "balance": balance,
                "transaction_count": len(transactions)
            }
            
            ai_summary = llm_service.generate_summary(trans_data)
            
            message = f"""
📊 *Ringkasan Keuangan*

💰 Total Pemasukan: Rp {total_income:,.0f}
💸 Total Pengeluaran: Rp {total_expense:,.0f}
📈 Saldo: Rp {balance:,.0f}

📝 Piutang: Rp {total_receivable:,.0f}
📝 Hutang: Rp {total_payable:,.0f}

🤖 *Analisis AI:*
{ai_summary}
"""
            
            await update.message.reply_text(message, parse_mode='Markdown')
            self.log_interaction(db, user.id, "/summary", message)
        except Exception as e:
            logger.error(f"Error in summary_command: {e}")
            await update.message.reply_text("Maaf, terjadi error saat membuat ringkasan.")
        finally:
            db.close()
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        db = self.db_session_factory()
        try:
            user = self.get_or_create_user(db, update.effective_user)
            user_message = update.message.text
            
            # Log the incoming message for debugging
            logger.info(f"Processing message from user {user.id}: {user_message[:100]}...")
            
            # Try parsing as single transaction first
            parsed = llm_service.parse_transaction(user_message)
            logger.info(f"Single parsing result: {parsed}")
            
            if "error" in parsed:
                # If single parsing fails, try multiple transaction parsing
                logger.info("Single parsing failed, trying multiple transaction parsing...")
                multi_parsed = llm_service.parse_multiple_transactions(user_message)
                logger.info(f"Multiple parsing result: {multi_parsed}")
                
                if "error" in multi_parsed:
                    logger.info(f"All parsing failed, treating as accounting question")
                    response = llm_service.answer_accounting_question(user_message)
                    await update.message.reply_text(response)
                    self.log_interaction(db, user.id, user_message, response)
                    return
                else:
                    # Handle multiple transactions
                    if multi_parsed.get("type") == "single":
                        parsed = multi_parsed["transaction"]
                    elif multi_parsed.get("type") == "multiple":
                        # Process multiple transactions
                        transactions_created = []
                        total_amount = 0
                        
                        for trans_data in multi_parsed["transactions"]:
                            try:
                                transaction_type = TransactionType[trans_data['transaction_type'].upper()]
                                transaction = Transaction(
                                    user_id=user.id,
                                    transaction_type=transaction_type,
                                    amount=float(trans_data['amount']),
                                    category=trans_data.get('category', 'Umum'),
                                    description=trans_data.get('description', ''),
                                    transaction_date=datetime.now(pytz.timezone('Asia/Jakarta'))
                                )
                                db.add(transaction)
                                transactions_created.append(trans_data)
                                total_amount += trans_data['amount']
                            except Exception as e:
                                logger.error(f"Error creating transaction: {e}")
                                continue
                        
                        if transactions_created:
                            db.commit()
                            response = f"""
✅ *{len(transactions_created)} Transaksi berhasil dicatat!*

💰 Total: Rp {total_amount:,.0f}

📋 Detail:
"""
                            for i, trans in enumerate(transactions_created, 1):
                                response += f"• {i}. {trans['transaction_type'].title()}: Rp {trans['amount']:,.0f} - {trans.get('description', '')}\n"
                            
                            await update.message.reply_text(response, parse_mode='Markdown')
                            self.log_interaction(db, user.id, user_message, response)
                            logger.info(f"{len(transactions_created)} transactions successfully recorded for user {user.id}")
                            return
                        else:
                            await update.message.reply_text("Maaf, tidak ada transaksi yang berhasil diproses.")
                            return
            
            # Handle single transaction
            if "error" not in parsed:
                # Validate transaction type
                try:
                    transaction_type = TransactionType[parsed['transaction_type'].upper()]
                except KeyError:
                    logger.error(f"Invalid transaction type: {parsed['transaction_type']}")
                    await update.message.reply_text("Maaf, tipe transaksi tidak valid. Gunakan /help untuk panduan.")
                    return
                
                transaction = Transaction(
                    user_id=user.id,
                    transaction_type=transaction_type,
                    amount=float(parsed['amount']),
                    category=parsed.get('category', 'Umum'),
                    description=parsed.get('description', ''),
                    transaction_date=datetime.now(pytz.timezone('Asia/Jakarta'))
                )
                
                db.add(transaction)
                db.commit()
                db.refresh(transaction)
                
                response = f"""
✅ *Transaksi berhasil dicatat!*

📋 Detail:
• Tipe: {parsed['transaction_type'].title()}
• Jumlah: Rp {parsed['amount']:,.0f}
• Kategori: {parsed.get('category', 'Umum')}
• Deskripsi: {parsed.get('description', '-')}
"""
                
                await update.message.reply_text(response, parse_mode='Markdown')
                self.log_interaction(db, user.id, user_message, response)
                logger.info(f"Transaction successfully recorded for user {user.id}")
            
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            
            # Provide more specific error messages
            if "API" in str(e) or "gemini" in str(e).lower():
                error_msg = "Maaf, sistem AI sedang bermasalah. Bot akan menggunakan parsing sederhana. Coba kirim pesan lagi."
            elif "database" in str(e).lower() or "connection" in str(e).lower():
                error_msg = "Maaf, ada masalah dengan database. Coba lagi dalam beberapa saat."
            else:
                error_msg = "Maaf, terjadi error. Coba lagi atau gunakan /help untuk bantuan."
            
            await update.message.reply_text(error_msg)
            self.log_interaction(db, user.id, user_message, f"Error: {str(e)}", LogLevel.ERROR)
        finally:
            db.close()
    
    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("summary", self.summary_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def initialize(self):
        self.application = Application.builder().token(settings.telegram_bot_token).build()
        self.setup_handlers()
        await self.application.initialize()
        await self.application.start()
        
        if settings.telegram_webhook_url:
            await self.application.bot.set_webhook(url=settings.telegram_webhook_url)
            logger.info(f"Webhook set to: {settings.telegram_webhook_url}")
        else:
            await self.application.updater.start_polling()
            logger.info("Bot started with polling mode")
    
    async def process_update(self, update_data: dict):
        if self.application:
            update = Update.de_json(update_data, self.application.bot)
            await self.application.process_update(update)
