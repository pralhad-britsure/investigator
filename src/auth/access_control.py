from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from functools import wraps
from src.database import get_db
from src.auth.jwt_handler import AuthHandler

from src.models.user import Role

auth_handler = AuthHandler()


def require_write_access(db: Session = Depends(get_db)):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, auth_data=Depends(auth_handler.auth_wrapper), **kwargs):
            user_id = auth_data["user_id"]
            role = auth_data["role"]

            if role != Role.PATRON:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Write access required for this operation"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator
