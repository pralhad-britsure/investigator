from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class PersonalDataResponse(BaseModel):
    user_id: Optional[int] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    pan_card: Optional[str] = None
    aadhaar_card: Optional[str] = None
    driving_license: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    taluka: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None

    class Config:
        from_attributes = True

class ContactResponse(BaseModel):
    mob_1: Optional[int] = None
    mob_2: Optional[int] = None
    mob_3: Optional[int] = None
    email_1: Optional[str] = None
    email_2: Optional[str] = None
    email_3: Optional[str] = None

    class Config:
        from_attributes = True

class ProfessionalHistoryResponse(BaseModel):
    agency_name_1: Optional[str]
    agency_owner_1: Optional[str]
    reporting_head_1: Optional[str]
    type_of_relieving_1: Optional[str]
    date_of_relieving_1: Optional[date]
    reported_by_1: Optional[str]
    relieving_remark_1: Optional[str]
    type_of_allegation_1: Optional[str]

    agency_name_2: Optional[str]
    agency_owner_2: Optional[str]
    reporting_head_2: Optional[str]
    type_of_relieving_2: Optional[str]
    date_of_relieving_2: Optional[date]
    reported_by_2: Optional[str]
    relieving_remark_2: Optional[str]
    type_of_allegation_2: Optional[str]

    nop_oi: Optional[str]
    case_or_claimno: Optional[str]

    class Config:
        from_attributes = True

class AlertResponse(BaseModel):
    alert_from: Optional[str]
    terminated_by: Optional[str]
    asked_to_resign_by: Optional[str]
    relieved_from: Optional[str]
    resigned_from: Optional[str]
    police_complaint_by: Optional[str]
    complaint_ps_name: Optional[str]
    complaint_date: Optional[date]
    fir_by: Optional[str]
    fir_ps_name: Optional[str]
    fir_date: Optional[date]
    what: Optional[str]
    when_info: Optional[str]
    by_whom: Optional[str]
    information_date: Optional[date]
    information_source_type: Optional[str]
    entry_type: Optional[str]

    class Config:
        from_attributes = True

class CompleteUserData(BaseModel):
    personal_data: PersonalDataResponse
    contact: Optional[ContactResponse] = None
    professional_history: Optional[List[ProfessionalHistoryResponse]] = None
    alert: Optional[List[AlertResponse]] = None


#######################
class PersonalDataCreate(BaseModel):
    first_name: str
    middle_name: Optional[str]
    last_name: Optional[str]
    dob: Optional[date]
    gender: Optional[str]
    pan_card: Optional[str]
    aadhaar_card: Optional[str]
    driving_license: Optional[str]
    address: Optional[str]
    city: Optional[str]
    taluka: Optional[str]
    district: Optional[str]
    state: Optional[str]



class ProfessionalHistoryCreate(BaseModel):
    agency_name_1: Optional[str]
    agency_owner_1: Optional[str]
    reporting_head_1: Optional[str]
    type_of_relieving_1: Optional[str]
    date_of_relieving_1: Optional[date]
    reported_by_1: Optional[str]
    relieving_remark_1: Optional[str]
    type_of_allegation_1: Optional[str]

    agency_name_2: Optional[str]
    agency_owner_2: Optional[str]
    reporting_head_2: Optional[str]
    type_of_relieving_2: Optional[str]
    date_of_relieving_2: Optional[date]
    reported_by_2: Optional[str]
    relieving_remark_2: Optional[str]
    type_of_allegation_2: Optional[str]

    nop_oi: Optional[str]
    case_or_claimno: Optional[str]


class ContactCreate(BaseModel):
    mob_1: Optional[int]
    mob_2: Optional[int]
    mob_3: Optional[int]
    email_1: Optional[str]
    email_2: Optional[str]
    email_3: Optional[str]


