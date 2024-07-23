from sqlalchemy.orm import Session

# from app.model import models
import app
from app.utils import schemas 
from app.utils import crud
import app.database as database

def test_database_operations():
    db = database.SessionLocal()

    # Create a new user
    TEST_EMAIL = "testuser@example.com"
    if crud.get_user_by_email(db, TEST_EMAIL) is not None:
        deleted_user = crud.delete_user_by_email(db, TEST_EMAIL)
        print(f"Deleted User: {deleted_user}")

    user_create = schemas.UserCreate(email=TEST_EMAIL)
    user = crud.create_user(db=db, user=user_create)
    print(f"Created User: {user}")

    # Get user by email
    user = crud.get_user_by_email(db, email=TEST_EMAIL)
    print(f"Fetched User: {user}")

    # Create a new letter
    letter_create = schemas.LetterCreate(title="Test Letter", content="This is a test letter.")
    letter = crud.create_letter(db=db, letter=letter_create)
    print(f"Created Letter: {letter}")

    # Get letters
    letters = crud.get_letters(db)
    print(f"Fetched Letters: {letters}")

    db.close()

if __name__ == "__main__":
    test_database_operations()