from datetime import datetime

class Validator:
    """
    Validates extracted data and calculates confidence scores.
    """
    
    @staticmethod
    def validate(extracted_data: dict) -> tuple[dict, dict, dict, str]:
        """
        Returns (validated_data, validation_flags, confidences, status)
        """
        validated_data = extracted_data.copy()
        flags = {
            "is_valid_amount": False,
            "is_valid_date": False,
            "has_vendor": False
        }
        confidences = {
            "amount": 0.0,
            "date": 0.0,
            "vendor": 0.0
        }

        # Validate amount
        if validated_data.get("amount") is not None and validated_data["amount"] > 0:
            flags["is_valid_amount"] = True
            confidences["amount"] = 0.90  # Mock confidence score
        
        # Validate date
        if validated_data.get("date") is not None and isinstance(validated_data["date"], datetime):
            flags["is_valid_date"] = True
            confidences["date"] = 0.85
        
        # Validate vendor
        if validated_data.get("vendor"):
            flags["has_vendor"] = True
            confidences["vendor"] = 0.75
            
        # Overall status
        status = "success" if all(flags.values()) else "partial_success"
        
        return validated_data, flags, confidences, status
