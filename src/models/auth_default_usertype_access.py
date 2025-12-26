from sqlalchemy import Column, Integer, String, Boolean
from src.database import Base

class AuthDefaultUsertypeAccess(Base):
    __tablename__ = "auth_default_usertype_access"

    user_type_id = Column(Integer, primary_key=True, autoincrement=True)
    user_type = Column(String, unique=True, index=True)
    user_creation = Column(Boolean)

    identity_details = Column(Boolean)
    masked_identity_details = Column(Boolean)

    contact_details = Column(Boolean)
    masked_contact_details = Column(Boolean)

    proffessional_details = Column(Boolean)
    masked_proffessional_details = Column(Boolean)

    allegation_details = Column(Boolean)
    masked_allegation_details = Column(Boolean)

    alert_details = Column(Boolean)
    masked_alert_details = Column(Boolean)

    actions_detail = Column(Boolean)
    masked_actions_detail = Column(Boolean)

    additional_information = Column(Boolean)
    masked_additional_information = Column(Boolean)

    information_source_type = Column(Boolean)
    masked_information_source_type = Column(Boolean)

    full_checking_tracking_history = Column(Boolean)
    masked_checking_history = Column(Boolean)

    audit_tria = Column(Boolean)
