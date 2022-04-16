import config
import pytest
from bson import ObjectId
from src.app_factory import create_app
from src.utils.models import Review, Spot


@pytest.fixture()
def app():
    app = create_app(config.TestingConfig)
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def clear_db(app):
    # Very important to keep app as parameter, or else this will may run connected to the base DB
    Spot.objects.all().delete()
    yield
    Spot.objects.all().delete()


def test_get_all(client):
    spot = Spot(name="Test Spot Get All", description="Test Description")
    spot.save()
    response = client.get("/api/spots")
    assert (
        response.status_code == 200
        and len(response.json) == 1
        and response.json[0]["name"] == "Test Spot Get All"
    )


def test_get_one(client):
    spot = Spot(name="Test Spot Get One", description="Test Description 2")
    spot.save()
    response = client.get(f"/api/spots/{spot._id}")
    assert response.status_code == 200 and response.json["name"] == "Test Spot Get One"


def test_get_one_with_reviews(client):
    spot = Spot(
        name="Test Spot Get One With Reviews",
        description="Test Description",
        reviews=[Review(author="Test Author", rating=5.0)],
    )
    spot.save()
    response = client.get(f"/api/spots/{spot._id}")
    assert (
        response.status_code == 200
        and response.json["reviews"][0]["author"] == "Test Author"
    )


def test_get_nonexistent(client):
    response = client.get(f"/api/spots/{ObjectId()}")
    assert response.status_code == 404


def test_post_one(client):
    response = client.post(
        "/api/spots",
        json={"name": "Test Spot Post One", "description": "Test Description"},
    )
    assert response.status_code == 200
    spot = Spot.objects.get({"_id": ObjectId(response.json["_id"])})
    assert spot.name == response.json["name"]


def test_post_missing_params(client):
    response = client.post(
        "/api/spots",
        json={"description": "Test Description"},
    )
    assert response.status_code == 400
    assert response.json["message"] == "Missing parameters"


def test_delete_one(client):
    spot = Spot(name="Test Spot Delete One 1", description="Test Description")
    spot.save()
    spot2 = Spot(name="Test Spot Delete One 2", description="Test Description")
    spot2.save()
    response = client.delete(f"/api/spots/{spot._id}")
    assert response.status_code == 204
    assert Spot.objects.get({"_id": spot2._id})
    with pytest.raises(Spot.DoesNotExist) as excinfo:
        Spot.objects.get({"_id": spot._id})


def test_delete_nonexistent(client):
    spot = Spot(name="Test Spot Delete Nonexistent", description="Test Description")
    spot.save()
    response = client.delete(f"/api/spots/{ObjectId()}")
    assert response.status_code == 204
    assert Spot.objects.get({"_id": spot._id})


def test_put(client):
    spot = Spot(
        name="Test Spot Put Unchanged",
        description="Test Description",
        reviews=[Review()],
    )
    spot.save()
    response = client.put(
        f"/api/spots/{spot._id}",
        json={"name": "Test Spot Put Changed", "description": "Test Description"},
    )
    assert response.status_code == 200
    changed = Spot.objects.get({"_id": spot._id})
    assert (
        changed.name == "Test Spot Put Changed"
        and changed.description == "Test Description"
        and not changed.reviews
    )


def test_put_reviews(client):
    spot = Spot(name="Test Spot Put Unchanged", description="Test Description")
    spot.save()
    response = client.put(
        f"/api/spots/{spot._id}",
        json={
            "name": "Test Spot Put Changed",
            "description": "Test Description",
            "reviews": [{"author": "Test Author", "rating": 5.0}],
        },
    )
    assert response.status_code == 200
    changed = Spot.objects.get({"_id": spot._id})
    assert (
        changed.name == "Test Spot Put Changed"
        and changed.description == "Test Description"
        and len(changed.reviews) == 1
        and changed.reviews[0].author == "Test Author"
    )


def test_put_nonexistent(client):
    response = client.put(
        f"/api/spots/{ObjectId()}",
        json={"name": "Test Spot Put Changed", "description": "Test Description"},
    )
    assert response.status_code == 200
    spot = Spot.objects.get({"_id": ObjectId(response.json["_id"])})
    assert spot.name == response.json["name"]


def test_patch(client):
    spot = Spot(name="Test Spot Patch", description="Test Description")
    spot.save()
    response = client.patch(
        f"/api/spots/{spot._id}",
        json={"description": "Changed Description"},
    )
    assert response.status_code == 200
    changed = Spot.objects.get({"_id": spot._id})
    assert (
        changed.name == "Test Spot Patch"
        and changed.description == "Changed Description"
    )


def test_patch_reviews(client):
    spot = Spot(name="Test Spot Patch", description="Test Description")
    spot.save()
    response = client.patch(
        f"/api/spots/{spot._id}",
        json={"reviews": [{"author": "Test Author", "rating": 5.0}]},
    )
    assert response.status_code == 200
    changed = Spot.objects.get({"_id": spot._id})
    assert (
        changed.name == "Test Spot Patch"
        and changed.description == "Test Description"
        and len(changed.reviews) == 1
        and changed.reviews[0].author == "Test Author"
    )


def test_patch_nonexistent(client):
    response = client.patch(
        f"/api/spots/{ObjectId()}",
        json={"description": "Test Description"},
    )
    assert response.status_code == 404
