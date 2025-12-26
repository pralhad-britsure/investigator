from src.models.master_database import Base
from src.models.user import User, Role
from src.models.master_database import PersonalData

# Make sure all models are imported so SQLAlchemy can resolve relationships
__all__ = ["Base", "User", "Role", "PersonalData"]