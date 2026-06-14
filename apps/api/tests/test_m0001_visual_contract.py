import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apps.api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_m0001_replay_contract_cache_gold_m15():
    response = client.get(
        "/replay/M0001",
        params={
            "symbol": "GOLD",
            "timeframe": "M15",
            "L": 5,
            "zone_ratio": 0.9,
            "exit_gap": 6,
            "consumption_mode": "hunt",
            "source": "cache",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["dataset"]["symbol"] == "GOLD"
    assert payload["dataset"]["timeframe"] == "M15"
    assert len(payload["candles"]) == 5000
    assert len(payload["layers"]) >= 5
    assert len(payload["tables"]) >= 2
    assert payload["dataset"]["parameters"]["events"] > 0
    assert payload["dataset"]["parameters"]["confirmed_nodes"] > 0

    event_table = next(table for table in payload["tables"] if table["table_id"] == "M0001:events")
    assert event_table["rows"]
    first_event = event_table["rows"][0]
    assert "selection_ref" in first_event
    assert first_event["entry_index"] > 0
    assert first_event["exit_index"] >= first_event["entry_index"]
