"""Execution-cost models shared by historical simulation, paper, and live audit."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class CostModel:
    model_id: str
    spread_price: float = 0.0
    slippage_price: float = 0.0
    commission_per_unit: float = 0.0
    minimum_commission: float = 0.0
    multiplier: float = 1.0

    def total_price_cost(self, volume: float = 1.0) -> float:
        commission = max(self.minimum_commission, self.commission_per_unit * volume)
        return self.multiplier * (self.spread_price + self.slippage_price + commission)

    def cost_in_r(self, risk_distance: float, volume: float = 1.0) -> float:
        if risk_distance <= 0:
            raise ValueError("risk_distance must be positive")
        return self.total_price_cost(volume=volume) / risk_distance

    @classmethod
    def from_mapping(cls, model_id: str, payload: Mapping[str, float]) -> "CostModel":
        return cls(
            model_id=model_id,
            spread_price=float(payload.get("spread_price", 0.0)),
            slippage_price=float(payload.get("slippage_price", 0.0)),
            commission_per_unit=float(payload.get("commission_per_unit", 0.0)),
            minimum_commission=float(payload.get("minimum_commission", 0.0)),
            multiplier=float(payload.get("multiplier", 1.0)),
        )
