from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

# 1. Logic: Fix the Imports to match your folder structure
from app.database import get_db
from app.routes.auth import get_current_user  # Logic: The 'bouncer' for JWT
from app.models.event import Event            # Logic: The DB table blueprint

router = APIRouter(prefix="/events", tags=["events"])

# --- 1. The Schema (The Contract) ---
class EventCreate(BaseModel):
    title: str  
    date: Optional[str] = None
    description :str

class EventResponse(EventCreate):
    id: int
    user_id: int
    class Config:
        from_attributes = True

# --- 2. The Routes ---

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_in: EventCreate, 
    db: Session = Depends(get_db),              # Logic: Grabs the DB connection
    current_user_id: int = Depends(get_current_user) # Logic: Grabs the User ID from JWT
):
    # 2. Logic: Create the actual DB record
    new_event = Event(
        owner_id=current_user_id, 
        title=event_in.title,
        description=event_in.description,
        date=event_in.date
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event) # Logic: This gives us the 'id' assigned by the DB
    return new_event

@router.get("/", response_model=List[EventResponse])
async def fetch_events(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    # 3. Logic: Filter events so Anshika only sees Anshika's events
    events = db.query(Event).filter(Event.user_id == current_user_id).all()
    return events

@router.delete("/{event_id}")
async def delete_event(
    event_id: int, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    # 4. Logic: Find and Verify ownership before deleting
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if event.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this")
        
    db.delete(event)
    db.commit()
    return {"message": "Event deleted successfully"}