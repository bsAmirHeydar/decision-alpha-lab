from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json
import threading

from .canonical import digest_object
from .errors import IntegrityError
from .types import fmt_time, parse_time

GENESIS = "sha256:" + "0" * 64


@dataclass(frozen=True, slots=True)
class AuditEvent:
    sequence: int
    event_id: str
    event_type: str
    tenant_id: str
    subject_id: str
    actor_id: str
    occurred_at: datetime
    payload_digest: str
    previous_hash: str
    event_hash: str
    metadata: dict[str, Any]

    def unsigned(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "event_id": self.event_id,
            "event_type": self.event_type,
            "tenant_id": self.tenant_id,
            "subject_id": self.subject_id,
            "actor_id": self.actor_id,
            "occurred_at": fmt_time(self.occurred_at),
            "payload_digest": self.payload_digest,
            "previous_hash": self.previous_hash,
            "metadata": self.metadata,
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self.unsigned(), "event_hash": self.event_hash}

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> "AuditEvent":
        return cls(
            int(obj["sequence"]),
            str(obj["event_id"]),
            str(obj["event_type"]),
            str(obj["tenant_id"]),
            str(obj["subject_id"]),
            str(obj["actor_id"]),
            parse_time(obj["occurred_at"]),
            str(obj["payload_digest"]),
            str(obj["previous_hash"]),
            str(obj["event_hash"]),
            dict(obj.get("metadata", {})),
        )


class AuditLedger:
    def __init__(self, path: Path | None = None):
        self.path = path
        self._events: list[AuditEvent] = []
        self._lock = threading.RLock()
        self._load()

    def _load(self) -> None:
        if self.path and self.path.exists():
            self._events = [
                AuditEvent.from_dict(json.loads(line))
                for line in self.path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.verify()

    def append(
        self,
        event_type: str,
        tenant_id: str,
        subject_id: str,
        actor_id: str,
        payload: Any,
        occurred_at: datetime | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AuditEvent:
        with self._lock:
            sequence = len(self._events) + 1
            previous_hash = self._events[-1].event_hash if self._events else GENESIS
            unsigned = {
                "sequence": sequence,
                "event_id": f"AUD_{sequence:012d}",
                "event_type": event_type,
                "tenant_id": tenant_id,
                "subject_id": subject_id,
                "actor_id": actor_id,
                "occurred_at": fmt_time(occurred_at or datetime.now(timezone.utc)),
                "payload_digest": digest_object(payload),
                "previous_hash": previous_hash,
                "metadata": metadata or {},
            }
            event = AuditEvent(
                sequence=sequence,
                event_id=unsigned["event_id"],
                event_type=event_type,
                tenant_id=tenant_id,
                subject_id=subject_id,
                actor_id=actor_id,
                occurred_at=parse_time(unsigned["occurred_at"]),
                payload_digest=unsigned["payload_digest"],
                previous_hash=previous_hash,
                event_hash=digest_object(unsigned),
                metadata=unsigned["metadata"],
            )
            self._events.append(event)
            if self.path:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                with self.path.open("a", encoding="utf-8", newline="\n") as handle:
                    handle.write(
                        json.dumps(event.to_dict(), sort_keys=True, separators=(",", ":"))
                        + "\n"
                    )
            return event

    def verify(self) -> bool:
        previous_hash = GENESIS
        for index, event in enumerate(self._events, 1):
            if event.sequence != index:
                raise IntegrityError(f"audit sequence mismatch at {index}")
            if event.previous_hash != previous_hash:
                raise IntegrityError(f"audit previous hash mismatch at {index}")
            if digest_object(event.unsigned()) != event.event_hash:
                raise IntegrityError(f"audit event hash mismatch at {index}")
            previous_hash = event.event_hash
        return True

    @property
    def events(self) -> tuple[AuditEvent, ...]:
        return tuple(self._events)

    @property
    def head(self) -> str:
        return self._events[-1].event_hash if self._events else GENESIS
