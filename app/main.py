from fastapi import FastAPI
from database import engine
from app.model.models import Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()