class AlertCreate(BaseModel):
    alert_from: Optional[str]
    terminated_by: Optional[str]
    asked_to_resign_by: Optional[str]
    relieved_from: Optional[str]
    resigned_from: Optional[str]
    police_complaint_by: Optional[str]
    complaint_ps_name: Optional[str]
    complaint_date: Optional[date]
    fir_by: Optional[str]
    fir_ps_name: Optional[str]
    fir_date: Optional[date]
    what: Optional[str]
    when_info: Optional[str]
    by_whom: Optional[str]
    information_date: Optional[date]
    information_source_type: Optional[str]
    entry_type: Optional[str]


class CreateUserRequest(BaseModel):
    personal_data: Optional[PersonalDataCreate]
    contact: Optional[ContactCreate]
    professional_history: Optional[List[ProfessionalHistoryCreate]]
    alert: Optional[List[AlertCreate]]





class PersonalDataByIdResponse(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    pan_card: Optional[str] = None
    aadhaar_card: Optional[str] = None
    driving_license: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    taluka: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    uid: int
    created_at: datetime
    modified_at: datetime
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class ContactByIdResponse(BaseModel):
    mob_1: Optional[int] = None
    mob_2: Optional[int] = None
    mob_3: Optional[int] = None
    email_1: Optional[str] = None
    email_2: Optional[str] = None
    email_3: Optional[str] = None

    class Config:
        from_attributes = True

class ProfessionalByIdHistoryResponse(BaseModel):
    agency_name_1: Optional[str]
    agency_owner_1: Optional[str]
    reporting_head_1: Optional[str]
    type_of_relieving_1: Optional[str]
    date_of_relieving_1: Optional[date]
    reported_by_1: Optional[str]
    relieving_remark_1: Optional[str]
    type_of_allegation_1: Optional[str]

    agency_name_2: Optional[str]
    agency_owner_2: Optional[str]
    reporting_head_2: Optional[str]
    type_of_relieving_2: Optional[str]
    date_of_relieving_2: Optional[date]
    reported_by_2: Optional[str]
    relieving_remark_2: Optional[str]
    type_of_allegation_2: Optional[str]

    nop_oi: Optional[str]
    case_or_claimno: Optional[str]

    class Config:
        from_attributes = True

class AlertByIdResponse(BaseModel):
    alert_from: Optional[str]
    terminated_by: Optional[str]
    asked_to_resign_by: Optional[str]
    relieved_from: Optional[str]
    resigned_from: Optional[str]
    police_complaint_by: Optional[str]
    complaint_ps_name: Optional[str]
    complaint_date: Optional[date]
    fir_by: Optional[str]
    fir_ps_name: Optional[str]
    fir_date: Optional[date]
    what: Optional[str]
    when_info: Optional[str]
    by_whom: Optional[str]
    information_date: Optional[date]
    information_source_type: Optional[str]
    entry_type: Optional[str]

    class Config:
        from_attributes = True

from pydantic import BaseModel, RootModel

class UserCompleteData(BaseModel):
    personal_data: PersonalDataByIdResponse
    contact: Optional[ContactByIdResponse] = None
    professional_history: Optional[List[ProfessionalByIdHistoryResponse]] = None
    alert: Optional[List[AlertByIdResponse]] = None

class CompleteByIdUserData(RootModel[List[UserCompleteData]]):
    pass




#
# from pydantic import BaseModel
# from typing import Optional, List
# from datetime import datetime, date
#
# class UpdatePersonalData(BaseModel):
#     first_name: Optional[str] = None
#     middle_name: Optional[str] = None
#     last_name: Optional[str] = None
#     dob: Optional[date] = None
#     gender: Optional[str] = None
#     pan_card: Optional[str] = None
#     aadhaar_card: Optional[str] = None
#     driving_license: Optional[str] = None
#     address: Optional[str] = None
#     city: Optional[str] = None
#     taluka: Optional[str] = None
#     district: Optional[str] = None
#     state: Optional[str] = None
#
# class UpdateContact(BaseModel):
#     mob_1: Optional[int] = None
#     mob_2: Optional[int] = None
#     mob_3: Optional[int] = None
#     email_1: Optional[str] = None
#     email_2: Optional[str] = None
#     email_3: Optional[str] = None
#
# class UpdateProfessionalHistory(BaseModel):
#     prof_id: Optional[int] = None  # required to identify existing row
#     agency_name_1: Optional[str]
#     agency_owner_1: Optional[str]
#     reporting_head_1: Optional[str]
#     type_of_relieving_1: Optional[str]
#     date_of_relieving_1: Optional[date]
#     reported_by_1: Optional[str]
#     relieving_remark_1: Optional[str]
#     type_of_allegation_1: Optional[str]
#
#     agency_name_2: Optional[str]
#     agency_owner_2: Optional[str]
#     reporting_head_2: Optional[str]
#     type_of_relieving_2: Optional[str]
#     date_of_relieving_2: Optional[date]
#     reported_by_2: Optional[str]
#     relieving_remark_2: Optional[str]
#     type_of_allegation_2: Optional[str]
#
#     nop_oi: Optional[str]
#     case_or_claimno: Optional[str]
#
# class UpdateAlert(BaseModel):
#     alert_id: Optional[int] = None  # required to identify existing row
#     alert_from: Optional[str]
#     terminated_by: Optional[str]
#     asked_to_resign_by: Optional[str]
#     relieved_from: Optional[str]
#     resigned_from: Optional[str]
#     police_complaint_by: Optional[str]
#     complaint_ps_name: Optional[str]
#     complaint_date: Optional[date]
#     fir_by: Optional[str]
#     fir_ps_name: Optional[str]
#     fir_date: Optional[date]
#     what: Optional[str]
#     when_info: Optional[str]
#     by_whom: Optional[str]
#     information_date: Optional[date]
#     information_source_type: Optional[str]
#     entry_type: Optional[str]
#
# class UpdateUserData(BaseModel):
#     personal_data: Optional[UpdatePersonalData] = None
#     contact: Optional[UpdateContact] = None
#     professional_history: Optional[List[UpdateProfessionalHistory]] = None
#     alert: Optional[List[UpdateAlert]] = None


from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

class UpdatePersonalData(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    pan_card: Optional[str] = None
    aadhaar_card: Optional[str] = None
    driving_license: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    taluka: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None

class UpdateContact(BaseModel):
    mob_1: Optional[int] = None
    mob_2: Optional[int] = None
    mob_3: Optional[int] = None
    email_1: Optional[str] = None
    email_2: Optional[str] = None
    email_3: Optional[str] = None

class UpdateProfessionalHistory(BaseModel):
    agency_name_1: Optional[str] = None
    agency_owner_1: Optional[str] = None
    reporting_head_1: Optional[str] = None
    type_of_relieving_1: Optional[str] = None
    date_of_relieving_1: Optional[date] = None
    reported_by_1: Optional[str] = None
    relieving_remark_1: Optional[str] = None
    type_of_allegation_1: Optional[str] = None

    agency_name_2: Optional[str] = None
    agency_owner_2: Optional[str] = None
    reporting_head_2: Optional[str] = None
    type_of_relieving_2: Optional[str] = None
    date_of_relieving_2: Optional[date] = None
    reported_by_2: Optional[str] = None
    relieving_remark_2: Optional[str] = None
    type_of_allegation_2: Optional[str] = None

    nop_oi: Optional[str] = None
    case_or_claimno: Optional[str] = None

class UpdateAlert(BaseModel):
    alert_from: Optional[str] = None
    terminated_by: Optional[str] = None
    asked_to_resign_by: Optional[str] = None
    relieved_from: Optional[str] = None
    resigned_from: Optional[str] = None
    police_complaint_by: Optional[str] = None
    complaint_ps_name: Optional[str] = None
    complaint_date: Optional[date] = None
    fir_by: Optional[str] = None
    fir_ps_name: Optional[str] = None
    fir_date: Optional[date] = None
    what: Optional[str] = None
    when_info: Optional[str] = None
    by_whom: Optional[str] = None
    information_date: Optional[date] = None
    information_source_type: Optional[str] = None
    entry_type: Optional[str] = None

class UpdateUserData(BaseModel):
    personal_data: Optional[UpdatePersonalData] = None
    contact: Optional[UpdateContact] = None
    professional_history: Optional[List[UpdateProfessionalHistory]] = None
    alert: Optional[List[UpdateAlert]] = None
