from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title:str
    description:Optional[str]=None
    completed:bool=False
    
class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    
class Task(TaskBase):
    id:int
    created_at:datetime
    owner_id:int
    class Config:
        from_attributes=True
        
class UserBase(BaseModel):
    username:str
    
    
class UserCreate(UserBase):
    password:str
    
class User(UserBase):
    id:int
    tasks:list[Task]=[]
    class Config:
        from_attributes=True


class Token(BaseModel):
    access_token:str
    token_type:str
    
    
class TokenData(BaseModel):
    username:Optional[str]=None