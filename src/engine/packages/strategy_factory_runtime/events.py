from __future__ import annotations
from dataclasses import dataclass, replace
from enum import IntEnum
from collections import deque
from .config import BusOverflowPolicy

class EventType(IntEnum):
    NONE = 0
    RUNTIME_INITIALIZED = 1
    RUNTIME_STARTED = 2
    RUNTIME_STOPPED = 3
    RUNTIME_FAILED = 4
    HEARTBEAT = 5
    ANATOMY_DETECTED = 10
    ANATOMY_REJECTED = 11
    SNAPSHOT_CREATED = 20
    SNAPSHOT_REJECTED = 21
    AUDIT_DROPPED = 90

@dataclass(frozen=True, slots=True)
class EventEnvelope:
    sequence: int
    event_type: EventType
    aggregate_id: str
    source_id: str
    occurred_at_utc_msc: int
    known_at_utc_msc: int
    payload_hash: str
    priority: int = 50

    def validate(self) -> None:
        if self.event_type == EventType.NONE:
            raise ValueError("event_type cannot be NONE")
        if not self.aggregate_id or not self.source_id or not self.payload_hash:
            raise ValueError("event identity fields are required")
        if self.occurred_at_utc_msc > self.known_at_utc_msc:
            raise ValueError("occurred_at after known_at")
        if not 0 <= self.priority <= 100:
            raise ValueError("priority out of range")

class BoundedEventBus:
    def __init__(self, capacity: int, policy: BusOverflowPolicy):
        if capacity < 8:
            raise ValueError("capacity below minimum")
        self.capacity = capacity
        self.policy = policy
        self._queue: deque[EventEnvelope] = deque()
        self._next_sequence = 1
        self.dropped = 0

    def publish(self, event: EventEnvelope) -> bool:
        event.validate()
        if len(self._queue) >= self.capacity:
            if self.policy == BusOverflowPolicy.REJECT_NEW:
                self.dropped += 1
                return False
            self._queue.popleft()
            self.dropped += 1
        self._queue.append(replace(event, sequence=self._next_sequence))
        self._next_sequence += 1
        return True

    def poll(self) -> EventEnvelope | None:
        return self._queue.popleft() if self._queue else None

    def __len__(self) -> int:
        return len(self._queue)
