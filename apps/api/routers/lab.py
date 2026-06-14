from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from apps.api.services.research_registry import (
    build_graph,
    docs_to_dicts,
    entities_to_dicts,
    get_entity,
    list_documents,
    list_entities,
    list_runs,
    list_stages,
    overview,
    read_document,
    runs_to_dicts,
)

router = APIRouter(prefix="/api/lab", tags=["lab"])


@router.get("/overview")
def get_lab_overview():
    return overview()


@router.get("/stages")
def get_lab_stages():
    return {"stages": list_stages()}


@router.get("/catalog")
def get_lab_catalog(stage_id: str | None = "all", q: str | None = Query(default=None)):
    documents = docs_to_dicts(list_documents(stage_id=stage_id, query=q))
    return {
        "documents": documents,
        "selected_document_path": documents[0]["path"] if documents else None,
    }


@router.get("/document")
def get_lab_document(path: str):
    try:
        return read_document(path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Document not found: {path}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/entities")
def get_entities(entity_type: str | None = "all", q: str | None = Query(default=None)):
    return {"entities": entities_to_dicts(list_entities(entity_type=entity_type, query=q))}


@router.get("/entities/{entity_id}")
def get_entity_detail(entity_id: str):
    entity = get_entity(entity_id)
    if entity is None:
        raise HTTPException(status_code=404, detail=f"Entity not found: {entity_id}")
    return {"entity": entity}


@router.get("/graph")
def get_graph():
    return build_graph()


@router.get("/runs")
def get_runs(entity_id: str | None = "all"):
    return {"runs": runs_to_dicts(list_runs(entity_id=entity_id))}
