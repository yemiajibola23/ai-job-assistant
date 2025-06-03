from enum import Enum

class ApplicationStatus(Enum):
    INTERESTED = "Interested"
    APPLIED = "Applied"
    INTERVIEW = "Interviewing"
    OFFER = "Offer received"
    REJECTED = "Rejected"
    SAVED = "Saved"

    

    @classmethod
    def from_value(cls, value: str) -> "ApplicatonStatus":
        for member in cls:
            if member.value.lower() == value.lower():
                return member
            raise ValueError(f"Invalid application status: {value}")