from pydantic import BaseModel, field_validator

banned_words = []


class CommentRead(BaseModel):
    text: str


class CommentCreate(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, val: str) -> str | ValueError:
        if len(val) >= 3000:
            raise ValueError("Your commentary must not exceed 3000 characters.")
        for i in val:
            if i in banned_words:
                raise ValueError("Your commentary includes inappropriate words.")
        return val


class CommentUpdatePartial(CommentCreate):
    pass


class CommentUpdateFull(CommentCreate):
    pass
