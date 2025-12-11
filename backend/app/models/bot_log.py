from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import enum

class LogLevel(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    DEBUG = "debug"

class BotLog(Base):
    __tablename__ = "bot_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    level = Column(SQLEnum(LogLevel), default=LogLevel.INFO)
    message = Column(Text, nullable=False)
    user_input = Column(Text, nullable=True)
    bot_response = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="bot_logs")
