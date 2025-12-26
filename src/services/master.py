# from sqlalchemy.orm import Session
# from sqlalchemy import or_, func
#
# from src.schemas.master import CompleteUserData, ProfessionalHistoryResponse, AlertResponse
# from src.models.master_database import PersonalData, Contact, ProfessionalHistory, Alert
#
#
# def get_filtered_users(
#         db: Session,
#         name: str = None,
#         pan_card: str = None,
#         aadhaar_card: str = None,
#         mobile: int = None,
#         location: str = None
# ):
#     query = db.query(PersonalData)
#
#     if name:
#         name = name.lower().strip()
#         # Normalize spaces in search term
#         name = ' '.join(name.split())
#
#         # Create individual name parts for flexible matching
#         name_parts = name.split()
#
#         conditions = []
#
#         # Match individual name parts
#         conditions.extend([
#             func.lower(func.trim(PersonalData.first_name)).ilike(f"%{name}%"),
#             func.lower(func.trim(PersonalData.middle_name)).ilike(f"%{name}%"),
#             func.lower(func.trim(PersonalData.last_name)).ilike(f"%{name}%")
#         ])
#
#         # If multiple words in search, try to match each part
#         if len(name_parts) > 1:
#             for part in name_parts:
#                 conditions.extend([
#                     func.lower(func.trim(PersonalData.first_name)).ilike(f"%{part}%"),
#                     func.lower(func.trim(PersonalData.middle_name)).ilike(f"%{part}%"),
#                     func.lower(func.trim(PersonalData.last_name)).ilike(f"%{part}%")
#                 ])
#
#         # Try full name combinations with simple concat and space normalization
#         full_name_combinations = [
#             func.trim(func.concat(func.trim(PersonalData.first_name), ' ', func.trim(PersonalData.last_name))),
#             func.trim(func.concat(func.trim(PersonalData.first_name), ' ', func.trim(PersonalData.middle_name), ' ',
#                                   func.trim(PersonalData.last_name))),
#             func.trim(func.concat(func.trim(PersonalData.last_name), ' ', func.trim(PersonalData.first_name)))
#         ]
#
#         for combo in full_name_combinations:
#             conditions.append(func.lower(combo).ilike(f"%{name}%"))
#
#         query = query.filter(or_(*conditions))
#
#     if pan_card:
#         query = query.filter(PersonalData.pan_card == pan_card)
#
#     if aadhaar_card:
#         query = query.filter(PersonalData.aadhaar_card == aadhaar_card)
#
#     if location:
#         location = location.lower()
#         query = query.filter(
#             or_(
#                 func.lower(PersonalData.city).ilike(f"%{location}%"),
#                 func.lower(PersonalData.taluka).ilike(f"%{location}%"),
#                 func.lower(PersonalData.district).ilike(f"%{location}%"),
#                 func.lower(PersonalData.state).ilike(f"%{location}%")
#             )
#         )
#
#     personal_results = query.all()
#     final_result = []
#
#     for person in personal_results:
#         contact = db.query(Contact).filter(Contact.user_id == person.user_id).first()
#
#         # Only filter by mobile if mobile parameter is provided
#         if mobile is not None and contact:
#             mobile_str = str(mobile)
#             contact_mobiles = [str(contact.mob_1), str(contact.mob_2), str(contact.mob_3)]
#             # Filter out 'None' strings from contact_mobiles
#             contact_mobiles = [mob for mob in contact_mobiles if mob != 'None' and mob is not None]
#
#             if mobile_str not in contact_mobiles:
#                 continue
#
#         prof_history = db.query(ProfessionalHistory).filter(ProfessionalHistory.user_id == person.user_id).all()
#         prof_history_response = [ProfessionalHistoryResponse.model_validate(p) for p in prof_history]
#
#         alerts = db.query(Alert).filter(Alert.user_id == person.user_id).all()
#         alerts_response = [AlertResponse.model_validate(a) for a in alerts]
#
#         final_result.append(
#             CompleteUserData(
#                 personal_data=person,
#                 contact=contact,
#                 professional_history=prof_history_response if prof_history_response else None,
#                 alert=alerts_response if alerts_response else None
#             )
#         )
#     return final_result


