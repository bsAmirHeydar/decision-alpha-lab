"""Deterministic paper broker used before any live adapter is authorized."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Mapping, Optional
import hashlib

from ..contracts import ExecutionIntent, ExecutionTrace
from .broker import BrokerAdapter


class PaperBroker(BrokerAdapter):
    adapter_id = "paper_broker_v1"

    def __init__(self) -> None:
        self._state: Dict[str, ExecutionTrace] = {}

    def validate_intent(self, intent: ExecutionIntent) -> Mapping[str, object]:
        try:
            intent.validate()
        except Exception as exc:
            return {"valid": False, "reason": str(exc)}
        if intent.intent_id in self._state:
            return {"valid": False, "reason": "duplicate_intent"}
        return {"valid": True, "reason": "ok"}

    def submit(self, intent: ExecutionIntent) -> ExecutionTrace:
        validation = self.validate_intent(intent)
        now = datetime.now(timezone.utc)
        if not validation["valid"]:
            return ExecutionTrace(
                intent_id=intent.intent_id,
                broker_adapter_id=self.adapter_id,
                request_time_utc=now,
                response_time_utc=now,
                order_id=None,
                position_id=None,
                state="rejected",
                reject_reason=str(validation["reason"]),
            )
        order_id = "paper_ord_" + hashlib.sha256(intent.intent_id.encode()).hexdigest()[:16]
        trace = ExecutionTrace(
            intent_id=intent.intent_id,
            broker_adapter_id=self.adapter_id,
            request_time_utc=now,
            response_time_utc=now,
            order_id=order_id,
            position_id=None,
            state="accepted",
            metadata={"entry_type": intent.entry_type, "entry_price": intent.entry_price},
        )
        self._state[intent.intent_id] = trace
        return trace

    def cancel(self, intent_id: str) -> ExecutionTrace:
        now = datetime.now(timezone.utc)
        existing = self._state.get(intent_id)
        trace = ExecutionTrace(
            intent_id=intent_id,
            broker_adapter_id=self.adapter_id,
            request_time_utc=now,
            response_time_utc=now,
            order_id=existing.order_id if existing else None,
            position_id=existing.position_id if existing else None,
            state="cancelled" if existing else "not_found",
            reject_reason=None if existing else "unknown_intent",
        )
        self._state[intent_id] = trace
        return trace

    def reconcile(self) -> list[ExecutionTrace]:
        return list(self._state.values())
