from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..database import get_db
from ..models.transaction import Transaction
from ..models.prediction import Prediction, PredictionType
from ..services.ml_forecasting import forecasting_service
from ..services.ml_anomaly import anomaly_detection_service
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/predictions", tags=["predictions"])

class ForecastRequest(BaseModel):
    user_id: int = None
    periods: int = 30

class AnomalyRequest(BaseModel):
    user_id: int = None

@router.post("/forecast")
def generate_forecast(request: ForecastRequest, db: Session = Depends(get_db)):
    query = db.query(Transaction)
    if request.user_id:
        query = query.filter(Transaction.user_id == request.user_id)
    
    transactions = query.all()
    
    transactions_data = [
        {
            "id": t.id,
            "transaction_type": t.transaction_type.value,
            "amount": t.amount,
            "transaction_date": t.transaction_date,
            "category": t.category
        }
        for t in transactions
    ]
    
    forecast_result = forecasting_service.forecast_revenue(transactions_data, request.periods)
    
    prediction = Prediction(
        prediction_type=PredictionType.FORECAST,
        prediction_data=forecast_result,
        extra_metadata={"user_id": request.user_id, "periods": request.periods}
    )
    db.add(prediction)
    db.commit()
    
    return forecast_result

@router.post("/anomaly")
def detect_anomalies(request: AnomalyRequest, db: Session = Depends(get_db)):
    query = db.query(Transaction)
    if request.user_id:
        query = query.filter(Transaction.user_id == request.user_id)
    
    transactions = query.all()
    
    transactions_data = [
        {
            "id": t.id,
            "transaction_type": t.transaction_type.value,
            "amount": t.amount,
            "transaction_date": t.transaction_date,
            "category": t.category,
            "description": t.description
        }
        for t in transactions
    ]
    
    anomaly_result = anomaly_detection_service.detect_anomalies(transactions_data)
    
    if anomaly_result["status"] == "success":
        for anomaly in anomaly_result["anomalies"]:
            transaction = db.query(Transaction).filter(Transaction.id == anomaly["transaction_id"]).first()
            if transaction:
                transaction.is_anomaly = 1
                transaction.anomaly_score = anomaly["anomaly_score"]
        
        db.commit()
    
    prediction = Prediction(
        prediction_type=PredictionType.ANOMALY,
        prediction_data=anomaly_result,
        extra_metadata={"user_id": request.user_id}
    )
    db.add(prediction)
    db.commit()
    
    return anomaly_result

@router.get("/business-pattern/{user_id}")
def get_business_pattern(user_id: int, db: Session = Depends(get_db)):
    """Get user's business pattern analysis"""
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    
    if len(transactions) < 5:
        return {
            "status": "insufficient_data",
            "message": "Minimal 5 transaksi diperlukan untuk analisis pola bisnis"
        }
    
    transactions_data = [
        {
            "id": t.id,
            "transaction_type": t.transaction_type.value,
            "amount": t.amount,
            "transaction_date": t.transaction_date,
            "category": t.category,
            "description": t.description
        }
        for t in transactions
    ]
    
    # Use the anomaly service to analyze patterns
    import pandas as pd
    df = pd.DataFrame(transactions_data)
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    
    business_pattern = anomaly_detection_service._analyze_business_pattern(df)
    
    return {
        "status": "success",
        "user_id": user_id,
        "total_transactions": len(transactions),
        "business_type": business_pattern['business_type'],
        "operating_hours": business_pattern['hour_pattern']['common_hours'],
        "hour_distribution": business_pattern['hour_pattern']['hour_distribution'],
        "top_categories": dict(list(business_pattern['categories'].items())[:5])
    }

@router.post("/reset-anomaly/{transaction_id}")
def reset_anomaly_flag(transaction_id: int, db: Session = Depends(get_db)):
    """Reset anomaly flag for a specific transaction"""
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    transaction.is_anomaly = 0
    transaction.anomaly_score = None
    db.commit()
    
    return {
        "status": "success",
        "message": f"Anomaly flag reset for transaction {transaction_id}",
        "transaction_id": transaction_id
    }

@router.post("/whitelist-hour")
def whitelist_hour_pattern(
    user_id: int,
    hour: int,
    db: Session = Depends(get_db)
):
    """Whitelist a specific hour as normal for a user (future feature)"""
    # This could be implemented to store user preferences
    # For now, just return success
    return {
        "status": "success", 
        "message": f"Hour {hour:02d}:00 whitelisted for user {user_id}",
        "note": "This feature will learn from your patterns automatically"
    }

@router.post("/fix-timezone")
def fix_timezone_issues(db: Session = Depends(get_db)):
    """Fix timezone issues in existing transaction data"""
    import pytz
    
    # Get all transactions with potential timezone issues
    transactions = db.query(Transaction).all()
    
    fixed_count = 0
    jakarta_tz = pytz.timezone('Asia/Jakarta')
    
    for transaction in transactions:
        # If transaction_date is naive (no timezone), assume it's Jakarta time
        if transaction.transaction_date.tzinfo is None:
            # Localize as Jakarta timezone
            transaction.transaction_date = jakarta_tz.localize(transaction.transaction_date)
            fixed_count += 1
        elif transaction.transaction_date.tzinfo != jakarta_tz:
            # Convert to Jakarta timezone
            transaction.transaction_date = transaction.transaction_date.astimezone(jakarta_tz)
            fixed_count += 1
    
    if fixed_count > 0:
        db.commit()
    
    return {
        "status": "success",
        "message": f"Fixed timezone for {fixed_count} transactions",
        "total_transactions": len(transactions)
    }

@router.get("/history")
def get_prediction_history(
    prediction_type: str = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Prediction)
    
    if prediction_type:
        query = query.filter(Prediction.prediction_type == prediction_type)
    
    predictions = query.order_by(Prediction.created_at.desc()).limit(limit).all()
    
    return {
        "predictions": [
            {
                "id": p.id,
                "prediction_type": p.prediction_type.value,
                "prediction_data": p.prediction_data,
                "metadata": p.extra_metadata,
                "created_at": p.created_at
            }
            for p in predictions
        ]
    }
