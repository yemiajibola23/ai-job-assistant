from enum import Enum
from backend.utils.constants import APPLICATION_STATUSES

class ApplicationStatus(Enum):
    INTERESTED = APPLICATION_STATUSES[0]
    APPLIED = APPLICATION_STATUSES[1]
    INTERVIEW = APPLICATION_STATUSES[2]
    OFFER = APPLICATION_STATUSES[3]
    REJECTED = APPLICATION_STATUSES[4]
    SAVED = APPLICATION_STATUSES[5]

    

    @classmethod
    def from_value(cls, value: str) -> "ApplicationStatus":
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise ValueError(f"Invalid application status: {value}")