from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth as firebase_auth
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.db.models import User
import logging
from app.core import firebase # Ensure firebase is initialized

logger = logging.getLogger(__name__)
security = HTTPBearer()

async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency that verifies the Firebase ID token and returns the corresponding User from the DB.
    If the user doesn't exist in the local DB yet, it creates one.
    """
    try:
        # 1. Verify Firebase Token
        decoded_token = firebase_auth.verify_id_token(token.credentials)
        firebase_uid = decoded_token['uid']
        email = decoded_token.get('email', 'no-email@provided.com')

        # 2. Check if user exists in internal DB
        query = select(User).where(User.firebase_uid == firebase_uid)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        # 3. Auto-Create User if first time
        if not user:
            logger.info(f"Creating new internal user for firebase_uid: {firebase_uid}")
            user = User(firebase_uid=firebase_uid, email=email)
            db.add(user)
            await db.commit()
            await db.refresh(user)

        return user

    except Exception as e:
        logger.error(f"Auth error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
