"""Bounded idempotency guard for event and decision processing."""
from __future__ import annotations

from collections import OrderedDict
from threading import RLock


class IdempotencyGuard:
    def __init__(self, maxsize: int = 100000) -> None:
        self._maxsize = maxsize
        self._seen: OrderedDict[str, None] = OrderedDict()
        self._lock = RLock()

    def claim(self, key: str) -> bool:
        with self._lock:
            if key in self._seen:
                self._seen.move_to_end(key)
                return False
            self._seen[key] = None
            while len(self._seen) > self._maxsize:
                self._seen.popitem(last=False)
            return True
