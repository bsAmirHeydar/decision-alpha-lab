from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .io import iter_jsonl
from .models import Resolution


class CompatibilityRedirectResolver:
    """Resolve exact legacy locators without importing or executing domain code.

    A legacy locator can legitimately identify more than one extracted canonical
    record (for example, multiple visual surfaces discovered under the same
    MQL5 entry point). Such groups are consumer-scoped and must fail closed when
    the caller omits the consumer identity.
    """

    def __init__(self, redirect_records_path: Path):
        rows = list(iter_jsonl(redirect_records_path))
        self._by_key: dict[tuple[str, str], dict] = {}
        grouped: dict[str, list[dict]] = defaultdict(list)
        for row in rows:
            key = (row["legacy_locator"], row["consumer_id"])
            if key in self._by_key:
                raise ValueError("DUPLICATE_CONSUMER_SCOPED_REDIRECT")
            self._by_key[key] = row
            grouped[row["legacy_locator"]].append(row)
        self._by_legacy = {
            locator: tuple(sorted(values, key=lambda item: item["consumer_id"]))
            for locator, values in grouped.items()
        }

    def resolve(self, legacy_locator: str, consumer_id: str | None = None) -> Resolution:
        rows = self._by_legacy.get(legacy_locator)
        if not rows:
            raise KeyError(f"UNKNOWN_LEGACY_LOCATOR:{legacy_locator}")
        if consumer_id is None:
            if len(rows) != 1:
                raise KeyError(f"AMBIGUOUS_LEGACY_LOCATOR:{legacy_locator}")
            row = rows[0]
        else:
            try:
                row = self._by_key[(legacy_locator, consumer_id)]
            except KeyError as exc:
                raise KeyError(
                    f"UNKNOWN_CONSUMER_SCOPED_REDIRECT:{legacy_locator}:{consumer_id}"
                ) from exc
        return Resolution(
            legacy_locator=row["legacy_locator"],
            canonical_locator=row["canonical_locator"],
            canonical_target_digest=row["canonical_target_digest"],
            warning_code=row["warning_code"],
            warning_message=row["warning_message"],
            redirect_mode=row["redirect_mode"],
        )
