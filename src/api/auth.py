import logging
from fastapi import Request
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserResponse, UserLogin, Token, ForgotPasswordRequest, UserDetailsResponse
from src.services.user_service import create_user, authenticate_user, forgot_password, get_user_by_username
from src.database import get_db
from src.auth.jwt_handler import AuthHandler
from src.models.user import User
from src.services.user_service import get_access_rights_by_role
from src.utils.user_activity import log_user_activity
from src.auth.dependencies import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(tags=["User"])
auth_handler = AuthHandler()


# @router.post("/register", response_model=UserResponse)
# async def register(user: UserCreate, db: Session = Depends(get_db)):
#     try:
#         logger.info(f"Registration request received for email: {user.email_id}")
#         result = create_user(db=db, user=user)
#         logger.info("Registration completed successfully")
#         return result
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Unexpected error in register endpoint: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Internal server error"
#         )


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    try:
        result = create_user(db=db, user=user)
        await log_user_activity(db, request, current_user=result, request_body=user.dict())
        return result
    except HTTPException:
        raise

#
# @router.post("/login", response_model=Token)
# def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
#     user = authenticate_user(db, user_credentials.user_name, user_credentials.user_password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = auth_handler.encode_token(user.uid, user.role)
#
#     # Fetch access rights for the user's role
#     access_rights = get_access_rights_by_role(db, user.role)
#
#     return {
#         "access_token": access_token,
#         "token_type": "bearer",
#         "role": user.role,
#         "access": access_rights
#     }


@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, user_credentials.user_name, user_credentials.user_password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_handler.encode_token(user.uid, user.role)
    access_rights = get_access_rights_by_role(db, user.role)

    # log login activity
    await log_user_activity(db, request, current_user=user, request_body={"action": "login"})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "access": access_rights
    }

# @router.get("/me", response_model=UserResponse)
# def get_current_user(auth_data=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
#     user_id = auth_data["user_id"]
#     user = db.query(User).filter(User.uid == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
#

@router.get("/me", response_model=UserResponse)
async def get_current_user_route(
    request: Request,
    auth_data=Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db)
):
    user_id = auth_data["user_id"]
    user = db.query(User).filter(User.uid == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await log_user_activity(db, request, current_user=user, request_body={"action": "get_me"})
    return user


# @router.post("/forgot-password")
# def forgot_password_route(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
#     password = forgot_password(db, data)
#     return password
#

@router.post("/forgot-password")
async def forgot_password_route(
    data: ForgotPasswordRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    password = forgot_password(db, data)

    # Try to fetch user object if email/username is available in request
    user = db.query(User).filter(User.user_name == data.user_name).first()

    if user:
        await log_user_activity(db, request, current_user=user, request_body={"action": "forgot_password"})

    return password


# @router.get("/user-info/{user_name}", response_model=UserDetailsResponse)
# def get_user_details(user_name: str, db: Session = Depends(get_db)):
#     return get_user_by_username(db, user_name)


@router.get("/user-info/{user_name}", response_model=UserDetailsResponse)
async def get_user_details(
    user_name: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await log_user_activity(db, request, current_user=current_user, request_body={"searched_user": user_name})
    return get_user_by_username(db, user_name)
