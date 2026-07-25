from __future__ import annotations
from dataclasses import dataclass
from .enums import LabelKind, AmbiguousLabelPolicy
from .models import LabelContract

@dataclass(frozen=True, slots=True)
class DerivedLabel:
    value: float | None
    available: bool
    reason: str

def derive_label(net_r: float, ambiguous: bool, filled: bool, terminal: bool, contract: LabelContract) -> DerivedLabel:
    contract.validate()
    if contract.require_filled and not filled:
        return DerivedLabel(None, False, "not_filled")
    if contract.require_terminal and not terminal:
        return DerivedLabel(None, False, "non_terminal")
    if ambiguous:
        if contract.ambiguous_policy == AmbiguousLabelPolicy.EXCLUDE:
            return DerivedLabel(None, False, "ambiguous_excluded")
        if contract.ambiguous_policy == AmbiguousLabelPolicy.NEGATIVE:
            return DerivedLabel(0.0 if contract.kind == LabelKind.BINARY_NET_R else min(0.0, net_r), True, "ambiguous_negative")
        return DerivedLabel(0.0, True, "ambiguous_zero_utility")
    if contract.kind == LabelKind.BINARY_NET_R:
        return DerivedLabel(1.0 if net_r > contract.positive_threshold_r else 0.0, True, "binary_net_r")
    clipped = min(contract.regression_cap_r, max(contract.regression_floor_r, net_r))
    return DerivedLabel(clipped, True, "continuous_net_r")
