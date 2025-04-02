import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_recommend_highlighted():
    query = "machine learning"
    response = client.get(f"/recommend_highlighted/?query={query}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    for item in response.json():
        assert "Title" in item
        assert "Category" in item
        assert "Rating" in item
        assert "Viewers" in item