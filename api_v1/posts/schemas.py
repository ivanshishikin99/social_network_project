from pydantic import BaseModel, field_validator


class PostRead(BaseModel):
    text: str
    tags: str | None


class PostCreate(BaseModel):
    text: str
    tags: str | None = None

    @field_validator("text")
    @classmethod
    def validate_text_field(cls, val: str) -> str | ValueError:
        if len(val) >= 5000:
            raise ValueError("Your post is too long!")
        return val

class PostUpdatePartial(PostCreate):
    pass


class PostUpdateFull(PostCreate):
    pass
