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
    "budget": 1000.0,
    "cost_per_click": 0.1,
    "cost_per_impression": 0.1,
    "target_audience": "adult",
    "media_url": "https://testurl.com/ad.jpg",
    "created_at": "2024-12-10T06:00:00"
}

AdvertisementUpdate = {
    "client_name": "New Test Client",
    "ad_title": "New Test Title",
    "ad_content": "<p>New Test Ad Content</p>",
    "status": "inactive",
    "end_date": "2024-12-30T23:59:59",
    "ad_type": "video",
    "target_url": "https://newtesturl.com",
    "placement": "Story_1",
    "media_url": "https://newtesturl.com/new_image.jpg",
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
    # Sample Advertisement data
    advertisement_data = {
        "client_name": "John Doe",
        "ad_title": "Holiday Sale",
        "ad_content": "Big discounts on electronics!",
        "start_date": "2024-12-20T00:00:00",
        "end_date": "2025-01-05T23:59:59",
        "status": "active",
        "ad_type": "banner",
        "target_url": "https://example.com",
        "placement": "homepage",
        "budget": 1000.0,
        "cost_per_click": 0.5,
        "cost_per_impression": 0.1,
        "target_audience": "18-35",
        "media_url": "https://example.com/banner.jpg",
        "created_at": "2024-12-15T12:00:00"
    }

    print(f"Advertisement data: {advertisement_data}")

    # Make the POST request
    response = client.post("/api/ads/", json=advertisement_data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    response_data = response.json()

    # Debug output
    print("Response JSON:", response_data)

    # Assertions
    for key in advertisement_data:
        assert response_data.get(key) == advertisement_data[key], f"Mismatch for field: {key}"


def test_update_advertisement():
    ad_id = "existing-ad-id" # Replace when first ad created
    response = client.put(f"/api/ads/{ad_id}", json=AdvertisementUpdate)
    print(response.json)

    assert response.status_code == 200

    response_data = response.json()
    assert response_data["message"] == "Advertisement updated successfully"
    assert response_data["updated_info"]["client_name"] == AdvertisementUpdate["client_name"]

"""
def test_delete_advertisement():



# API Route Tests

def test_create_ad_route():



def test_update_ad_route():



def test_delete_ad_route():



def test_get_all_ads_route():
"""