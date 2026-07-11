from __future__ import annotations

from dataclasses import dataclass, replace
from strategy_factory_contracts.validation import validate_terminal_symbol
from .enums import DataQuality

@dataclass(frozen=True, slots=True)
class SymbolSpecSnapshot:
    symbol: str
    digits: int
    point: float
    tick_size: float
    tick_value: float
    contract_size: float
    volume_min: float
    volume_max: float
    volume_step: float
    stops_level_points: int
    freeze_level_points: int
    filling_mode: int
    order_mode: int
    trade_mode: int
    specification_generation: int
    observed_at_utc_milliseconds: int
    quality: DataQuality = DataQuality.VALID

    def __post_init__(self) -> None:
        validate_terminal_symbol(self.symbol, "symbol")
        if self.digits < 0:
            raise ValueError("negative digits")
        if self.point <= 0 or self.tick_size <= 0 or self.volume_step <= 0:
            raise ValueError("invalid symbol specification")
        if self.volume_min < 0 or self.volume_max < self.volume_min:
            raise ValueError("invalid volume range")
        if self.specification_generation < 0:
            raise ValueError("negative specification generation")

    def material_key(self) -> tuple[object, ...]:
        return (
            self.digits, self.point, self.tick_size, self.tick_value,
            self.contract_size, self.volume_min, self.volume_max,
            self.volume_step, self.stops_level_points, self.freeze_level_points,
            self.filling_mode, self.order_mode, self.trade_mode,
        )

class SymbolSpecCache:
    def __init__(self) -> None:
        self._items: dict[str, SymbolSpecSnapshot] = {}

    def put(self, snapshot: SymbolSpecSnapshot) -> SymbolSpecSnapshot:
        previous = self._items.get(snapshot.symbol)
        generation = 1 if previous is None else previous.specification_generation
        if previous is not None and previous.material_key() != snapshot.material_key():
            generation += 1
        updated = replace(snapshot, specification_generation=generation)
        self._items[snapshot.symbol] = updated
        return updated

    def get(self, symbol: str) -> SymbolSpecSnapshot:
        try:
            return self._items[symbol]
        except KeyError as exc:
            raise KeyError("symbol specification not cached") from exc
