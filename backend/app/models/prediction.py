from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from ..database import Base
import enum

class PredictionType(str, enum.Enum):
    FORECAST = "forecast"
    ANOMALY = "anomaly"

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    prediction_type = Column(SQLEnum(PredictionType), nullable=False)
    prediction_data = Column(JSON, nullable=False)
    extra_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
