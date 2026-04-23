from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class ReceiptBase(BaseModel):
    vendor: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None

class ReceiptResponse(ReceiptBase):
    id: str
    file_path: str
    confidence: Optional[Dict[str, Any]] = None
    status: str = "success"

    model_config = ConfigDict(from_attributes=True)
