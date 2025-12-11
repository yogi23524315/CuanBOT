from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from datetime import datetime, timedelta
from ..database import get_db
from ..models.transaction import Transaction, TransactionType
from ..models.user import User
from pydantic import BaseModel

router = APIRouter(prefix="/api/transactions", tags=["transactions"])

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    transaction_type: str
    amount: float
    category: Optional[str]
    description: Optional[str]
    transaction_date: datetime
    is_anomaly: int
    anomaly_score: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True

class TransactionStats(BaseModel):
    total_income: float  # Total Penjualan
    hpp: float  # HPP / Bahan Baku
    gross_profit: float  # Laba Kotor = Income - HPP
    operational_expense: float  # Pengeluaran Operasional (excluding HPP)
    net_profit: float  # Laba Bersih = Gross Profit - Operational Expense
    cash_balance: float  # Saldo Kas
    total_receivable: float
    total_payable: float
    transaction_count: int

@router.get("/", response_model=List[TransactionResponse])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    transaction_type: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)
    
    if user_id:
        query = query.filter(Transaction.user_id == user_id)
    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)
    
    transactions = query.order_by(Transaction.transaction_date.desc()).offset(skip).limit(limit).all()
    return transactions

@router.get("/stats", response_model=TransactionStats)
def get_transaction_stats(
    user_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)
    
    if user_id:
        query = query.filter(Transaction.user_id == user_id)
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date <= end_date)
    
    transactions = query.all()
    
    total_income = sum(t.amount for t in transactions if t.transaction_type == TransactionType.INCOME)
    total_expense = sum(t.amount for t in transactions if t.transaction_type == TransactionType.EXPENSE)
    total_receivable = sum(t.amount for t in transactions if t.transaction_type == TransactionType.RECEIVABLE)
    total_payable = sum(t.amount for t in transactions if t.transaction_type == TransactionType.PAYABLE)
    
    # Calculate HPP (Cost of Goods Sold) from expenses with specific categories
    hpp_categories = ['COGS', 'Bahan Baku', 'HPP', 'Cost of Goods Sold']
    hpp = sum(t.amount for t in transactions 
              if t.transaction_type == TransactionType.EXPENSE 
              and t.category and any(cat.lower() in t.category.lower() for cat in hpp_categories))
    
    # Calculate Operational Expenses (excluding HPP)
    operational_expense = total_expense - hpp
    
    # Calculate profit metrics
    gross_profit = total_income - hpp  # Laba Kotor = Pemasukan - HPP
    net_profit = gross_profit - operational_expense  # Laba Bersih = Laba Kotor - Operational Expense
    cash_balance = total_income - total_expense  # Saldo Kas
    
    return TransactionStats(
        total_income=total_income,
        hpp=hpp,
        gross_profit=gross_profit,
        operational_expense=operational_expense,
        net_profit=net_profit,
        cash_balance=cash_balance,
        total_receivable=total_receivable,
        total_payable=total_payable,
        transaction_count=len(transactions)
    )

@router.get("/daily")
def get_daily_transactions(
    days: int = 30,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    start_date = datetime.now() - timedelta(days=days)
    
    query = db.query(
        func.date(Transaction.transaction_date).label('date'),
        Transaction.transaction_type,
        func.sum(Transaction.amount).label('total')
    ).filter(Transaction.transaction_date >= start_date)
    
    if user_id:
        query = query.filter(Transaction.user_id == user_id)
    
    results = query.group_by(
        func.date(Transaction.transaction_date),
        Transaction.transaction_type
    ).all()
    
    daily_data = {}
    for result in results:
        date_str = str(result.date)
        if date_str not in daily_data:
            daily_data[date_str] = {"date": date_str, "income": 0, "expense": 0}
        
        if result.transaction_type == TransactionType.INCOME:
            daily_data[date_str]["income"] = float(result.total)
        elif result.transaction_type == TransactionType.EXPENSE:
            daily_data[date_str]["expense"] = float(result.total)
    
    return {"data": list(daily_data.values())}

@router.get("/by-category")
def get_transactions_by_category(
    user_id: Optional[int] = None,
    transaction_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label('total'),
        func.count(Transaction.id).label('count')
    )
    
    if user_id:
        query = query.filter(Transaction.user_id == user_id)
    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)
    
    results = query.group_by(Transaction.category).all()
    
    return {
        "data": [
            {
                "category": r.category or "Uncategorized",
                "total": float(r.total),
                "count": r.count
            }
            for r in results
        ]
    }

