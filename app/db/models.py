from sqlalchemy import Column, String, Float, DateTime, Text, JSON, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    firebase_uid = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to receipts
    receipts = relationship("Receipt", back_populates="owner")

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
    category = Column(String, nullable=False, server_default="uncategorized")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Link to User
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    
    # Relationship back to User
    owner = relationship("User", back_populates="receipts")
