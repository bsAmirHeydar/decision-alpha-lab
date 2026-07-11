"""Broker adapter boundary."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Mapping

from ..contracts import ExecutionIntent, ExecutionTrace


class BrokerAdapter(ABC):
    adapter_id: str

    @abstractmethod
    def validate_intent(self, intent: ExecutionIntent) -> Mapping[str, object]:
        raise NotImplementedError

    @abstractmethod
    def submit(self, intent: ExecutionIntent) -> ExecutionTrace:
        raise NotImplementedError

    @abstractmethod
    def cancel(self, intent_id: str) -> ExecutionTrace:
        raise NotImplementedError

    @abstractmethod
    def reconcile(self) -> list[ExecutionTrace]:
        raise NotImplementedError
