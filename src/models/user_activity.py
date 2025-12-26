from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.models.user import Base

class UserActivity(Base):
    __tablename__ = "user_activity"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth_user.uid"), nullable=True)
    endpoint = Column(String, nullable=False)
    method = Column(String, nullable=False)
    query_params = Column(String, nullable=True)
    request_body = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    role = Column(String, nullable=True)

    user = relationship("User", back_populates="activities")
