from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import app.database as database
from app.database import engine
from app.model.models import Base
from app.utils import crud, schemas

# Create tables if they don't exist
# Base.metadata.create_all(bind=engine)

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db=db, user=user)
    # send_past_emails_to_new_user.delay(user.id)
    return user

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/", response_model=List[schemas.User])
def read_users_pagination(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    users = crud.get_users_pagination(db, skip=skip, limit=limit)
    if users is None:
        raise HTTPException(status_code=404, detail="No user found")
    return users


#--------------------------- Letters' Endpoints --------------------------------------

@app.post("/letters/", response_model=schemas.Letter)
def create_letter(letter: schemas.LetterCreate, user_id: int, db: Session = Depends(database.get_db)):
    return crud.create_letter(db=db, letter=letter, user_id=user_id)

@app.get("/letters/", response_model=List[schemas.Letter])
def read_letters_pagination(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    letters = crud.get_letters_pagination(db, skip=skip, limit=limit)
    return letters

@app.get("/letters/", response_model=List[schemas.Letter])
def get_all_unsent_letters(db: Session = Depends(database.get_db)):
    unsent_letters = crud.get_unsent_latters(db)
    if unsent_letters is None:
        raise HTTPException (status_code=404, detail="No unsent letter found")
    return unsent_letters
