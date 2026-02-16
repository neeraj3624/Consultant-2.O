from sqlalchemy import Boolean, Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

import datetime

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,index=True,nullable=False)
    hashed_password=Column(String,nullable=False)
    tasks=relationship('Task',back_populates='owner',cascade='all,delete-orphan')
    
class Task(Base):
    __tablename__='tasks'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    description=Column(String,default="")
    completed=Column(Boolean,default=False)
    created_at=Column(DateTime,default=datetime.datetime.utcnow)
    owner_id=Column(Integer,ForeignKey("users.id"))
    owner=relationship("User",back_populates="tasks")