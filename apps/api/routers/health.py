from __future__ import annotations

from fastapi import APIRouter

from apps.api.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "app": settings.app_name,
        "contract_version": settings.contract_version,
    }
