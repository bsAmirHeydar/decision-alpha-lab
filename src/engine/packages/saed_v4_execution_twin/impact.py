from __future__ import annotations
import math
from .models import ExecutionTwinProfile, Scenario


def market_impact_points(fill_fraction: float, scenario: Scenario, profile: ExecutionTwinProfile) -> float:
    units = profile.notional_units * fill_fraction
    permanent = profile.impact.linear_points_per_unit * units
    temporary = profile.impact.square_root_points_per_sqrt_unit * math.sqrt(max(0.0, units))
    retained = temporary * (1.0 - profile.impact.temporary_decay_fraction)
    return round((permanent + retained) * scenario.impact_multiplier, 12)
