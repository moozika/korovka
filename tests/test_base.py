from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_vibes():
    response = client.get("/api/v1/vibes")
    assert response.status_code == 200
    assert 'name' in response.json()[0].keys()
    assert 'colors' in response.json()[0].keys()
