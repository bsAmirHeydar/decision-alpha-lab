"""Bounded caches for online context assembly.

The cache is intentionally small and deterministic. It does not perform I/O,
serialization, or background refresh in the decision thread.
"""
from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from threading import RLock
from time import monotonic_ns
from typing import Any, Hashable


@dataclass(frozen=True, slots=True)
class CacheRecord:
    value: Any
    created_ns: int
    expires_ns: int | None
    version: str

    def expired(self, now_ns: int) -> bool:
        return self.expires_ns is not None and now_ns >= self.expires_ns


class BoundedTTLCache:
    __slots__ = ("_maxsize", "_data", "_lock")

    def __init__(self, maxsize: int = 4096) -> None:
        if maxsize <= 0:
            raise ValueError("maxsize must be positive")
        self._maxsize = maxsize
        self._data: OrderedDict[Hashable, CacheRecord] = OrderedDict()
        self._lock = RLock()

    def get(self, key: Hashable) -> CacheRecord | None:
        now = monotonic_ns()
        with self._lock:
            record = self._data.get(key)
            if record is None:
                return None
            if record.expired(now):
                self._data.pop(key, None)
                return None
            self._data.move_to_end(key)
            return record

    def put(self, key: Hashable, value: Any, *, ttl_seconds: float | None, version: str) -> None:
        now = monotonic_ns()
        expires = None if ttl_seconds is None else now + int(ttl_seconds * 1_000_000_000)
        with self._lock:
            self._data[key] = CacheRecord(value, now, expires, version)
            self._data.move_to_end(key)
            while len(self._data) > self._maxsize:
                self._data.popitem(last=False)

    def invalidate(self, key: Hashable) -> None:
        with self._lock:
            self._data.pop(key, None)

    def invalidate_prefix(self, prefix: tuple[Any, ...]) -> int:
        with self._lock:
            keys = [key for key in self._data if isinstance(key, tuple) and key[: len(prefix)] == prefix]
            for key in keys:
                self._data.pop(key, None)
            return len(keys)

    def clear(self) -> None:
        with self._lock:
            self._data.clear()

    def __len__(self) -> int:
        return len(self._data)
