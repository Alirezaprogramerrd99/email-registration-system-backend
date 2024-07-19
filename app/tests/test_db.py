from sqlalchemy.orm import Session

# from app.model import models
import app
from app.utils import schemas 
from app.utils import crud
import app.database as database

def test_database_operations():
    db = database.SessionLocal()

    # Create a new user
    user_create = schemas.UserCreate(email="testuser@example.com")
    user = crud.create_user(db=db, user=user_create)
    print(f"Created User: {user}")

    # Get user by email
    user = crud.get_user_by_email(db, email="testuser@example.com")
    print(f"Fetched User: {user}")

    # Create a new letter
    letter_create = schemas.LetterCreate(title="Test Letter", content="This is a test letter.")
    letter = crud.create_letter(db=db, letter=letter_create, user_id=user.id)
    print(f"Created Letter: {letter}")

    # Get letters
    letters = crud.get_letters(db)
    print(f"Fetched Letters: {letters}")

    db.close()

if __name__ == "__main__":
    test_database_operations()