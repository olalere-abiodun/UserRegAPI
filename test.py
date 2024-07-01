import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
import crud
import os

# Test Database URL
SQLALCHEMY_DATABASE_URL = os.environ.get('DB_URL')

# Create a test database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)


# Create a test database session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the test database tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    """Yield a new database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()

    # Use the connection with a transaction
    session = TestingSessionLocal(bind=connection)

    yield session  # this is where the testing happens!

    # Rollback - clean up the session
    session.close()
    transaction.rollback()
    connection.close()

def test_create_user():
    response = client.post("/user/", json={
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password_hash": "hashedpassword",
        "first_name": "John",
        "last_name": "Doe"
    })
    assert response.status_code == 200
    assert response.json()["msg"] == "User created successfully"
    assert response.json()["user"]["username"] == "johndoe"

def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)



def test_read_user_by_id():
    # Use the created user's ID to fetch them
    user_id = 1
    
    response = client.get(f"/user/id/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "johndoe"
    assert response.json()["email"] == "johndoe@example.com"

def test_read_user_by_username():
    response = client.get("/user/username/johndoe")
    assert response.status_code == 200
    assert response.json()["username"] == "johndoe"

def test_update_user():
    updated_user_data = {
        "username": "johnnydoe",
        "email": "johnnydoe@example.com",
        "password_hash": "newhashedpassword",
        "first_name": "Johnny",
        "last_name": "Doe"
    }
    response = client.put("/user/Update/johndoe", json=updated_user_data)
    assert response.status_code == 200

    response = client.get("/user/username/johnnydoe")
    assert response.status_code == 200
    assert response.json()["username"] == "johnnydoe"
    assert response.json()["email"] == "johnnydoe@example.com"
