import re
from datetime import datetime
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class Extractor:
    """
    Extracts fields (vendor, amount, date) from cleaned text.
    """
    
    @staticmethod
    def extract_vendor(text: str) -> Optional[str]:
        # Simple heuristic: first line is often the vendor
        lines = text.split('\n')
        for line in lines:
            clean_line = line.strip()
            # Ignore empty lines or lines with only numbers/symbols
            if len(clean_line) > 2 and re.search(r'[a-z]', clean_line):
                return clean_line
        return None

    @staticmethod
    def extract_amount(text: str) -> Optional[float]:
        """
        Robustly extracts the total amount, handling common OCR artifacts
        like spaces in numbers (1 0. 00) or commas as decimals (10,00).
        """
        # Look for lines containing keywords
        keywords = ['total', 'amount', 'sum', 'due', 'payable', 'balance', 'net']
        
        found_amounts = []
        
        # 1. Try keyword-based extraction
        # Pattern: keyword followed by symbols/spaces and then a number with 2 decimals
        for keyword in keywords:
            # This regex allows spaces between digits and symbols
            pattern = rf'{keyword}[\s\:\$]*([\d\s\.\,]+\d{{2}})'
            matches = re.findall(pattern, text)
            for m in matches:
                # Normalize: remove spaces, replace comma with dot
                clean_m = re.sub(r'\s+', '', m).replace(',', '.')
                try:
                    val = float(clean_m)
                    # Simple heuristic: ignore very large numbers that might be phone numbers or dates
                    if 0.01 < val < 1000000:
                        found_amounts.append(val)
                except ValueError:
                    continue

        if found_amounts:
            # If we found multiple, the last one near a keyword is often the Grand Total
            return found_amounts[-1]

        # 2. Fallback: find any currency-looking pattern in the whole text
        # Look for any digit sequence ending in .XX or ,XX
        all_matches = re.findall(r'([\d\s\.\,]+\d{2})', text)
        for m in all_matches:
            clean_m = re.sub(r'\s+', '', m).replace(',', '.')
            try:
                val = float(clean_m)
                # Avoid common years (like 2023)
                if val != 2023 and val != 2024 and val != 2025:
                    found_amounts.append(val)
            except ValueError:
                continue
        
        if found_amounts:
            return max(found_amounts)
            
        return None

    @staticmethod
    def extract_date(text: str) -> Optional[datetime]:
        # Regex for common date formats
        date_patterns = [
            r'\b(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})\b',
        ]
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            if matches:
                # Take the first matched date
                date_str = matches[0]
                for fmt in ('%m/%d/%Y', '%m-%d-%Y', '%Y-%m-%d', '%m/%d/%y', '%d/%m/%Y'):
                    try:
                        return datetime.strptime(date_str, fmt)
                    except ValueError:
                        continue
        return None

    @staticmethod
    def extract_all(cleaned_text: str) -> dict:
        return {
            "vendor": Extractor.extract_vendor(cleaned_text),
            "amount": Extractor.extract_amount(cleaned_text),
            "date": Extractor.extract_date(cleaned_text)
        }
