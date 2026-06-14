from __future__ import annotations

from fastapi import APIRouter, Query

from apps.api.schemas.visualization import MetricSummary, ReplayPayload
from apps.api.services.m0001_visualization import build_m0001_replay, build_m0001_summary

router = APIRouter(tags=["M0001"])


@router.get("/replay/M0001", response_model=ReplayPayload)
def replay_m0001(
    symbol: str = Query("GOLD"),
    timeframe: str = Query("M15"),
    L: int = Query(5, ge=1, le=100),
    zone_ratio: float = Query(0.9, ge=0.0, le=1.0),
    exit_gap: int = Query(6, ge=1, le=500),
    consumption_mode: str = Query("hunt", pattern="^(hunt|touch)$"),
    source: str = Query("cache"),
    reset_metric_cache: bool = Query(False),
) -> ReplayPayload:
    return build_m0001_replay(
        symbol=symbol,
        timeframe=timeframe,
        L=L,
        zone_ratio=zone_ratio,
        exit_gap=exit_gap,
        consumption_mode=consumption_mode,
        source=source,
        reset_metric_cache=reset_metric_cache,
    )


@router.get("/metrics/M0001/summary", response_model=MetricSummary)
def summary_m0001(
    symbol: str = Query("GOLD"),
    timeframe: str = Query("M15"),
    L: int = Query(5, ge=1, le=100),
    zone_ratio: float = Query(0.9, ge=0.0, le=1.0),
    exit_gap: int = Query(6, ge=1, le=500),
    consumption_mode: str = Query("hunt", pattern="^(hunt|touch)$"),
    source: str = Query("cache"),
    reset_metric_cache: bool = Query(False),
) -> MetricSummary:
    return build_m0001_summary(
        symbol=symbol,
        timeframe=timeframe,
        L=L,
        zone_ratio=zone_ratio,
        exit_gap=exit_gap,
        consumption_mode=consumption_mode,
        source=source,
        reset_metric_cache=reset_metric_cache,
    )
