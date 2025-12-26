from enum import Enum

class Role(str, Enum):
    SUPER_ADMIN = "Super Admin"
    MASTER = "Master"
    PATRON = "Patron"
    CONTRIBUTOR = "Contributor"
    CHECKER = "Checker"
    VISITOR = "Visitor"
    GUEST = "Guest"
    PUBLIC = "Public"
    WHISTLE_BLOWER = "Whistle Blower"


class AccessRight(str, Enum):
    USER_CREATION = "User Creation"
    IDENTITY_DETAILS = "Identity Details"
    MASKED_IDENTITY_DETAILS = "Masked Identity Details"
    CONTACT_DETAILS = "Contact Details"
    MASKED_CONTACT_DETAILS = "Masked Contact Details"
    PROFESSIONAL_DETAILS = "Professional Details"
    MASKED_PROFESSIONAL_DETAILS = "Masked Professional Details"
    ALLEGATION_DETAILS = "Allegation Details"
