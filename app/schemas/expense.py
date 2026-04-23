from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Dict

class ExpenseResponse(BaseModel):
    id: str
    vendor: Optional[str]
    amount: Optional[float]
    date: Optional[datetime]
    category: str
    confidence: Optional[Dict] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class ExpenseUpdateRequest(BaseModel):
    vendor: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    date: Optional[datetime] = None
    category: Optional[str] = None

class AnalyticsResponse(BaseModel):
    total_spent: float
    expense_count: int
    category_breakdown: Dict[str, float]
