from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from apps.api.services.data_fetch import fetch_market_data, list_cached_datasets

router = APIRouter(prefix="/api/data", tags=["data"])


class FetchDataRequest(BaseModel):
    symbol: str = Field(default="GOLD")
    timeframe: str = Field(default="M15")
    bars: int = Field(default=5000, ge=100, le=500000)
    source: str = Field(default="cache", pattern="^(cache|mt5)$")
    reset_cache: bool = False


@router.get("/datasets")
def get_cached_datasets():
    return {"datasets": list_cached_datasets()}


@router.post("/fetch")
def post_fetch_data(payload: FetchDataRequest):
    try:
        return fetch_market_data(
            symbol=payload.symbol,
            timeframe=payload.timeframe,
            bars=payload.bars,
            source=payload.source,
            reset_cache=payload.reset_cache,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