@router.delete("/reset")
def reset_all_transactions(
    confirm: bool = Query(False, description="Must be true to confirm deletion"),
    db: Session = Depends(get_db)
):
    """Delete all transactions from database. Requires confirmation."""
    if not confirm:
        raise HTTPException(
            status_code=400,
            detail="Confirmation required. Set confirm=true to delete all data."
        )
    
    try:
        # Delete all transactions
        deleted_count = db.query(Transaction).delete()
        db.commit()
        
        return {
            "status": "success",
            "message": f"Successfully deleted {deleted_count} transactions",
            "deleted_count": deleted_count
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error resetting data: {str(e)}")

@router.post("/generate-sample")
def generate_sample_data(db: Session = Depends(get_db)):
    """Generate 30 days of sample transaction data for UMKM Kuliner."""
    import random
    from datetime import datetime, timedelta
    
    try:
        # Get or create default user
        user = db.query(User).first()
        if not user:
            user = User(
                telegram_id="sample_user",
                username="sample",
                first_name="Sample",
                last_name="User"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        transactions = []
        start_date = datetime.now() - timedelta(days=30)
        
        # Categories for UMKM Kuliner
        income_categories = ["Penjualan"]
        
        # HPP / Bahan Baku categories (Cost of Goods Sold)
        hpp_categories = ["Bahan Baku", "HPP"]
        
        # Operational expense categories (excluding HPP)
        operational_categories = [
            "Gas", "Listrik", "Kemasan", "Transportasi", 
            "Gaji", "Sewa", "Operasional"
        ]
        
        for day in range(30):
            current_date = start_date + timedelta(days=day)
            
            # Generate 3-8 income transactions per day (penjualan kuliner)
            for _ in range(random.randint(3, 8)):
                amount = random.randint(30000, 350000)
                transactions.append(Transaction(
                    user_id=user.id,
                    transaction_type=TransactionType.INCOME,
                    amount=amount,
                    category="Penjualan",
                    description=f"Penjualan menu hari {day + 1}",
                    transaction_date=current_date + timedelta(hours=random.randint(8, 20)),
                    is_anomaly=0
                ))
            
            # Generate 1-2 HPP/Bahan Baku transactions per day
            for _ in range(random.randint(1, 2)):
                amount = random.randint(80000, 250000)
                transactions.append(Transaction(
                    user_id=user.id,
                    transaction_type=TransactionType.EXPENSE,
                    amount=amount,
                    category="Bahan Baku",
                    description=f"Pembelian bahan baku - {current_date.strftime('%d/%m/%Y')}",
                    transaction_date=current_date + timedelta(hours=random.randint(6, 10)),
                    is_anomaly=0
                ))
            
            # Generate 2-4 operational expense transactions per day
            for _ in range(random.randint(2, 4)):
                category = random.choice(operational_categories)
                
                # Different amount ranges based on category
                if category == "Gas":
                    amount = random.randint(15000, 50000)
                elif category == "Listrik":
                    amount = random.randint(20000, 80000)
                elif category == "Kemasan":
                    amount = random.randint(10000, 40000)
                elif category == "Transportasi":
                    amount = random.randint(15000, 60000)
                elif category == "Gaji":
                    amount = random.randint(50000, 150000)
                elif category == "Sewa":
                    amount = random.randint(100000, 300000)
                else:  # Operasional
                    amount = random.randint(20000, 80000)
                
                transactions.append(Transaction(
                    user_id=user.id,
                    transaction_type=TransactionType.EXPENSE,
                    amount=amount,
                    category=category,
                    description=f"{category} - {current_date.strftime('%d/%m/%Y')}",
                    transaction_date=current_date + timedelta(hours=random.randint(9, 18)),
                    is_anomaly=0
                ))
        
        # Add all transactions to database
        db.add_all(transactions)
        db.commit()
        
        return {
            "status": "success",
            "message": f"Successfully generated {len(transactions)} sample transactions for 30 days",
            "transaction_count": len(transactions)
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating sample data: {str(e)}")
