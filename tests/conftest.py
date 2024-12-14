import pytest
from fastapi.testclient import TestClient

from app.db.base import Base, engine
from app.db.session import SessionLocal
from app.schemas.user import UserCreate
from app.services.auth_service import create_user


# Set up and tear down tables for test module
@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Provide a test client
@pytest.fixture(scope="module")
def client():
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client


employee_data = UserCreate(
    username="testuser_employee", password="testpass", role="employee"
)
employer_data = UserCreate(
    username="testuser_employer", password="testpass", role="employer"
)


# Seed a test users into the database before authentication tests
@pytest.fixture(scope="module")
def test_user():
    db = SessionLocal()
    create_user(db, employee_data)
    create_user(db, employer_data)
    db.close()


# Generate an auth token for authenticated tests
@pytest.fixture(scope="function")
def get_auth_token_employee(client: TestClient, test_user):
    response = client.post(
        "/api/v1/login",
        json={
            "username": employee_data.username,
            "password": employee_data.password,
        },
    )
    assert response.status_code == 200, f"Login failed: {response.json()}"
    token = response.json().get("access_token")
    assert token, "Access token not returned"
    if token:
        return token
    return None


# Generate an auth token for authenticated tests
@pytest.fixture(scope="function")
def get_auth_token_employer(client: TestClient, test_user):
    response = client.post(
        "/api/v1/login",
        json={
            "username": employer_data.username,
            "password": employer_data.password,
        },
    )
    assert response.status_code == 200, f"Login failed: {response.json()}"
    token = response.json().get("access_token")
    if token:
        return token
    return None
