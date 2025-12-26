# src/utils/activity_logger.py
from fastapi import Request
from sqlalchemy.orm import Session
from src.models.user_activity import UserActivity
from src.models.user import User
import json

async def log_user_activity(
    db: Session,
    request: Request,
    current_user: User = None,
    request_body: dict = None
):
    try:
        body = json.dumps(request_body or {})[:1000]
        query_params = str(request.query_params)
        activity = UserActivity(
            user_id=current_user.uid if current_user else None,
            role=current_user.role if current_user else None,
            endpoint=request.url.path,
            method=request.method,
            query_params=query_params,
            request_body=body
        )
        db.add(activity)
        db.commit()
    except Exception as e:
        # Optional: use logger to log activity failures
        print(f"[Activity Log Error] {e}")
