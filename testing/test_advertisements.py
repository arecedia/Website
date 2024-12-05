import pytest
from Tools.scripts.patchcheck import status
from fastapi.testclient import TestClient
from datetime import datetime

from sqlalchemy import True_
from sqlmodel import Session, create_engine, SQLModel

from webapp.main import app
from webapp.database import get_session, engine, connect_args
from webapp.routes.API_Routes import create_advertisement, update_advertisement, delete_advertisement

TEST_DATABASE_URL = "sqlite:///test_database.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

# Initialize the database
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

# Test client
client = TestClient(app)

# Sample Advertisement Data
sample_ad = {
    "client_name": "Test Client",
    "ad_title": "Test Ad Title",
    "ad_content": "<p>Test Ad Content</p>",
    "start_date": "2024-12-10T08:00:00",
    "end_date": "2024-12-31T23:59:59",
    "status": "active",

}