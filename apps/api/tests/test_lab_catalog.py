from fastapi.testclient import TestClient

from apps.api.main import app

client = TestClient(app)


def test_lab_overview_exposes_research_stages():
    response = client.get("/api/lab/overview")
    assert response.status_code == 200
    payload = response.json()
    assert payload["stats"]["documents"] > 0
    assert any(stage["stage_id"] == "hypotheses" for stage in payload["stages"])
    assert payload["critical_path"][0]["id"].startswith("OBS")


def test_document_reader_returns_markdown_content():
    catalog = client.get("/api/lab/catalog", params={"stage_id": "hypotheses"})
    assert catalog.status_code == 200
    documents = catalog.json()["documents"]
    assert documents
    document = client.get("/api/lab/document", params={"path": documents[0]["path"]})
    assert document.status_code == 200
    payload = document.json()
    assert payload["doc"]["stage_id"] == "hypotheses"
    assert isinstance(payload["content"], str)
    assert payload["content"]
