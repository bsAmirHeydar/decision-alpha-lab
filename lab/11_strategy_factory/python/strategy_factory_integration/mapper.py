from __future__ import annotations
from .enums import CanonicalDirection, LegacyDirection
from .hashing import canonical_hash, stable_id
from .models import AdapterConfig, CanonicalAnatomyEvent, LegacyDivergenceCandidate, MappingRecord

PRODUCER_ID = "sf20.exp0017.temporal_intermarket_divergence"
PRODUCER_VERSION = "1.0.0"

def _cluster_id(c: LegacyDivergenceCandidate) -> str:
    payload = "|".join((c.group_name,str(c.group_minutes),str(c.trading_day_start_ny_s),str(c.current_cycle_start_ny_s),str(c.reference_cycle_start_ny_s),c.direction.value,c.side.value))
    return stable_id("cluster", payload)

def _parent_id(c: LegacyDivergenceCandidate) -> str:
    return stable_id("parent", "|".join((c.group_name,str(c.trading_day_start_ny_s),str(c.reference_cycle_start_ny_s))))

def _source_hash(c: LegacyDivergenceCandidate) -> str:
    # Deliberately identity-stable while current extremes evolve intracycle.
    return stable_id("src", c.identity_payload)

def map_candidate(c: LegacyDivergenceCandidate, config: AdapterConfig, known_time_ms: int,
                  strategy_id: str = "exp0017_cycle_group_divergence",
                  strategy_version: str = "1.0.0") -> tuple[CanonicalAnatomyEvent, MappingRecord]:
    if known_time_ms <= 0: raise ValueError("known_time_ms must be positive")
    direction = CanonicalDirection.LONG if c.direction == LegacyDirection.BUY else CanonicalDirection.SHORT
    cluster = _cluster_id(c)
    source = _source_hash(c)
    event = CanonicalAnatomyEvent(
        schema_name="alpha_lab.strategy_factory/anatomy_event",
        schema_version="1.0.0",
        event_id="pending",
        strategy_id=strategy_id,
        strategy_version=strategy_version,
        producer_id=PRODUCER_ID,
        producer_version=PRODUCER_VERSION,
        symbol=c.clean_symbol,
        reference_symbol=c.hunter_symbol,
        direction=direction,
        event_time_ms=known_time_ms,
        known_time_ms=known_time_ms,
        confirmation_time_ms=known_time_ms,
        reference_price=c.clean_reference_price,
        invalidation_price=c.clean_stop_reference_price,
        timeframe_seconds=c.group_minutes * 60,
        session_id=stable_id("nytd", str(c.trading_day_start_ny_s)),
        parent_event_id=_parent_id(c),
        market_event_cluster_id=cluster,
        source_hash=source,
        anatomy_state="exp0017_raw_divergence_candidate_unconfirmed_trade",
    )
    object.__setattr__(event, "event_id", event.derived_event_id)
    mapping = MappingRecord(
        mapping_id=stable_id("sf20map", "|".join((c.divergence_id,event.event_id,str(known_time_ms),config.config_hash))),
        legacy_divergence_id=c.divergence_id,
        legacy_payload_hash=c.payload_hash,
        canonical_event_id=event.event_id,
        canonical_source_hash=event.source_hash,
        cluster_id=event.market_event_cluster_id,
        mapped_at_utc_ms=known_time_ms,
        adapter_config_hash=config.config_hash,
        adapter_version=config.adapter_version,
        reasons=("legacy_raw_candidate","trade_confirmation_not_inferred","clean_symbol_is_trade_symbol"),
    )
    return event, mapping
