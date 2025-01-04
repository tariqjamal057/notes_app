from datetime import date

from pydantic import BaseModel


class NoteRequest(BaseModel):
    title: str
    content: str


class NoteResponse(NoteRequest):
    id: str
    last_update: date
    created_on: date
