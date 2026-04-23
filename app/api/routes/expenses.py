from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.expense_service import ExpenseService
from app.schemas.expense import ExpenseResponse, ExpenseUpdateRequest, AnalyticsResponse
from app.core.dependencies import get_current_user
from app.db.models import User
from typing import List, Optional
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[ExpenseResponse])
async def get_expenses(
    category: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    vendor: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Fetch user's expenses with optional filtering, sorting, and pagination (Protected).
    """
    return await ExpenseService.get_expenses(
        db, current_user.id, category, start_date, end_date, min_amount, max_amount, vendor, limit, offset
    )

@router.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user-specific spending analytics and category breakdown (Protected).
    """
    return await ExpenseService.get_analytics(db, current_user.id)

@router.get("/{id}", response_model=ExpenseResponse)
async def get_expense(
    id: str = Path(..., description="The ID of the expense to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed information for a specific expense (Protected).
    """
    return await ExpenseService.get_expense_by_id(db, id, current_user.id)

@router.put("/{id}", response_model=ExpenseResponse)
async def update_expense(
    data: ExpenseUpdateRequest,
    id: str = Path(..., description="The ID of the expense to update"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Partially update an existing expense's data (Protected).
    """
    return await ExpenseService.update_expense(db, id, current_user.id, data)

@router.delete("/{id}", status_code=204)
async def delete_expense(
    id: str = Path(..., description="The ID of the expense to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Permanently delete an expense record (Protected).
    """
    await ExpenseService.delete_expense(db, id, current_user.id)
    return None
