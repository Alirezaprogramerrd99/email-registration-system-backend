from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    pass

# for returing when we want to retrive it from the database and wrap it into the JSON.
class User(UserBase):
    id: int
    registered_at: datetime

    class Config:
        orm_mode: True

class LetterBase(BaseModel):
    title: str
    content: str

class LetterCreate(LetterBase):
    pass

# for returing when we want to retrive it from the database and wrap it into the JSON.
class Letter(LetterBase):   
    id: int
    title: str
    content: str
    created_at: datetime
    sent: bool
    # user_id: Optional[int]

    class Config:
        orm_mode: True