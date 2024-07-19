from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    pass

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

class Letter(LetterBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode: True