import firebase_admin
from firebase_admin import credentials
import os
import json
import logging

logger = logging.getLogger(__name__)

# Path to your service account JSON
# In production, you would use environment variables
service_account_path = "firebase-service-account.json"

def initialize_firebase():
    if not firebase_admin._apps:
        try:
            if os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase Admin initialized using service account JSON.")
            else:
                # Fallback for environment variables (Production/CI)
                cred_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")
                if cred_json:
                    cred_dict = json.loads(cred_json)
                    cred = credentials.Certificate(cred_dict)
                    firebase_admin.initialize_app(cred)
                    logger.info("Firebase Admin initialized using environment variables.")
                else:
                    logger.warning("Firebase Service Account JSON not found. Auth will fail.")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase Admin: {e}")

initialize_firebase()
