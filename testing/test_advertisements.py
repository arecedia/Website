import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel

from webapp.main import app
from webapp.database import get_session, engine, connect_args
from webapp.models.Advertisement_models import Advertisement
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
Advertisement = {
    "client_name": "Test Client",
    "ad_title": "Test Ad Title",
    "ad_content": "<p>Test Ad Content</p>",
    "start_date": "2024-12-10T08:00:00",
    "end_date": "2024-12-31T23:59:59",
    "status": "active",
    "ad_type": "banner",
    "target_url": "https://testurl.com",
    "placement": "homepage",
    "media_url": "https://testurl.com/image.jpg",
    "budget": 1000.0
}

# Helper to create an advertisement
def create_test_ad(session):
    ad = Advertisement(**Advertisement)
    session.add(ad)
    session.commit()
    session.refresh(ad)
    return ad

# Core Function Tests
def test_create_advertisement():
    response = client.post("/api/ads/", json=Advertisement)
    print(response.json())

    assert response.status_code == 200

    response_data = response.json()
    assert response_data["message"] == "Advertisement created successfully"
    assert response_data["data"] == Advertisement

"""
def test_update_advertisement():
    response = client.post("/api/ads/{ad_id}", json=



def test_delete_advertisement():



# API Route Tests

def test_create_ad_route():



def test_update_ad_route():



def test_delete_ad_route():



def test_get_all_ads_route():
"""