"""Atomic generation swapping for compiled plans and models."""
from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Generation(Generic[T]):
    generation_id: int
    artifact: T
    artifact_hash: str


class AtomicGeneration(Generic[T]):
    __slots__ = ("_current", "_lock")

    def __init__(self, initial: Generation[T]) -> None:
        self._current = initial
        self._lock = RLock()

    def get(self) -> Generation[T]:
        with self._lock:
            return self._current

    def swap(self, artifact: T, artifact_hash: str) -> Generation[T]:
        with self._lock:
            next_generation = Generation(self._current.generation_id + 1, artifact, artifact_hash)
            self._current = next_generation
            return next_generation
