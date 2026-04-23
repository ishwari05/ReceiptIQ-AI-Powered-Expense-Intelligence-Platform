import re

class Cleaner:
    """
    Cleans and normalizes OCR text.
    """
    
    @staticmethod
    def clean_text(raw_text: str) -> str:
        """
        Normalizes text and fixes common OCR errors.
        """
        if not raw_text:
            return ""
            
        # Lowercase normalization
        text = raw_text.lower()
        
        # Fix common OCR errors for numbers
        # Replace 'o' with '0' when surrounded by digits
        text = re.sub(r'(?<=\d)o|o(?=\d)', '0', text)
        # Replace 'l' with '1' when surrounded by digits
        text = re.sub(r'(?<=\d)l|l(?=\d)', '1', text)

        # Remove special characters except common receipt ones (e.g. $, ., /, -, :, comma, newline)
        text = re.sub(r'[^a-z0-9\s\.\,\$\/\-\:\n]', '', text)
        
        # Remove extra whitespace but retain newlines
        text = re.sub(r'[^\S\n]+', ' ', text).strip()
        
        return text
