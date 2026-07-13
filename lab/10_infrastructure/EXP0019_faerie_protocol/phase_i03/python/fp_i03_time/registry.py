"""Frozen registry for time/calendar public surfaces."""
from __future__ import annotations
from dataclasses import dataclass
from fp_i02_kernel.canonical import canonical_sha256
from .contracts import canonical_registry_snapshot
from .errors import FPI03Error


@dataclass(frozen=True, slots=True)
class TimeContractDescriptor:
    contract_id: str
    version: str
    identity_domain: str
    producer: str
    persistence: str
    authority: str = "NONE"


_DESCRIPTORS = (
    TimeContractDescriptor("FP.TimeKernelConfig", "1.0.0", "SEMANTIC", "FP-I03", "MANIFEST"),
    TimeContractDescriptor("FP.BrokerTimestamp", "1.0.0", "OPERATIONAL", "FP-I03", "TRANSIENT"),
    TimeContractDescriptor("FP.NyTimestamp", "1.0.0", "SEMANTIC", "FP-I03", "EVENT_STORE"),
    TimeContractDescriptor("FP.LocalResolution", "1.0.0", "SEMANTIC", "FP-I03", "DIAGNOSTIC"),
    TimeContractDescriptor("FP.SessionDefinition", "1.0.0", "SEMANTIC", "FP-I03", "REGISTRY"),
    TimeContractDescriptor("FP.TradingDayWindow", "1.0.0", "SEMANTIC", "FP-I03", "EVENT_STORE"),
    TimeContractDescriptor("FP.SessionWindow", "1.0.0", "SEMANTIC", "FP-I03", "EVENT_STORE"),
    TimeContractDescriptor("FP.WeekWindow", "1.0.0", "SEMANTIC", "FP-I03", "EVENT_STORE"),
    TimeContractDescriptor("FP.BoundaryEvidence", "1.0.0", "SEMANTIC", "FP-I03", "LEDGER"),
    TimeContractDescriptor("FP.CalendarSnapshot", "1.0.0", "SEMANTIC", "FP-I03", "CHECKPOINT"),
    TimeContractDescriptor("FP.CalendarRegistrySnapshot", "1.0.0", "SEMANTIC", "FP-I03", "REGISTRY"),
)


class TimeContractRegistry:
    def __init__(self) -> None:
        keys = [f"{item.contract_id}@{item.version}" for item in _DESCRIPTORS]
        if len(keys) != len(set(keys)):
            raise FPI03Error("FP_TRC_REGISTRY_DUPLICATE", "duplicate time contract")
        if any(item.authority != "NONE" for item in _DESCRIPTORS):
            raise FPI03Error("FP_TRC_AUTHORITY_FORBIDDEN", "time contracts cannot grant runtime authority")
        self._items = dict(zip(keys, _DESCRIPTORS))
        self.registry_hash = canonical_sha256({
            "contracts": _DESCRIPTORS,
            "session_registry_hash": canonical_registry_snapshot().registry_hash,
        })

    def resolve(self, exact_key: str) -> TimeContractDescriptor:
        try:
            return self._items[exact_key]
        except KeyError as exc:
            raise FPI03Error("FP_TRC_CONTRACT_UNKNOWN", f"unknown time contract {exact_key}") from exc

    def all(self):
        return tuple(self._items[key] for key in sorted(self._items))

    def register(self, descriptor: TimeContractDescriptor) -> None:
        raise FPI03Error("FP_TRC_REGISTRY_FROZEN", "time contract registry is frozen")


DEFAULT_TIME_CONTRACT_REGISTRY = TimeContractRegistry()
