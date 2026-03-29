from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import datetime 

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    # Logic: This link connects the event to a specific user ID
    owner_id = Column(Integer, ForeignKey("users.id")) 
    date = Column(String,nullable=True)
    
    # Logic: Automatically records the exact time you hit 'Execute'
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))