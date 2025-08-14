from pydantic import BaseModel


class MessageCreate(BaseModel):
    text: str


class MessageRead(BaseModel):
    text: str
    sent_from: int


class MessageUpdatePartial(BaseModel):
    text: str


class MessageUpdateFull(BaseModel):
    text: str
