import random
import string
import logging
from passlib.hash import bcrypt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.auth.jwt_handler import AuthHandler
from src.models.user import User
from src.schemas.user import UserCreate, ForgotPasswordRequest
from src.utils.email_utils import send_credentials_email

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_handler = AuthHandler()


def generate_random_password() -> str:
    letters = ''.join(random.choices(string.ascii_lowercase, k=4))
    special = random.choice('!@#$%^&*')
    digits = ''.join(random.choices(string.digits, k=3))

    password_chars = list(letters + special + digits)
    random.shuffle(password_chars)

    return ''.join(password_chars)


def generate_unique_username(db: Session, f_name: str = None, l_name: str = None, email_id: str = None) -> str:
    try:
        if f_name or l_name:
            base_username = (f_name or "") + (l_name or "")
            base_username = base_username.lower()
        else:
            base_username = email_id.split('@')[0].lower()
        base_username = ''.join(c for c in base_username if c.isalnum())[:7]
        for attempt in range(10):
            suffix = ''.join(random.choices(string.digits, k=3))
            username = f"{base_username}{suffix}"[:10]

            existing_user = db.query(User).filter(User.user_name == username).first()
            if not existing_user:
                return username

        import time
        timestamp = str(int(time.time()))[-6:]
        return f"user{timestamp}"

    except Exception as e:
        logger.error(f"Error generating username: {e}")
        import time
        timestamp = str(int(time.time()))[-6:]
        return f"user{timestamp}"

#
# def create_user(db: Session, user: UserCreate):
#     try:
#         logger.info(f"Creating user with email: {user.email_id}")
#
#         if not user.email_id:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Email is required"
#             )
#
#         existing_email = db.query(User).filter(User.email_id == user.email_id).first()
#         if existing_email:
#             logger.warning(f"Email already exists: {user.email_id}")
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Email already registered"
#             )
#         if user.mobile:
#             existing_mobile = db.query(User).filter(User.mobile == user.mobile).first()
#             if existing_mobile:
#                 logger.warning(f"Mobile already exists: {user.mobile}")
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail="Mobile number already registered"
#                 )
#
#         logger.info("Generating unique username...")
#         user_name = generate_unique_username(db, user.f_name, user.l_name, user.email_id)
#         logger.info(f"Generated username: {user_name}")
#
#         plain_password = generate_random_password()
#         logger.info("Password generated/provided")
#         db_user = User(
#             f_name=user.f_name,
#             l_name=user.l_name,
#             mobile=user.mobile,
#             email_id=user.email_id,
#             organisation_type=user.organisation_type,
#             individual_type=user.individual_type,
#             purpose_or_objective=user.purpose_or_objective,
#             user_type=user.user_type,
#             user_name=user_name,
#             user_password=bcrypt.hash(plain_password),
#             role=user.role or "Patron",
#         )
#
#         # Database operations with proper error handling
#         logger.info("Adding user to database...")
#         db.add(db_user)
#
#         try:
#             db.commit()
#             db.refresh(db_user)
#             logger.info(f"User created successfully with ID: {db_user.uid}")
#         except IntegrityError as e:
#             db.rollback()
#             logger.error(f"Database integrity error: {e}")
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="User with this information already exists"
#             )
#         except Exception as e:
#             db.rollback()
#             logger.error(f"Database commit failed: {e}")
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Failed to create user"
#             )
#         logger.info("Attempting to send credentials email...")
#         try:
#             send_credentials_email(user.email_id, user_name, plain_password)
#             logger.info("Email sent successfully")
#         except Exception as e:
#             logger.error(f"Failed to send email: {e}")
#         logger.info("User registration completed successfully")
#         return db_user
#
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Unexpected error in create_user: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Internal server error during user creation"
#         )
def create_user(db: Session, user: UserCreate):
    try:
        logger.info(f"Creating user with email: {user.email_id}")

        if not user.email_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is required"
            )

        existing_email = db.query(User).filter(User.email_id == user.email_id).first()
        if existing_email:
            logger.warning(f"Email already exists: {user.email_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        if user.mobile:
            existing_mobile = db.query(User).filter(User.mobile == user.mobile).first()
            if existing_mobile:
                logger.warning(f"Mobile already exists: {user.mobile}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Mobile number already registered"
                )

        logger.info("Generating unique username...")
        user_name = generate_unique_username(db, user.f_name, user.l_name, user.email_id)
        logger.info(f"Generated username: {user_name}")

        plain_password = generate_random_password()
        logger.info("Password generated")

        db_user = User(
            f_name=user.f_name,
            l_name=user.l_name,
            mobile=user.mobile,
            email_id=user.email_id,
            organisation_type=user.organisation_type,
            individual_type=user.individual_type,
            purpose_or_objective=user.purpose_or_objective,
            user_type=user.user_type,
            user_name=user_name,
            user_password=bcrypt.hash(plain_password),
            role=user.role or "Patron",
        )

        logger.info("Attempting to send credentials email before DB commit...")
        try:
            send_credentials_email(user.email_id, user_name, plain_password)
            logger.info("Email sent successfully")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send email. User not registered."
            )

        logger.info("Adding user to database and committing...")
        db.add(db_user)
        try:
            db.commit()
            db.refresh(db_user)
            logger.info(f"User created successfully with ID: {db_user.uid}")
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Database integrity error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this information already exists"
            )
        except Exception as e:
            db.rollback()
            logger.error(f"Database commit failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )

        logger.info("User registration completed successfully")
        return db_user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in create_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during user creation"
        )

def authenticate_user(db: Session, user_name: str, password: str):
    user = db.query(User).filter(User.user_name == user_name).first()

    if not user:
        return False
    if not auth_handler.verify_password(password, user.user_password):
        return False
    return user

def get_access_rights_by_role(db: Session, role: str):
    from src.models.auth_default_usertype_access import AuthDefaultUsertypeAccess
    access_entry = db.query(AuthDefaultUsertypeAccess).filter(
        AuthDefaultUsertypeAccess.user_type == role
    ).first()
    if not access_entry:
        return {}
    access_dict = {
        k: v for k, v in access_entry.__dict__.items()
        if not k.startswith("_") and isinstance(v, int) and v == 1
    }
    return access_dict


def forgot_password(db: Session, data: ForgotPasswordRequest):
    # Find user by username
    user = db.query(User).filter(User.user_name == data.user_name).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logger.info(f"Processing forgot password for user: {user.user_name}")

    # Validate new password matches confirm password
    if data.new_password != data.confirm_new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirm password do not match"
        )

    # Hash and update the new password
    user.user_password = bcrypt.hash(data.new_password)

    try:
        db.commit()
        db.refresh(user)
        logger.info(f"Password successfully updated for user: {user.user_name}")
        return {"message": "Password reset successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating password for user {user.user_name}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update password"
        )


def get_user_by_username(db: Session, user_name: str):
    user = db.query(User).filter(User.user_name == user_name).first()

    if not user:
        logger.warning(f"User not found: {user_name}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logger.info(f"Retrieved user details for: {user_name}")

    # Handle mobile field conversion
    mobile_value = None
    if user.mobile is not None and user.mobile != 0:
        mobile_value = str(user.mobile)

    return {
        "f_name": user.f_name,
        "l_name": user.l_name,
        "mobile": mobile_value,
        "email_id": user.email_id,
        "role": user.role
    }