from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from src.models.user import User
from src.schemas.master import CompleteUserData, ProfessionalHistoryResponse, AlertResponse, CompleteByIdUserData, \
    PersonalDataByIdResponse, ContactByIdResponse, ProfessionalByIdHistoryResponse, AlertByIdResponse, UserCompleteData
from src.models.master_database import PersonalData, Contact, ProfessionalHistory, Alert


def get_filtered_users(db: Session, name: str = None, pan_card: str = None,
                       aadhaar_card: str = None, mobile: int = None, location: str = None):
    query = db.query(PersonalData).filter(PersonalData.status == True)


    # Name filtering
    if name:
        name = name.lower().strip()
        name_parts = name.split()
        conditions = []

        for part in name_parts:
            conditions.extend([
                func.lower(PersonalData.first_name).ilike(f"%{part}%"),
                func.lower(PersonalData.middle_name).ilike(f"%{part}%"),
                func.lower(PersonalData.last_name).ilike(f"%{part}%")
            ])

        query = query.filter(or_(*conditions))

    # Other filters
    if pan_card:
        query = query.filter(PersonalData.pan_card == pan_card)
    if aadhaar_card:
        query = query.filter(PersonalData.aadhaar_card == aadhaar_card)
    if location:
        query = query.filter(func.lower(PersonalData.city).ilike(f"%{location.lower()}%"))

    results = []
    for person in query.all():
        contact = db.query(Contact).filter(Contact.user_id == person.user_id).first()

        # Mobile filter
        if mobile and contact:
            mobiles = [contact.mob_1, contact.mob_2, contact.mob_3]
            if mobile not in [m for m in mobiles if m]:
                continue

        prof_history = db.query(ProfessionalHistory).filter(ProfessionalHistory.user_id == person.user_id).all()
        alerts = db.query(Alert).filter(Alert.user_id == person.user_id).all()

        results.append(CompleteUserData(
            personal_data=person,
            contact=contact,
            professional_history=[ProfessionalHistoryResponse.model_validate(p) for p in prof_history] or None,
            alert=[AlertResponse.model_validate(a) for a in alerts] or None
        ))

    return results


def get_filtered_invalidate_users(db: Session, name: str = None, pan_card: str = None,
                       aadhaar_card: str = None, mobile: int = None, location: str = None):
    query = db.query(PersonalData).filter(PersonalData.status == False)


    # Name filtering
    if name:
        name = name.lower().strip()
        name_parts = name.split()
        conditions = []

        for part in name_parts:
            conditions.extend([
                func.lower(PersonalData.first_name).ilike(f"%{part}%"),
                func.lower(PersonalData.middle_name).ilike(f"%{part}%"),
                func.lower(PersonalData.last_name).ilike(f"%{part}%")
            ])

        query = query.filter(or_(*conditions))

    # Other filters
    if pan_card:
        query = query.filter(PersonalData.pan_card == pan_card)
    if aadhaar_card:
        query = query.filter(PersonalData.aadhaar_card == aadhaar_card)
    if location:
        query = query.filter(func.lower(PersonalData.city).ilike(f"%{location.lower()}%"))

    results = []
    for person in query.all():
        contact = db.query(Contact).filter(Contact.user_id == person.user_id).first()

        # Mobile filter
        if mobile and contact:
            mobiles = [contact.mob_1, contact.mob_2, contact.mob_3]
            if mobile not in [m for m in mobiles if m]:
                continue

        prof_history = db.query(ProfessionalHistory).filter(ProfessionalHistory.user_id == person.user_id).all()
        alerts = db.query(Alert).filter(Alert.user_id == person.user_id).all()

        results.append(CompleteUserData(
            personal_data=person,
            contact=contact,
            professional_history=[ProfessionalHistoryResponse.model_validate(p) for p in prof_history] or None,
            alert=[AlertResponse.model_validate(a) for a in alerts] or None
        ))

    return results



