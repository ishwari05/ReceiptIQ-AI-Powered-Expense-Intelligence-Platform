from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.receipt_service import ReceiptService
from app.schemas.receipt import ReceiptResponse
from app.core.dependencies import get_current_user
from app.db.models import User

router = APIRouter()

@router.post("/upload_receipt", response_model=ReceiptResponse)
async def upload_receipt(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a receipt image/PDF and extract structured expense data (Protected).
    """
    # Quick content type validation
    if not file.content_type.startswith("image/") and file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be an image or PDF")
        
    try:
        result = await ReceiptService.process_receipt(file, db, current_user.id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
