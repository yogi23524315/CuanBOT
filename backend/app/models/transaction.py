from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import enum

class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    RECEIVABLE = "receivable"
    PAYABLE = "payable"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transaction_type = Column(SQLEnum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    transaction_date = Column(DateTime(timezone=True), nullable=False)
    is_anomaly = Column(Integer, default=0)
    anomaly_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="transactions")
