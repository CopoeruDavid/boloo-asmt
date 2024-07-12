# app/schemas.py

from pydantic import BaseModel, HttpUrl
from uuid import UUID
from datetime import datetime

class PollCreate(BaseModel):
    question: str

class OptionCreate(BaseModel):
    poll_id: UUID
    text: str

class OptionVote(BaseModel):
    id: UUID

class TimerResponse(BaseModel):
    id: UUID
    time_left: int
