# app/models/user.py
from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String,unique=True,index=True,nullable=False)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String,nullable=False) # Never store plain text!

    events = relationship("event",back_populates="owner")