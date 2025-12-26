# src/auth/dependencies.py

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.user import User
from src.auth.jwt_handler import AuthHandler

auth_handler = AuthHandler()

def get_current_user(
    auth_data=Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db)
) -> User:
    user_id = auth_data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.uid == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