from src.models.master_database import PersonalData, Contact, ProfessionalHistory, Alert
from src.schemas.master import CreateUserRequest
from sqlalchemy.orm import Session

# def create_user(db: Session, user_data: CreateUserRequest):
#     # Insert into PersonalData
#     personal = PersonalData(**user_data.personal_data.dict())
#     db.add(personal)
#     db.commit()
#     db.refresh(personal)
#
#     user_id = personal.user_id
#
#     # Insert Contact
#     if user_data.contact:
#         contact = Contact(**user_data.contact.dict(), user_id=user_id)
#         db.add(contact)
#
#     # Insert Professional History
#     if user_data.professional_history:
#         for history_data in user_data.professional_history:
#             history = ProfessionalHistory(**history_data.dict(), user_id=user_id)
#             db.add(history)
#
#     # Insert Alert
#     if user_data.alert:
#         for alert_data in user_data.alert:
#             alert = Alert(**alert_data.dict(), user_id=user_id)
#             db.add(alert)
#
#     db.commit()
#     return {"message": "User created successfully", "user_id": user_id}


def create_user(db: Session, user_data: CreateUserRequest, current_user: User):
    # Include uid when inserting PersonalData
    personal = PersonalData(
        **user_data.personal_data.dict(),
        uid=current_user.uid  # <- Set foreign key here
    )
    db.add(personal)
    db.commit()
    db.refresh(personal)

    user_id = personal.user_id

    # Insert Contact
    if user_data.contact:
        contact = Contact(**user_data.contact.dict(), user_id=user_id)
        db.add(contact)

    # Insert Professional History
    if user_data.professional_history:
        for history_data in user_data.professional_history:
            history = ProfessionalHistory(**history_data.dict(), user_id=user_id)
            db.add(history)

    # Insert Alert
    if user_data.alert:
        for alert_data in user_data.alert:
            alert = Alert(**alert_data.dict(), user_id=user_id)
            db.add(alert)

    db.commit()
    return {"message": "User created successfully", "user_id": user_id}


def create_whistle_blower_users(db: Session, user_data: CreateUserRequest):
    # No current_user.uid; adjust logic accordingly

    personal = PersonalData(
        **user_data.personal_data.dict(),
        # Remove uid or replace it with default value or logic
        uid=None  # or some default value if needed
    )
    db.add(personal)
    db.commit()
    db.refresh(personal)

    user_id = personal.user_id

    # Insert Contact
    if user_data.contact:
        contact = Contact(**user_data.contact.dict(), user_id=user_id)
        db.add(contact)

    # Insert Professional History
    if user_data.professional_history:
        for history_data in user_data.professional_history:
            history = ProfessionalHistory(**history_data.dict(), user_id=user_id)
            db.add(history)

    # Insert Alert
    if user_data.alert:
        for alert_data in user_data.alert:
            alert = Alert(**alert_data.dict(), user_id=user_id)
            db.add(alert)

    db.commit()
    return {"message": "User created successfully", "user_id": user_id}





from sqlalchemy.orm import Session
from src.models.master_database import PersonalData, Contact, ProfessionalHistory, Alert
from src.schemas.master import CompleteUserData, PersonalDataResponse, ContactResponse, ProfessionalHistoryResponse, AlertResponse

def get_user_by_uid(db: Session, uid: int) -> CompleteByIdUserData:
    person_records = db.query(PersonalData).filter(PersonalData.uid == uid).all()

    if not person_records:
        return None

    user_ids = [p.user_id for p in person_records]

    # Fetch all related data
    contacts_map = {c.user_id: c for c in db.query(Contact).filter(Contact.user_id.in_(user_ids)).all()}
    prof_history_map = {}
    for p in db.query(ProfessionalHistory).filter(ProfessionalHistory.user_id.in_(user_ids)).all():
        prof_history_map.setdefault(p.user_id, []).append(p)

    alert_map = {}
    for a in db.query(Alert).filter(Alert.user_id.in_(user_ids)).all():
        alert_map.setdefault(a.user_id, []).append(a)

    # Build the response per personal record
    user_data_list = []
    for person in person_records:
        user_id = person.user_id
        user_data = UserCompleteData(
            personal_data=PersonalDataByIdResponse.model_validate(person),
            contact=ContactByIdResponse.model_validate(contacts_map[user_id]) if user_id in contacts_map else None,
            professional_history=[ProfessionalByIdHistoryResponse.model_validate(ph) for ph in prof_history_map.get(user_id, [])],
            alert=[AlertByIdResponse.model_validate(al) for al in alert_map.get(user_id, [])]
        )
        user_data_list.append(user_data)

    return CompleteByIdUserData(user_data_list)






