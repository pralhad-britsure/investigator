from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.database import get_db
from sqlalchemy.orm import Session
from src.schemas.user_management import UserListResponse, UserUpdate
from src.services.user_management import get_all_users, get_user_by_id, update_user, delete_user
router =  APIRouter()

@router.get("/users", response_model=List[UserListResponse])
def fetch_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.get("/users/{user_id}", response_model=UserListResponse)
def fetch_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserListResponse)
def update_user_by_id(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user_data)


@router.delete("/users/{user_id}")
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)
