from fastapi.testclient import TestClient

from apps.api.main import app

client = TestClient(app)


def test_lab_overview_has_registry():
    response = client.get("/api/lab/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["stats"]["documents"] > 0
    assert "lineage" in data
    assert isinstance(data["recent_runs"], list)


def test_catalog_autoselects_document():
    response = client.get("/api/lab/catalog")
    assert response.status_code == 200
    data = response.json()
    assert data["documents"]
    assert data["selected_document_path"]


def test_document_reader_loads_first_document():
    catalog = client.get("/api/lab/catalog").json()
    path = catalog["selected_document_path"]
    response = client.get("/api/lab/document", params={"path": path})
    assert response.status_code == 200
    data = response.json()
    assert data["content"]
    assert data["doc"]["path"] == path


def test_entities_include_m0001_or_docs():
    response = client.get("/api/lab/entities")
    assert response.status_code == 200
    data = response.json()
    assert data["entities"]
    ids = {entity["id"] for entity in data["entities"]}
    assert "M0001" in ids or any(entity["entity_type"] == "metric" for entity in data["entities"])
