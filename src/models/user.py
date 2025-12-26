import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLEnum

from sqlalchemy import Column, Integer, String, Boolean, Enum, BigInteger

from src.models.base import Base


class Role(str, enum.Enum):
    SUPER_ADMIN = "Super_Admin"
    MASTER = "Master"
    PATRON = "Patron"
    CONTRIBUTOR = "Contributor"
    CHECKER = "Checker"
    VISITOR = "Visitor"
    GUEST = "Guest"
    PUBLIC = "Public"
    WHISTLE_BLOWER = "Whistle_Blower"


class User(Base):
    __tablename__ = "auth_user"

    uid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    f_name = Column(String(50))
    l_name = Column(String(50))
    mobile = Column(BigInteger)
    email_id = Column(String(50), unique=True, index=True)
    organisation_type = Column(String(50))
    individual_type = Column(String(50))
    purpose_or_objective = Column(String(50))
    user_type = Column(String(50))
    user_name = Column(String(10), unique=True, index=True)
    user_password = Column(String(255))
    role = Column(
        SQLEnum(
            Role,
            native_enum=False,
            values_callable=lambda x: [e.value for e in x]
        ),
        default=Role.PATRON.value
    )
    activities = relationship("UserActivity", back_populates="user", cascade="all, delete-orphan")
    personal_data = relationship("PersonalData", back_populates="user", uselist=False)
