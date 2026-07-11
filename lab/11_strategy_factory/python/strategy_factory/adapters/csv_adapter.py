"""Reference CSV anatomy adapter used for rapid onboarding and testing."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

import pandas as pd

from .base import AnatomyAdapter
from ..contracts import AnatomyEvent, Direction, FeatureSnapshot, FeatureValue, stable_hash
from ..manifest import StrategyManifest


def _utc(value: Any) -> datetime:
    parsed = pd.Timestamp(value)
    if parsed.tzinfo is None:
        parsed = parsed.tz_localize("UTC")
    return parsed.tz_convert("UTC").to_pydatetime()


class CsvAnatomyAdapter(AnatomyAdapter):
    adapter_id = "csv_anatomy"
    adapter_version = "1.0.0"

    def emit_events(self, source: Any, manifest: StrategyManifest) -> Iterable[AnatomyEvent]:
        frame = source if isinstance(source, pd.DataFrame) else pd.read_csv(source)
        strategy = manifest.section("strategy")
        adapter = manifest.section("anatomy_adapter")
        known_field = str(adapter["known_time_field"])
        event_fields = list(adapter["event_id_fields"])

        for _, row in frame.iterrows():
            raw = row.to_dict()
            direction = Direction(str(raw.get("direction", "neutral")).lower())
            identity_payload = {name: raw.get(name) for name in event_fields}
            event_id = str(raw.get("event_id") or stable_hash(identity_payload, prefix="evt_")[:36])
            event = AnatomyEvent(
                event_id=event_id,
                strategy_id=str(strategy["id"]),
                strategy_version=str(strategy["version"]),
                symbol=str(raw["symbol"]),
                reference_symbol=(None if pd.isna(raw.get("reference_symbol")) else str(raw.get("reference_symbol"))),
                direction=direction,
                event_time_utc=_utc(raw.get("event_time_utc", raw[known_field])),
                known_time_utc=_utc(raw[known_field]),
                confirmation_time_utc=_utc(raw.get("confirmation_time_utc", raw[known_field])),
                reference_price=float(raw["reference_price"]),
                invalidation_price=(
                    None if pd.isna(raw.get("invalidation_price")) else float(raw.get("invalidation_price"))
                ),
                timeframe=(None if pd.isna(raw.get("timeframe")) else str(raw.get("timeframe"))),
                session=(None if pd.isna(raw.get("session")) else str(raw.get("session"))),
                parent_event_id=(None if pd.isna(raw.get("parent_event_id")) else str(raw.get("parent_event_id"))),
                market_event_cluster_id=(
                    None
                    if pd.isna(raw.get("market_event_cluster_id"))
                    else str(raw.get("market_event_cluster_id"))
                ),
                source_hash=stable_hash(identity_payload, prefix="src_"),
                metadata={k: v for k, v in raw.items() if k not in {
                    "event_id", "symbol", "reference_symbol", "direction", "event_time_utc", known_field,
                    "confirmation_time_utc", "reference_price", "invalidation_price", "timeframe", "session",
                    "parent_event_id", "market_event_cluster_id"
                } and not pd.isna(v)},
            )
            event.validate()
            yield event

    def build_snapshot(
        self,
        event: AnatomyEvent,
        source: Any,
        manifest: StrategyManifest,
        decision_time_utc: datetime,
    ) -> FeatureSnapshot:
        feature_map: Mapping[str, Any]
        if isinstance(source, Mapping):
            feature_map = source
        elif isinstance(source, pd.Series):
            feature_map = source.to_dict()
        else:
            raise TypeError("CSV reference adapter snapshot source must be a mapping or Series")

        allowed = list(manifest.section("features")["shared"]) + list(
            manifest.section("features")["strategy_specific"]
        )
        values = []
        for feature_name in allowed:
            raw_value = feature_map.get(feature_name)
            known_field = f"{feature_name}__known_time_utc"
            known_time = _utc(feature_map.get(known_field, decision_time_utc))
            values.append(
                FeatureValue(
                    name=feature_name,
                    value=raw_value,
                    known_time_utc=known_time,
                    source=self.adapter_id,
                    version=self.adapter_version,
                    missing_reason="source_missing" if raw_value is None else None,
                )
            )
        payload = {
            "event_id": event.event_id,
            "decision_time": decision_time_utc.astimezone(timezone.utc).isoformat(),
            "features": [(item.name, item.value, item.known_time_utc.isoformat()) for item in values],
        }
        snapshot = FeatureSnapshot(
            snapshot_id=stable_hash(payload, prefix="snap_")[:40],
            event_id=event.event_id,
            snapshot_time_utc=decision_time_utc,
            features=values,
            schema_version=str(manifest.section("features")["schema_version"]),
            producer_version=self.adapter_version,
        )
        snapshot.validate()
        return snapshot
