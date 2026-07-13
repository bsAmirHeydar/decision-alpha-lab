"""Closed Faerie Protocol relation registry."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .canonical import canonical_sha256, require_semver
from .enums import RelationCode, WindowKind, WindowScope
from .errors import FPI02Error


@dataclass(frozen=True, slots=True)
class RelationDescriptor:
    code: RelationCode
    reference_kind: WindowKind
    reference_scope: WindowScope
    check_kind: WindowKind
    check_scope: WindowScope
    quota_session: str
    ww_gated: bool
    tradeable: bool
    directional_gate: bool = False

    def __post_init__(self) -> None:
        if self.code.value[0] != self.reference_kind.value or self.code.value[1] != self.check_kind.value:
            raise FPI02Error("FP_RC_RELATION_DESCRIPTOR_INVALID", "relation code must be reference-then-check")
        if self.code is RelationCode.WW:
            if not self.directional_gate or self.ww_gated or self.quota_session != "SESSION_AT_ENTRY_ELIGIBILITY":
                raise FPI02Error("FP_RC_RELATION_DESCRIPTOR_INVALID", "WW descriptor policy mismatch")
        elif self.directional_gate or self.quota_session not in {"A", "L", "N"}:
            raise FPI02Error("FP_RC_RELATION_DESCRIPTOR_INVALID", "intraday relation descriptor mismatch")


_DEFAULT = (
    RelationDescriptor(RelationCode.AL, WindowKind.A, WindowScope.SAME_TRADING_DAY, WindowKind.L, WindowScope.SAME_TRADING_DAY, "L", True, True),
    RelationDescriptor(RelationCode.AN, WindowKind.A, WindowScope.SAME_TRADING_DAY, WindowKind.N, WindowScope.SAME_TRADING_DAY, "N", True, True),
    RelationDescriptor(RelationCode.LN, WindowKind.L, WindowScope.SAME_TRADING_DAY, WindowKind.N, WindowScope.SAME_TRADING_DAY, "N", True, True),
    RelationDescriptor(RelationCode.NA, WindowKind.N, WindowScope.EXACT_PRIOR_CALENDAR_OFFSET, WindowKind.A, WindowScope.CURRENT_TRADING_DAY, "A", True, True),
    RelationDescriptor(RelationCode.NL, WindowKind.N, WindowScope.EXACT_PRIOR_CALENDAR_OFFSET, WindowKind.L, WindowScope.CURRENT_TRADING_DAY, "L", True, True),
    RelationDescriptor(RelationCode.NN, WindowKind.N, WindowScope.EXACT_PRIOR_CALENDAR_OFFSET, WindowKind.N, WindowScope.CURRENT_TRADING_DAY, "N", True, True),
    RelationDescriptor(RelationCode.WW, WindowKind.W, WindowScope.PREVIOUS_COMPLETED_NY_WEEK, WindowKind.W, WindowScope.CURRENT_NY_WEEK, "SESSION_AT_ENTRY_ELIGIBILITY", False, True, True),
)


class RelationRegistry:
    def __init__(self, version: str = "2.0.0", descriptors: Iterable[RelationDescriptor] = _DEFAULT) -> None:
        self.version = require_semver(version, "relation_registry_version")
        material = tuple(descriptors)
        keys = [item.code for item in material]
        if len(keys) != 7 or set(keys) != set(RelationCode):
            raise FPI02Error("FP_RC_RELATION_DESCRIPTOR_INVALID", "registry must contain exactly AL/AN/LN/NA/NL/NN/WW")
        self._items = {item.code: item for item in material}
        self.registry_hash = canonical_sha256({"version": self.version, "descriptors": material})

    def resolve(self, code: RelationCode | str) -> RelationDescriptor:
        try:
            key = code if isinstance(code, RelationCode) else RelationCode(code)
        except ValueError as exc:
            raise FPI02Error("FP_RC_UNKNOWN_ENUM", f"unknown relation code: {code}") from exc
        return self._items[key]

    def all(self) -> tuple[RelationDescriptor, ...]:
        return tuple(self._items[code] for code in RelationCode)


DEFAULT_RELATION_REGISTRY = RelationRegistry()
