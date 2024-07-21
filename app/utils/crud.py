from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.model import models
from app.utils import schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session):
    return db.query(models.User).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user_by_email(db: Session, email: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    db.delete(db_user)
    db.commit()
    return db_user

# ------------------------------------- Letters Crud -------------------------------

def get_letter(db: Session, letter_id: int):
    return db.query(models.Letter).filter(models.Letter.id == letter_id).first()

def get_letters_pagination(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Letter).offset(skip).limit(limit).all()

def get_letters(db: Session):
    return db.query(models.Letter).all()

def create_letter(db: Session, letter: schemas.LetterCreate, user_id: int):
    # db_letter = models.Letter(**letter.dict(), user_id=user_id)
    db_letter = models.Letter(**dict(letter), user_id=user_id)
    db.add(db_letter)
    db.commit()
    db.refresh(db_letter)
    return db_letter

def mark_letter_as_sent(db: Session, letter_id: int):
    letter = db.query(models.Letter).get(letter_id)
    if letter:
        letter.sent = True
        db.commit()

def get_unsent_latters(db: Session):
    return db.query(models.Letter).filter(models.Letter.sent == False).all()

def get_letters_from_last_month(db: Session):
    # one_month_ago = datetime.utcnow() - timedelta(days=30)
    one_month_ago = datetime.now(timezone.utc) - timedelta(days=30)
    return db.query(models.Letter).filter(models.Letter.created_at >= one_month_ago).all()

def get_users_pagination(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def delete_letter(db: Session, letter_id: int):
    db_letter = db.query(models.Letter).filter(models.Letter.id == letter_id).first()
    db.delete(db_letter)
    db.commit()
    return db_letter