from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.master_database import PersonalData, Contact, ProfessionalHistory, Alert
from src.schemas.master import UpdateUserData

# def update_user_by_uid(db: Session, user_id: int, data: UpdateUserData):
#     person = db.query(PersonalData).filter(PersonalData.user_id == user_id).first()
#     if not person:
#         raise HTTPException(status_code=404, detail="User not found")
#
#     user_id = person.user_id
#
#     # Update personal data
#     if data.personal_data:
#         for key, value in data.personal_data.dict(exclude_unset=True).items():
#             setattr(person, key, value)
#
#     # Update contact
#     if data.contact:
#         contact = db.query(Contact).filter(Contact.user_id == user_id).first()
#         if contact:
#             for key, value in data.contact.dict(exclude_unset=True).items():
#                 setattr(contact, key, value)
#
#     # Update professional history
#     if data.professional_history:
#         for item in data.professional_history:
#             if not item.prof_id:
#                 continue
#             record = db.query(ProfessionalHistory).filter_by(prof_id=item.prof_id, user_id=user_id).first()
#             if record:
#                 for key, value in item.dict(exclude={"prof_id"}, exclude_unset=True).items():
#                     setattr(record, key, value)
#
#     # Update alerts
#     if data.alert:
#         for item in data.alert:
#             if not item.alert_id:
#                 continue
#             alert_record = db.query(Alert).filter_by(alert_id=item.alert_id, user_id=user_id).first()
#             if alert_record:
#                 for key, value in item.dict(exclude={"alert_id"}, exclude_unset=True).items():
#                     setattr(alert_record, key, value)
#
#     db.commit()
#     return {"message": "User data updated successfully"}


def update_user_by_uid(db: Session, user_id: int, data: UpdateUserData):
    person = db.query(PersonalData).filter(PersonalData.user_id == user_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = person.user_id

    # Update personal data
    if data.personal_data:
        for key, value in data.personal_data.dict(exclude_unset=True).items():
            setattr(person, key, value)

    # Update contact
    if data.contact:
        contact = db.query(Contact).filter(Contact.user_id == user_id).first()
        if contact:
            for key, value in data.contact.dict(exclude_unset=True).items():
                setattr(contact, key, value)

    # Update professional history - Alternative approach
    if data.professional_history:
        # Get all existing professional history records for this user
        existing_records = db.query(ProfessionalHistory).filter(ProfessionalHistory.user_id == user_id).all()

        for i, item in enumerate(data.professional_history):
            if i < len(existing_records):
                # Update existing record
                record = existing_records[i]
                for key, value in item.dict(exclude_unset=True).items():
                    setattr(record, key, value)
            else:
                # Create new record if more items than existing records
                new_record = ProfessionalHistory(user_id=user_id, **item.dict(exclude_unset=True))
                db.add(new_record)

    # Update alerts - Alternative approach
    if data.alert:
        # Get all existing alert records for this user
        existing_alerts = db.query(Alert).filter(Alert.user_id == user_id).all()

        for i, item in enumerate(data.alert):
            if i < len(existing_alerts):
                # Update existing record
                alert_record = existing_alerts[i]
                for key, value in item.dict(exclude_unset=True).items():
                    setattr(alert_record, key, value)
            else:
                # Create new record if more items than existing records
                new_alert = Alert(user_id=user_id, **item.dict(exclude_unset=True))
                db.add(new_alert)

    db.commit()
    return {"message": "User data updated successfully"}
