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
sample_ad = {
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
    ad = Advertisement(**sample_ad)
    session.add(ad)
    session.commit()
    session.refresh(ad)
    return ad

# Core Function Tests
def test_create_advertisement():
    response = client.post("/ads/", json=sample_ad)
    assert response.status_code == 200
    new_ad = response.json()
    assert new_ad["id"] is not None
    assert new_ad["client_name"] == "Test Client"


def test_update_advertisement():
    with Session(engine) as session:
        ad = create_test_ad(session)
        updates = {"ad_title": "Updated Test Ad Title"}
        updated_ad = update_advertisement(session, ad.id, updates)
        assert updated_ad.ad_title == "Updated Test Ad Title"


def test_delete_advertisement():
    with Session(engine) as session:
        ad = create_test_ad(session)
        delete_advertisement(session, ad.id)
        assert session.get(Advertisement, ad.id) is None


# API Route Tests

def test_create_ad_route():
    response = client.post("/ads/", json=sample_ad)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["client_name"] == "Test Client"


def test_update_ad_route():
    # First create an add
    create_response = client.post("/ads/", json=sample_ad)
    ad_id = create_response.json()["id"]

    # Update the ad
    updates = {"ad_title": "Updated Test Ad Title"}
    update_response = client.put(f"/ads/{ad_id}", json=updates)
    assert update_response.status_code == 200
    updated_ad = update_response.json()
    assert updated_ad["ad_title"] == "Updated Test Ad Title"


def test_delete_ad_route():
    # First create an ad
    create_response = client.post("/ads/", json=sample_ad)
    ad_id = create_response.json()["id"]

    # Delete the ad
    delete_response = client.delete(f"/ads/{ad_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Advertisement deleted successfully"

    # Verify deletion
    get_response = client.get(f"/ads/{ad_id}")
    assert get_response.status_code == 404


def test_get_all_ads_route():
    # Clean database
    with Session(engine) as session:
        session.query(Advertisement).delete()
        session.commit()

    # Create multiple ads
    client.post("/ads/", json=sample_ad)
    client.post("/ads/", json={**sample_ad, "client_name": "Another Client"})

    # Fetch all ads
    response = client.get("/ads/")
    assert response.status_code == 200
    ads = response.json()
    assert len(ads) == 2
    assert ads[0]["client_name"] == "Test Client"
    assert ads[1]["client_name"] == "Another Client"