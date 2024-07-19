from sqlalchemy.orm import Session

from app.model import models
from app.utils import schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_letters(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Letter).offset(skip).limit(limit).all()

def create_letter(db: Session, letter: schemas.LetterCreate, user_id: int):
    db_letter = models.Letter(**letter.dict(), user_id=user_id)
    db.add(db_letter)
    db.commit()
    db.refresh(db_letter)
    return db_letter