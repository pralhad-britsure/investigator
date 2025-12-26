from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from src.models.master_database import PersonalData
from src.auth.dependencies import get_current_user
from src.models.user import User
from src.database import get_db
from src.services.master import get_filtered_users, get_user_by_uid, update_user_by_uid, get_filtered_invalidate_users, create_whistle_blower_users
from src.schemas.master import CompleteUserData, CompleteByIdUserData, UpdateUserData
from src.utils.user_activity import log_user_activity

from src.schemas.master import CreateUserRequest
from src.services.master import create_user
from src.utils.encryption import encrypt_data


router = APIRouter()

@router.get("/users", response_model=List[CompleteUserData])
def get_users(
        name: Optional[str] = None,
        pan_card: Optional[str] = None,
        aadhaar_card: Optional[str] = None,
        mobile: Optional[int] = None,
        location: Optional[str] = None,
        db: Session = Depends(get_db),
):
    users = get_filtered_users(db, name, pan_card, aadhaar_card, mobile, location)
    return users


user_search_count = {}
# Allowed roles with 3 search limit
LIMITED_ROLES = {"patron", "checker", "contributor", "visitor", "guest", "whistle blower"}

@router.get("/limited-search-users", response_model=List[CompleteUserData])
def get_limited_search_users(
    name: Optional[str] = None,
    pan_card: Optional[str] = None,
    aadhaar_card: Optional[str] = None,
    mobile: Optional[int] = None,
    location: Optional[str] = None,
    page: int = 1,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    role = current_user.role.lower()
    uid = current_user.uid

    # Enforce search limit for specific roles
    if role in LIMITED_ROLES:
        user_search_count.setdefault(uid, 0)
        if user_search_count[uid] >= 3:
            raise HTTPException(
                status_code=403,
                detail="Search limit exceeded. Please get a subscription."
            )
        user_search_count[uid] += 1
    else:
        raise HTTPException(status_code=403, detail="You are not allowed to access this API.")

    # Fetch all matching users (unpaginated)
    all_users = get_filtered_users(db, name, pan_card, aadhaar_card, mobile, location)

    # Manual Pagination - show 3 records per page
    page_size = 3
    start = (page - 1) * page_size
    end = start + page_size
    paginated_users = all_users[start:end]

    return paginated_users


@router.get("/invalidate-user", response_model=List[CompleteUserData])
def get_invalidate_user(
        name: Optional[str] = None,
        pan_card: Optional[str] = None,
        aadhaar_card: Optional[str] = None,
        mobile: Optional[int] = None,
        location: Optional[str] = None,
        db: Session = Depends(get_db),
):
    users = get_filtered_invalidate_users(db, name, pan_card, aadhaar_card, mobile, location)
    return users




@router.get("/users-encrypt")
def get_users_encrypt(
        name: Optional[str] = None,
        pan_card: Optional[str] = None,
        aadhaar_card: Optional[str] = None,
        mobile: Optional[int] = None,
        location: Optional[str] = None,
        db: Session = Depends(get_db),
):
    users = get_filtered_users(db, name, pan_card, aadhaar_card, mobile, location)
    user_data = [user.__dict__ for user in users]
    for user in user_data:
        user.pop('_sa_instance_state', None)
    encrypted_response = encrypt_data(user_data)
    return {encrypted_response}


@router.put("/users/{user_id}/validate")
def validate_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(PersonalData).filter(PersonalData.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.status:
        return {"message": "User is already validated"}

    user.status = True
    db.commit()
    db.refresh(user)

    return {"message": "User validated successfully"}





@router.get("/user/{uid}", response_model=CompleteByIdUserData)
def get_user(uid: int, db: Session = Depends(get_db)):
    user_data = get_user_by_uid(db, uid)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data

@router.put("/user/{uid}")
def update_user(uid: int, payload: UpdateUserData, db: Session = Depends(get_db)):
    return update_user_by_uid(db, uid, payload)


# @router.post("/users")
# def create_user_api(user_data: CreateUserRequest, db: Session = Depends(get_db)):
#     try:
#         return create_user(db, user_data)
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))




from src.auth.dependencies import get_current_user
from src.models.user import User

@router.post("/users")
def create_user_api(
    user_data: CreateUserRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_user(db, user_data, current_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/whistle-blower-user")
def create_whistle_blower_user(
    user_data: CreateUserRequest,
    db: Session = Depends(get_db),
):
    try:
        return create_whistle_blower_users(db, user_data)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))







# ALLOWED_ROLES_WITH_LIMIT = {"Patron", "Contributor", "Checker"}
# SEARCH_LIMIT = 3
#
#
# @router.get("/users", response_model=EncryptedResponse)
# async def get_users(
#         name: str,
#         pan_card: Optional[str] = None,
#         aadhaar_card: Optional[str] = None,
#         mobile: Optional[int] = None,
#         location: Optional[str] = None,
#         db: Session = Depends(get_db),
#         request: Request = None,
#         current_user: User = Depends(get_current_user)
# ):
#     users = get_filtered_users(db, name, pan_card, aadhaar_card, mobile, location)
#
#     await log_user_activity(
#         db, request, current_user=current_user,
#         request_body={"name": name, "pan_card": pan_card, "aadhaar_card": aadhaar_card}
#     )
#
#     users_dict = [user.dict() for user in users]
#     encrypted_data = encrypt_data(users_dict)
#     return EncryptedResponse(encrypted_data=encrypted_data)

