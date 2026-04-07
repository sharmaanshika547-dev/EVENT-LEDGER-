from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# 1. Shared fields (Internal Base)
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    date: Optional[datetime] = None

# 2. Schema for Creating an Event (POST)
class EventCreate(EventBase):
    pass 

# 3. Schema for Updating an Event (PATCH/PUT)
class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None

# 4. Schema for the API Response (GET)
class Event(EventBase):
    id: int
    user_id: int # Matches your models/event.py

    # Critical for SQLAlchemy 2.0 compatibility
    model_config = ConfigDict(from_attributes=True)