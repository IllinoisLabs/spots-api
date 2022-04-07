import config
import pytest
from main import create_app
from utils.models import Spot


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
    spot = Spot(name="Test Spot", description="Test Description")
    spot.save()
    response = client.get("/api/spots")
    assert len(response.json) == 1 and response.json[0]["name"] == "Test Spot"
