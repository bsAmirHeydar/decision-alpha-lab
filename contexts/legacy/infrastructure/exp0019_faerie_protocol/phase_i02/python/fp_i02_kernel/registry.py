"""Frozen public contract registry for FP-I02."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .canonical import canonical_sha256
from .errors import FPI02Error
from .reason_codes import DEFAULT_REASON_REGISTRY
from .relations import DEFAULT_RELATION_REGISTRY


@dataclass(frozen=True, slots=True)
class ContractDescriptor:
    contract_id: str
    version: str
    identity_domain: str
    persistence: str
    phase_owner: str
    authority: str


_DEFAULT = (
    ContractDescriptor("FP.SymbolPair", "1.0.0", "SEMANTIC", "MANIFEST", "FP-I02", "NONE"),
    ContractDescriptor("FP.WindowKey", "1.0.0", "SEMANTIC", "EVENT_STORE", "FP-I02", "NONE"),
    ContractDescriptor("FP.WindowRecord", "1.0.0", "SEMANTIC", "EVENT_STORE", "FP-I05", "NONE"),
    ContractDescriptor("FP.ReferenceSideKey", "1.0.0", "SEMANTIC", "EVENT_STORE", "FP-I02", "NONE"),
    ContractDescriptor("FP.ReferenceSideRecord", "1.0.0", "SEMANTIC", "CHECKPOINT", "FP-I05", "NONE"),
    ContractDescriptor("FP.HuntFact", "1.0.0", "SEMANTIC", "LEDGER", "FP-I06", "NONE"),
    ContractDescriptor("FP.DivergenceCandidate", "1.0.0", "SEMANTIC", "LEDGER", "FP-I06", "NONE"),
    ContractDescriptor("FP.ConfirmationEvent", "1.0.0", "SEMANTIC", "LEDGER", "FP-I07", "NONE"),
    ContractDescriptor("FP.ConfirmedSignal", "1.0.0", "SEMANTIC", "LEDGER", "FP-I07", "NONE"),
    ContractDescriptor("FP.WWContextRecord", "1.0.0", "SEMANTIC", "CHECKPOINT", "FP-I08", "NONE"),
    ContractDescriptor("FP.QuotaKey", "1.0.0", "SEMANTIC", "LEDGER", "FP-I09", "NONE"),
    ContractDescriptor("FP.QuotaRecord", "1.0.0", "SEMANTIC", "CHECKPOINT", "FP-I09", "NONE"),
    ContractDescriptor("FP.ReasonEvidence", "1.0.0", "SEMANTIC", "LEDGER", "FP-I02", "NONE"),
    ContractDescriptor("FP.HealthStatus", "1.0.0", "SEMANTIC", "DIAGNOSTIC", "FP-I02", "NONE"),
    ContractDescriptor("FP.ContextManifestRecord", "1.0.0", "SEMANTIC", "MANIFEST", "FP-I02", "NONE"),
    ContractDescriptor("FP.ProjectionIdentity", "1.0.0", "PROJECTION", "CHART_OBJECT", "FP-I10", "NONE"),
)


class ContractRegistry:
    def __init__(self, descriptors: Iterable[ContractDescriptor] = _DEFAULT) -> None:
        items = tuple(descriptors)
        keys = [f"{item.contract_id}@{item.version}" for item in items]
        if len(keys) != len(set(keys)):
            raise FPI02Error("FP_RC_INVALID_CONFIG", "duplicate contract descriptor")
        if any(item.authority != "NONE" for item in items):
            raise FPI02Error("FP_RC_LIVE_AUTHORITY_FORBIDDEN", "FP-I02 contracts cannot grant runtime authority")
        self._items = {key: item for key, item in zip(keys, items)}
        self.registry_hash = canonical_sha256({
            "contracts": items,
            "relation_registry_hash": DEFAULT_RELATION_REGISTRY.registry_hash,
            "reason_registry_hash": DEFAULT_REASON_REGISTRY.registry_hash,
        })
        self._frozen = True

    def resolve(self, exact_key: str) -> ContractDescriptor:
        try:
            return self._items[exact_key]
        except KeyError as exc:
            raise FPI02Error("FP_RC_CHECKPOINT_VERSION_MISMATCH", f"unknown contract key: {exact_key}") from exc

    def all(self) -> tuple[ContractDescriptor, ...]:
        return tuple(self._items[key] for key in sorted(self._items))

    def register(self, descriptor: ContractDescriptor) -> None:
        raise FPI02Error("FP_RC_INVALID_CONFIG", "contract registry is frozen")


DEFAULT_CONTRACT_REGISTRY = ContractRegistry()
