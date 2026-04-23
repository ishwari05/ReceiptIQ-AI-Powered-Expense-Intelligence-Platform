import os
import uuid
import logging
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.db.models import Receipt
from app.ml.preprocessor import Preprocessor
from app.ml.ocr_engine import OCREngine
from app.ml.cleaner import Cleaner
from app.ml.extractor import Extractor
from app.ml.validator import Validator

logger = logging.getLogger(__name__)

class ReceiptService:
    @staticmethod
    async def process_receipt(file: UploadFile, db: AsyncSession, user_id: str) -> dict:
        """
        Full pipeline: save_file -> preprocess -> OCR -> clean -> extract -> validate -> store
        """
        # 1. Save file
        ext = os.path.splitext(file.filename)[1].lower() if file.filename else ".jpg"
        file_id = str(uuid.uuid4())
        file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{ext}")
        
        try:
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
                
            # 2. Preprocess
            images = Preprocessor.process_file(file_path)
            
            # 3. OCR
            ocr_result = OCREngine.extract(images)
            raw_text = ocr_result["raw_text"]
            
            # 4. Clean Text
            cleaned_text = Cleaner.clean_text(raw_text)
            
            # 5. Extract Fields
            extracted_data = Extractor.extract_all(cleaned_text)
            
            # 6. Validate
            validated_data, flags, confidences, status = Validator.validate(extracted_data)
            
            # 7. Store
            db_receipt = Receipt(
                id=file_id,
                file_path=file_path,
                vendor=validated_data.get("vendor"),
                amount=validated_data.get("amount"),
                date=validated_data.get("date"),
                category=validated_data.get("category", "uncategorized"), # SAVE CATEGORY
                raw_text=raw_text,
                confidence=confidences,
                user_id=user_id # LINK TO USER
            )
            db.add(db_receipt)
            await db.commit()
            await db.refresh(db_receipt)
            
            return {
                "id": db_receipt.id,
                "vendor": db_receipt.vendor,
                "amount": db_receipt.amount,
                "date": db_receipt.date,
                "confidence": confidences,
                "status": status,
                "file_path": db_receipt.file_path
            }
            
        except Exception as e:
            logger.error(f"Error processing receipt: {e}")
            raise e
