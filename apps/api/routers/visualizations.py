from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from apps.api.services.visualization_m0001 import (
    compare_actual_to_random,
    load_m0001_random_baseline,
    load_m0001_visualization,
)

router = APIRouter(prefix="/api/visualizations", tags=["visualizations"])


@router.get("/m0001")
def get_m0001_visualization(
    symbol: str = "GOLD",
    timeframe: str = "M15",
    L: int = Query(default=5, ge=1, le=100),
    zone_ratio: float = Query(default=0.9, ge=0.0, le=1.0),
    exit_gap: int = Query(default=6, ge=1, le=500),
    consumption_mode: str = Query(default="hunt", pattern="^(hunt|touch)$"),
    max_bars: int = Query(default=5000, ge=100, le=100000),
):
    try:
        return load_m0001_visualization(
            symbol=symbol,
            timeframe=timeframe,
            L=L,
            zone_ratio=zone_ratio,
            exit_gap=exit_gap,
            consumption_mode=consumption_mode,
            max_bars=max_bars,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/m0001/random-baseline")
def post_m0001_random_baseline(
    symbol: str = "GOLD",
    timeframe: str = "M15",
    L: int = Query(default=5, ge=1, le=100),
    zone_ratio: float = Query(default=0.9, ge=0.0, le=1.0),
    exit_gap: int = Query(default=6, ge=1, le=500),
    consumption_mode: str = Query(default="hunt", pattern="^(hunt|touch)$"),
    max_bars: int = Query(default=5000, ge=100, le=100000),
    seed: int | None = Query(default=None),
    sample_size: int | None = Query(default=None, ge=1, le=10000),
):
    try:
        actual = load_m0001_visualization(
            symbol=symbol,
            timeframe=timeframe,
            L=L,
            zone_ratio=zone_ratio,
            exit_gap=exit_gap,
            consumption_mode=consumption_mode,
            max_bars=max_bars,
        )
        random_payload = load_m0001_random_baseline(
            symbol=symbol,
            timeframe=timeframe,
            L=L,
            zone_ratio=zone_ratio,
            exit_gap=exit_gap,
            consumption_mode=consumption_mode,
            max_bars=max_bars,
            seed=seed,
            sample_size=sample_size,
        )
        random_payload["comparison"] = compare_actual_to_random(actual, random_payload)
        return random_payload
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
