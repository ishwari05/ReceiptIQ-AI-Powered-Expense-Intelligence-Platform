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
            # Added support for currency codes (AED, USD, etc.) and symbols
            pattern = rf'{keyword}[\s\:\$A-Z]*([\d\s\.\,]+\d{{2}})'
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                # 1. Remove all whitespace
                clean_m = re.sub(r'\s+', '', m)
                
                # 2. Handle thousands separators (e.g., 30,000.00)
                # If there's a comma AND a dot, the comma is likely a thousands separator
                if ',' in clean_m and '.' in clean_m:
                    clean_m = clean_m.replace(',', '')
                # If there is ONLY a comma followed by 2 digits, it's likely a decimal (European style)
                elif ',' in clean_m and len(clean_m.split(',')[-1]) == 2:
                    clean_m = clean_m.replace(',', '.')
                
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
        """
        Robustly extracts dates from cleaned text using multiple regex patterns
        and fallback formats.
        """
        # 1. Regex for common date formats (/, -, .)
        date_patterns = [
            r'\b(\d{1,4}[\/\-\.]\d{1,2}[\/\-\.]\d{1,4})\b',
            r'\b([A-Z]{3,9}\s+\d{1,2},?\s+\d{4})\b', # OCT 27, 2023
            r'\b(\d{1,2},?\s+[A-Z]{3,9},?\s+\d{4})\b', # 12 SEP, 2024
        ]
        
        found_dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for date_str in matches:
                # Normalize: remove commas and replace dots with slashes
                clean_date = date_str.replace(',', '').replace('.', '/')
                
                # Try various format strings
                formats = (
                    '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d', 
                    '%m/%d/%y', '%d/%m/%y', '%Y-%m-%d',
                    '%b %d %Y', '%B %d %Y', '%d %b %Y', '%d %B %Y',
                    '%m-%d-%Y', '%d-%m-%Y'
                )
                
                for fmt in formats:
                    try:
                        dt = datetime.strptime(clean_date, fmt)
                        # Sanity check: Date shouldn't be in the far future or too far past
                        if 1990 < dt.year < 2100:
                            found_dates.append(dt)
                            break
                    except ValueError:
                        continue
        
        if found_dates:
            # Usually the first date found is the transaction date
            return found_dates[0]
            
        return None

    @staticmethod
    def categorize_expense(vendor: Optional[str], text: str) -> str:
        """
        Simple keyword-based categorization engine.
        """
        text_lower = (text + " " + (vendor or "")).lower()
        
        categories = {
            "Food & Beverage": ["starbucks", "mcdonald", "restaurant", "cafe", "coffee", "burger", "pizza", "dunkin", "subway", "eats"],
            "Shopping & Supplies": ["amazon", "walmart", "target", "staples", "office", "grocery", "market", "store", "mall"],
            "Transportation": ["uber", "lyft", "shell", "chevron", "gas", "fuel", "parking", "train", "metro", "airline"],
            "Utilities": ["electric", "water", "internet", "comcast", "verizon", "mobile", "phone", "insurance"],
            "Entertainment": ["netflix", "spotify", "cinema", "movie", "ticket", "event", "game"]
        }
        
        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
                
        return "uncategorized"

    @staticmethod
    def extract_all(cleaned_text: str) -> dict:
        vendor = Extractor.extract_vendor(cleaned_text)
        amount = Extractor.extract_amount(cleaned_text)
        date = Extractor.extract_date(cleaned_text)
        
        return {
            "vendor": vendor,
            "amount": amount,
            "date": date,
            "category": Extractor.categorize_expense(vendor, cleaned_text)
        }
