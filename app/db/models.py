from sqlalchemy import Column, String, Float, DateTime, Text, JSON, func
from app.db.database import Base
import uuid

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    file_path = Column(String, nullable=False)
    vendor = Column(String, nullable=True)
    amount = Column(Float, nullable=True)
    date = Column(DateTime, nullable=True)
    raw_text = Column(Text, nullable=True)
    confidence = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
