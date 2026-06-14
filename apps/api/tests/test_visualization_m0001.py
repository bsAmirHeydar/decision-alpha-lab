from fastapi.testclient import TestClient

from apps.api.main import app

client = TestClient(app)


def test_m0001_visualization_contract_or_missing_data():
    response = client.get("/api/visualizations/m0001")
    assert response.status_code in {200, 404}
    if response.status_code == 404:
        return
    data = response.json()
    assert data["dataset"]["symbol"]
    assert isinstance(data["candles"], list)
    assert isinstance(data["overlay_layers"], list)
    assert isinstance(data["tables"], list)
    assert "stats" in data
