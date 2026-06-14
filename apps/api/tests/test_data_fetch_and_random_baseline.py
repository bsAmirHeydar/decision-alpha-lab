from fastapi.testclient import TestClient

from apps.api.main import app

client = TestClient(app)


def test_cache_data_fetch_endpoint_for_default_dataset():
    response = client.post(
        "/api/data/fetch",
        json={"symbol": "GOLD", "timeframe": "M15", "bars": 5000, "source": "cache"},
    )
    assert response.status_code in {200, 404}
    if response.status_code == 200:
        data = response.json()
        assert data["rows"] > 0
        assert data["source"] == "cache"


def test_m0001_random_baseline_contract_or_missing_cache():
    response = client.post("/api/visualizations/m0001/random-baseline?symbol=GOLD&timeframe=M15&L=5&sample_size=25")
    assert response.status_code in {200, 404}
    if response.status_code == 200:
        data = response.json()
        assert data["entity"]["id"] == "M0001_RANDOM_BASELINE"
        assert data["overlay_layers"]
        assert data["tables"]
        assert "comparison" in data
