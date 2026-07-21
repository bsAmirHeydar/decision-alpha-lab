from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

from .io import iter_jsonl

@dataclass(frozen=True)
class Resolution:
    consumer_id: str
    resolved_locator: str
    primary_mode: str
    fallback_locator: str | None
    cutover_state: str
    runtime_authority: bool
    live_order_authority: bool
    capital_authority: bool

class ConsumerLocatorResolver:
    def __init__(self, bindings_path: Path):
        self._bindings = {row["consumer_id"]: row for row in iter_jsonl(bindings_path)}

    def resolve(self, consumer_id: str) -> Resolution:
        row = self._bindings[consumer_id]
        return Resolution(
            consumer_id=consumer_id,
            resolved_locator=row["active_locator"],
            primary_mode=row["resolution_mode"],
            fallback_locator=row.get("legacy_fallback_locator"),
            cutover_state=row["cutover_state"],
            runtime_authority=bool(row["runtime_authority"]),
            live_order_authority=bool(row["live_order_authority"]),
            capital_authority=bool(row["capital_authority"]),
        )
