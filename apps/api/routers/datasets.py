from __future__ import annotations

from fastapi import APIRouter

from apps.api.services.catalog import list_cached_datasets

router = APIRouter(tags=["datasets"])


@router.get("/datasets")
def datasets() -> dict:
    return {"datasets": list_cached_datasets()}
