from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_create_review():
    review_data = {
        "sandwich_id": 1,
        "rating": 4.5,
        "comment": "Delicious sandwich!"
    }
    response = client.post("/reviews/", json=review_data)
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == review_data["rating"]
    assert data["comment"] == review_data["comment"]

def test_read_all_reviews():
    response = client.get("/reviews/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
