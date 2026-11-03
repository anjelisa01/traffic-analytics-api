from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel):
    event_type:str
    page:str
    timestamp:datetime

class EventUpdate(BaseModel):
    event_type:str | None=None
    page:str | None=None