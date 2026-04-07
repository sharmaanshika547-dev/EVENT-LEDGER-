from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

# Import your database and models properly
from .database import get_db
from . import models, schemas  # Assuming you have these files

router = APIRouter()

# 1. READ ALL
@router.get("/events/", response_model=List[schemas.Event])
async def read_events(db: AsyncSession = Depends(get_db)):
    stmt = select(models.Event)
    result = await db.execute(stmt)
    # FIX: Changed 'results' to 'result' and 'scalara' to 'scalars'
    events = result.scalars().all()
    return events 

# 2. READ ONE
@router.get("/events/{event_id}", response_model=schemas.Event)
async def read_event(event_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(models.Event).where(models.Event.id == event_id)
    result = await db.execute(stmt)
    # FIX: Changed 'scalara' to 'scalars'
    event = result.scalars().first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# 3. CREATE
@router.post("/events/", status_code=status.HTTP_201_CREATED)
async def create_event(event_data: schemas.EventCreate, db: AsyncSession = Depends(get_db)):
    # Use .dict() or .model_dump() if using Pydantic v2
    new_event = models.Event(**event.model_dump(),user_id=current_user_id)
    
    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    
    return new_event

@router.put("/events/{event_id}",response_model=schemas.Event)
async def update_event(event_id:int,event_update:schemas.EventUpdate,db:AsyncSession=Depends(get_db)):
    stmt = select(models.Event).where(models.Event.id== event_id)
    result = await db.execute(stmt)
    db_event= result.scalars().first()

    if not db.event:
        raise HTTPException(status_code=404,detail ="event not found")
    
    update_data = event_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event,key, value)

    await db.commit()
    await db.refrsh(db_event)
    return db_event


@router.delete("/events/{event_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id:int,db:AsyncSession=Depends(get_db)):
    stmt = select(models.Event).where(models.Event.id ==event_id)
    result = await db.execute(stmt)
    db_event = result.scalars().first()

    if not db_event:
        raise HTTPException(status_code = 404,detail ="event not found")
    
    await db.delete(db_event)
    await db.commit()

    return None
