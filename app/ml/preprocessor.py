import cv2
import numpy as np
from pdf2image import convert_from_path
import os
import logging

logger = logging.getLogger(__name__)

class Preprocessor:
    """
    Handles image and PDF preprocessing for OCR.
    """
    
    @staticmethod
    def _preprocess_image(image: np.ndarray) -> np.ndarray:
        """
        Applies grayscale, noise removal, and thresholding to improve OCR accuracy.
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Noise removal (blur)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Thresholding (Otsu's binarization)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh

    @staticmethod
    def process_file(file_path: str) -> list[np.ndarray]:
        """
        Processes a file (Image or PDF) and returns a list of preprocessed image arrays.
        """
        ext = os.path.splitext(file_path)[1].lower()
        processed_images = []

        try:
            if ext == '.pdf':
                # Convert PDF to images
                images = convert_from_path(file_path)
                for img in images:
                    # Convert PIL image to OpenCV format (BGR)
                    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                    processed_images.append(Preprocessor._preprocess_image(img_cv))
            else:
                # Read image with OpenCV
                img = cv2.imread(file_path)
                if img is None:
                    raise ValueError(f"Failed to read image at {file_path}")
                processed_images.append(Preprocessor._preprocess_image(img))
        except Exception as e:
            logger.error(f"Error preprocessing file {file_path}: {e}")
            raise

        return processed_images
