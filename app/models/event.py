from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, Integer, DateTime
from datetime import datetime
from pydantic import BaseModel, Field

# 1. The Base for all your tables
class Base(DeclarativeBase):
    pass

# 2. The Database Model (The "Physical" Table in Postgres)
class EventModel(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500))
    location: Mapped[str] = mapped_column(String(100))
    # Core Ledger Fields
    available_slots: Mapped[int] = mapped_column(Integer, default=50)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

# 3. The Pydantic Schema (The "Validation" layer for the API)
class EventCreate(BaseModel):
    title: str = Field(..., min_length=3)
    description: str
    location: str
    available_slots: int = Field(ge=1) # Must be at least 1 slot

    class Config:
        from_attributes = True