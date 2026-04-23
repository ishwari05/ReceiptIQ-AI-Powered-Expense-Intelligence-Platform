import pytesseract
import numpy as np
import logging

logger = logging.getLogger(__name__)

class OCREngine:
    """
    Extracts text and bounding box data using Tesseract OCR.
    """
    
    @staticmethod
    def extract(images: list[np.ndarray]) -> dict:
        """
        Extracts raw text and structured data (bounding boxes) from images.
        """
        full_text = ""
        structured_data = []

        try:
            for idx, img in enumerate(images):
                # Extract raw text
                text = pytesseract.image_to_string(img)
                full_text += text + "\n"
                
                # Extract structured data (bounding boxes, confidences)
                data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
                data['page_num'] = [idx + 1] * len(data['text'])
                structured_data.append(data)
                
            return {
                "raw_text": full_text.strip(),
                "structured_data": structured_data
            }
        except Exception as e:
            logger.error(f"Error during OCR extraction: {e}")
            raise
