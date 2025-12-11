from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..database import get_db
from ..models.bot_log import BotLog, LogLevel
from pydantic import BaseModel

router = APIRouter(prefix="/api/bot-logs", tags=["bot-logs"])

class BotLogResponse(BaseModel):
    id: int
    user_id: Optional[int]
    level: str
    message: str
    user_input: Optional[str]
    bot_response: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[BotLogResponse])
def get_bot_logs(
    skip: int = 0,
    limit: int = 100,
    level: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(BotLog)
    
    if level:
        query = query.filter(BotLog.level == level)
    if user_id:
        query = query.filter(BotLog.user_id == user_id)
    
    logs = query.order_by(BotLog.created_at.desc()).offset(skip).limit(limit).all()
    return logs

@router.get("/stats")
def get_bot_stats(db: Session = Depends(get_db)):
    total_logs = db.query(BotLog).count()
    error_logs = db.query(BotLog).filter(BotLog.level == LogLevel.ERROR).count()
    
    return {
        "total_interactions": total_logs,
        "error_count": error_logs,
        "success_rate": ((total_logs - error_logs) / total_logs * 100) if total_logs > 0 else 0
    }

