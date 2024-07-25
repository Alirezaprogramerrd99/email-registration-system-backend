from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import app.database as database
from app.database import engine
from app.model.models import Base
from app.utils import crud, schemas
from app.celery_worker import check_and_send_emails, send_past_emails_to_new_user

from fastapi.middleware.cors import CORSMiddleware

# Create tables if they don't exist
# Base.metadata.create_all(bind=engine)

app = FastAPI()

# Set up CORS
origins = [
    "http://localhost:3000",  # React app running on this origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.post("/users/create/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud.create_user(db=db, user=user)
    send_past_emails_to_new_user.delay(new_user.id)
    return new_user

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/read/", response_model=List[schemas.User])
def read_users_pagination(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    users = crud.get_users_pagination(db, skip=skip, limit=limit)
    if users is None:
        raise HTTPException(status_code=404, detail="No user found")
    return users

@app.delete("/users/delete-all", response_model=dict)
def delete_all_users(db: Session = Depends(database.get_db)):
    crud.delete_all_users(db)
    return {"detail": "All users deleted"}


@app.delete("/users/{user_email}", response_model=schemas.User)
def delete_user_using_email(user_email: str, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    deleted_user = crud.delete_user_by_email(db, email=user_email)
    return deleted_user

#--------------------------- Letters' Endpoints --------------------------------------

@app.post("/letters/create", response_model=schemas.Letter)
def create_letter(letter: schemas.LetterCreate, db: Session = Depends(database.get_db)):
    check_and_send_emails()
    return crud.create_letter(db=db, letter=letter)

@app.get("/letters/read", response_model=List[schemas.Letter])
def read_letters_pagination(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    letters = crud.get_letters_pagination(db, skip=skip, limit=limit)
    if letters is None:
        raise HTTPException(status_code=404, detail="No letter found")
    return letters

@app.get("/letters/unsent", response_model=List[schemas.Letter])
def get_all_unsent_letters(db: Session = Depends(database.get_db)):
    unsent_letters = crud.get_unsent_latters(db)
    if unsent_letters is None:
        raise HTTPException (status_code=404, detail="No unsent letter found")
    return unsent_letters

@app.delete("/letters/delete-all", response_model=dict)
def delete_all_letters(db: Session = Depends(database.get_db)):
    crud.delete_all_letters(db)
    return {"detail": "All letters deleted"}

@app.delete("/letters/{letter_id}", response_model=schemas.Letter)
def delete_letter_from_system(letter_id: int, db: Session = Depends(database.get_db)):

    db_letter = crud.get_letter(db, letter_id=letter_id)
    if db_letter is None:
        raise HTTPException(status_code=404, detail="Letter not found")
    deleted_letter = crud.delete_letter(db, letter_id=letter_id)
    return deleted_letter


    
    
