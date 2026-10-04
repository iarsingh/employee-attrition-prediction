from fastapi.testclient import TestClient
from attrition.main import app

client = TestClient(app)


def test_high_and_low():
    assert client.post("/score", json={'overtime_hours': 20, 'tenure_months': 3, 'commute_km': 40}).json()["label"]
    high = client.post("/score", json={'overtime_hours': 20, 'tenure_months': 3, 'commute_km': 40}).json()
    low = client.post("/score", json={'overtime_hours': 0, 'tenure_months': 48, 'commute_km': 5}).json()
    assert high["label"] != low["label"]
    assert high["score"] > low["score"]


def test_missing_is_refused():
    body = dict({'overtime_hours': 20, 'tenure_months': 3, 'commute_km': 40})
    body.pop("overtime_hours")
    assert client.post("/score", json=body).status_code == 422
