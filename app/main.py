from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import app.database as database
from app.database import engine
from app.model.models import Base
from app.utils import crud, schemas

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
