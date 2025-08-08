from datetime import date

from pydantic import BaseModel, field_validator


class ProfileReadPublic(BaseModel):
    first_name: str | None
    last_name: str | None
    country: str | None
    sex: str | None
    date_of_birth: date | None
    bio: str | None
    place_of_work: str | None
    place_of_education: str | None
    is_public: bool


class ProfileReadPrivate(BaseModel):
    username: str


class ProfileUpdateFull(ProfileReadPublic):
    @field_validator("first_name", "last_name", "country")
    @classmethod
    def capitalize_field(cls, val: str | None) -> str | None:
        if val:
            return val.capitalize()
        else:
            return val

    @field_validator("sex")
    @classmethod
    def validate_sex(cls, val: str | None) -> str | None:
        if val:
            if val.startswith("m") or val.startswith("M"):
                return "Male"
            elif val.startswith("f") or val.startswith("F"):
                return "Female"
        return val

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, val: date | None) -> date | None | ValueError:
        if val:
            if val > date.today() or val < date(year=1900, month=1, day=1):
                raise ValueError("Incorrect date of birth.")
        return val


class ProfileUpdatePartial(ProfileUpdateFull):
    pass
