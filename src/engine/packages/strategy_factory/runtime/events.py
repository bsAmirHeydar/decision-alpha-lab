"""Deterministic synchronous event bus plus non-authoritative observers."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from threading import RLock
from typing import Any, Callable


EventHandler = Callable[[Any], None]


@dataclass(frozen=True, slots=True)
class Subscription:
    topic: str
    handler: EventHandler
    authoritative: bool = False


class EventBus:
    """Synchronous by design for deterministic replay.

    Authoritative handlers run first in registration order. Observer failures
    may be ignored by the caller; authoritative failures propagate.
    """

    def __init__(self) -> None:
        self._subscriptions: dict[str, list[Subscription]] = defaultdict(list)
        self._lock = RLock()

    def subscribe(self, topic: str, handler: EventHandler, *, authoritative: bool = False) -> None:
        with self._lock:
            self._subscriptions[topic].append(Subscription(topic, handler, authoritative))

    def publish(self, topic: str, payload: Any, *, ignore_observer_errors: bool = True) -> None:
        with self._lock:
            subscriptions = tuple(self._subscriptions.get(topic, ()))
        ordered = sorted(subscriptions, key=lambda s: not s.authoritative)
        for subscription in ordered:
            try:
                subscription.handler(payload)
            except Exception:
                if subscription.authoritative or not ignore_observer_errors:
                    raise
