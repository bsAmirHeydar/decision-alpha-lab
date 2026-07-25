"""Tamper-evident append-only constitutional decision ledger."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Iterable

from .canonical import content_hash
from .errors import IntegrityViolation


GENESIS_HASH = "0" * 64


@dataclass(frozen=True)
class LedgerEntry:
    sequence: int
    known_time: str
    event_type: str
    payload_hash: str
    previous_hash: str
    entry_hash: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class HashChainLedger:
    def __init__(self, entries: Iterable[LedgerEntry] = ()) -> None:
        self._entries: list[LedgerEntry] = []
        for entry in entries:
            self._entries.append(entry)
        if self._entries:
            self.verify()

    @staticmethod
    def calculate_hash(sequence: int, known_time: str, event_type: str, payload_hash: str, previous_hash: str) -> str:
        return content_hash({
            "sequence": sequence,
            "known_time": known_time,
            "event_type": event_type,
            "payload_hash": payload_hash,
            "previous_hash": previous_hash,
        })

    def append(self, known_time: str, event_type: str, payload: Any) -> LedgerEntry:
        sequence = len(self._entries) + 1
        previous = self._entries[-1].entry_hash if self._entries else GENESIS_HASH
        payload_hash = content_hash(payload)
        entry_hash = self.calculate_hash(sequence, known_time, event_type, payload_hash, previous)
        entry = LedgerEntry(sequence, known_time, event_type, payload_hash, previous, entry_hash)
        self._entries.append(entry)
        return entry

    def verify(self) -> bool:
        previous = GENESIS_HASH
        for expected_sequence, entry in enumerate(self._entries, start=1):
            if entry.sequence != expected_sequence or entry.previous_hash != previous:
                raise IntegrityViolation("ledger sequence or previous hash mismatch")
            expected = self.calculate_hash(entry.sequence, entry.known_time, entry.event_type, entry.payload_hash, entry.previous_hash)
            if entry.entry_hash != expected:
                raise IntegrityViolation("ledger entry hash mismatch")
            previous = entry.entry_hash
        return True

    def entries(self) -> tuple[LedgerEntry, ...]:
        return tuple(self._entries)

    def head_hash(self) -> str:
        return self._entries[-1].entry_hash if self._entries else GENESIS_HASH
