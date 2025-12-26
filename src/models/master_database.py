from sqlalchemy import Boolean
from sqlalchemy import Column, Integer, String, Date, BigInteger, ForeignKey, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from src.models.base import Base


class PersonalData(Base):
    __tablename__ = "mst_personal_data"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100))
    middle_name = Column(String(100))
    last_name = Column(String(100))
    dob = Column(Date)
    gender = Column(String(50))
    pan_card = Column(String(10))
    aadhaar_card = Column(String(12))
    driving_license = Column(String(20))
    address = Column(String(250))
    city = Column(String(50))
    taluka = Column(String(50))
    district = Column(String(50))
    state = Column(String(50))

    uid = Column(Integer, ForeignKey("auth_user.uid"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    status = Column(Boolean, default=False, server_default=text("0"))

    user = relationship("User", back_populates="personal_data")


class ProfessionalHistory(Base):
    __tablename__ = "mst_professional_history"

    prof_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("mst_personal_data.user_id"))
    agency_name_1 = Column(String(150))
    agency_owner_1 = Column(String(150))
    reporting_head_1 = Column(String(150))
    type_of_relieving_1 = Column(String(255), nullable=True)
    date_of_relieving_1 = Column(Date)
    reported_by_1 = Column(String(150))
    relieving_remark_1 = Column(String(500))
    type_of_allegation_1 = Column(String(100), nullable=True)
    agency_name_2 = Column(String(150))
    agency_owner_2 = Column(String(150))
    reporting_head_2 = Column(String(150))
    type_of_relieving_2 = Column(String(255), nullable=True)
    date_of_relieving_2 = Column(Date)
    reported_by_2 = Column(String(150))
    relieving_remark_2 = Column(String(500))
    type_of_allegation_2 = Column(String(100), nullable=True)
    nop_oi = Column(String(150))
    case_or_claimno = Column(String(50))

class Contact(Base):
    __tablename__ = "mst_contacts"

    contact_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("mst_personal_data.user_id"))
    mob_1 = Column(BigInteger)
    mob_2 = Column(BigInteger)
    mob_3 = Column(BigInteger)
    email_1 = Column(String(100))
    email_2 = Column(String(100))
    email_3 = Column(String(100))

class Alert(Base):
    __tablename__ = "mst_alerts"

    alert_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("mst_personal_data.user_id"))
    alert_from = Column(String(255), nullable=True)
    terminated_by = Column(String(150))
    asked_to_resign_by = Column(String(150))
    relieved_from = Column(String(150))
    resigned_from = Column(String(150))
    police_complaint_by = Column(String(150))
    complaint_ps_name = Column(String(150))
    complaint_date = Column(Date)
    fir_by = Column(String(150))
    fir_ps_name = Column(String(150))
    fir_date = Column(Date)
    what = Column(String(250))
    when_info = Column(String(250))
    by_whom = Column(String(250))
    information_date = Column(Date)
    information_source_type = Column(String(250))
    entry_type = Column(String(100), nullable=True)
