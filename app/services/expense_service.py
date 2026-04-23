from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func, and_
from app.db.models import Receipt
from app.schemas.expense import ExpenseUpdateRequest
from fastapi import HTTPException
from typing import Optional, List
from datetime import datetime

class ExpenseService:
    @staticmethod
    async def get_expenses(
        db: AsyncSession,
        user_id: str,
        category: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        vendor: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Receipt]:
        # Always filter by user_id
        query = select(Receipt).where(Receipt.user_id == user_id)
        
        filters = []
        if category:
            filters.append(Receipt.category == category)
        if start_date:
            filters.append(Receipt.date >= start_date)
        if end_date:
            filters.append(Receipt.date <= end_date)
        if min_amount:
            filters.append(Receipt.amount >= min_amount)
        if max_amount:
            filters.append(Receipt.amount <= max_amount)
        if vendor:
            filters.append(Receipt.vendor.ilike(f"%{vendor}%"))
            
        if filters:
            query = query.where(and_(*filters))
            
        query = query.order_by(Receipt.date.desc()).offset(offset).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_expense_by_id(db: AsyncSession, expense_id: str, user_id: str) -> Receipt:
        # Filter by both id and user_id to ensure ownership
        query = select(Receipt).where(and_(Receipt.id == expense_id, Receipt.user_id == user_id))
        result = await db.execute(query)
        expense = result.scalar_one_or_none()
        
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found or unauthorized")
        return expense

    @staticmethod
    async def update_expense(db: AsyncSession, expense_id: str, user_id: str, data: ExpenseUpdateRequest) -> Receipt:
        expense = await ExpenseService.get_expense_by_id(db, expense_id, user_id)
        
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return expense
            
        for key, value in update_data.items():
            setattr(expense, key, value)
            
        await db.commit()
        await db.refresh(expense)
        return expense

    @staticmethod
    async def delete_expense(db: AsyncSession, expense_id: str, user_id: str):
        expense = await ExpenseService.get_expense_by_id(db, expense_id, user_id)
        await db.delete(expense)
        await db.commit()

    @staticmethod
    async def get_analytics(db: AsyncSession, user_id: str) -> dict:
        # Total spent and count scoped to user
        stats_query = select(
            func.sum(Receipt.amount).label("total_spent"),
            func.count(Receipt.id).label("expense_count")
        ).where(Receipt.user_id == user_id)
        
        stats_result = await db.execute(stats_query)
        stats = stats_result.one()
        
        # Category breakdown scoped to user
        category_query = select(
            Receipt.category,
            func.sum(Receipt.amount).label("total")
        ).where(Receipt.user_id == user_id).group_by(Receipt.category)
        
        category_result = await db.execute(category_query)
        
        breakdown = {row.category: float(row.total or 0) for row in category_result.all()}
        
        return {
            "total_spent": float(stats.total_spent or 0),
            "expense_count": stats.expense_count,
            "category_breakdown": breakdown
        }
