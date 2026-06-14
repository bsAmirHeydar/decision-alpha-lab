from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from apps.api.services.visualization_m0001 import load_m0001_visualization

router = APIRouter(prefix="/api/visualizations", tags=["visualizations"])


@router.get("/m0001")
def get_m0001_visualization(
    symbol: str = "GOLD",
    timeframe: str = "M15",
    L: int = 5,
    zone_ratio: float = 0.9,
    exit_gap: int = 6,
    consumption_mode: str = "hunt",
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
