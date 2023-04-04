from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ..config import DATABASE_URL

# from ..config import DATABASE_URL
from ..database import Base
from ..main import app, get_db


# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
SQLALCHEMY_DATABASE_URL = DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_save_user_dob():
    # Valid input
    response = client.put("/hello/testuser", json={"dateOfBirth": "1990-01-01"})
    assert response.status_code == 204

def test_invalid_username():
    # Invalid username
    response = client.put("/hello/test1", json={"dateOfBirth": "1990-01-03"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Username must contain only letters."}

def test_invalid_dateOfBirth():
    # Invalid dateOfBirth
    response = client.put("/hello/testuser", json={"dateOfBirth": "2024-01-01"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid date of birth."}

def test_get_hello_message():
    dob = datetime.strptime("1990-01-05", "%Y-%m-%d").date()
    client.put("/hello/birthdayuser", json={"dateOfBirth": "1990-01-05"})
    today = datetime.now()
    delta = (datetime(today.year+1, dob.month, dob.day+1) - today).days
    response = client.get("/hello/birthdayuser")
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello, birthdayuser! Your birthday is in {delta} day(s)"}

def test_user_not_found():
    # User not found
    response = client.get("/hello/nonexistentuser")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}

def test_birthday_today():
    # Birthday today
    dob = datetime.now().strftime("%Y-%m-%d")
    response = client.put("/hello/birthdayuser", json={"dateOfBirth": dob})
    assert response.status_code == 204

    response = client.get("/hello/birthdayuser")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, birthdayuser! Happy birthday!"}

def test_birthday_tomorrow():
    # Birthday tomorrow
    dob = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    response = client.put("/hello/birthdayuser", json={"dateOfBirth": dob})
    assert response.status_code == 204

    response = client.get("/hello/birthdayuser")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, birthdayuser! Your birthday is in 1 day(s)"}
