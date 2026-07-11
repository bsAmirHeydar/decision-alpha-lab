from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
import re

_SAFE = re.compile(r"^[A-Za-z0-9_.:/-]{1,128}$")

class RunMode(IntEnum):
    VISUAL_ANATOMY = 0
    ANATOMY_AUDIT = 1
    OUTCOME_STUDY = 2
    CANDIDATE_MATRIX = 3
    TESTER_EXECUTION = 4
    PAPER = 5
    LIVE_DISABLED = 6
    EXPORT_TRAINING_DATA = 7
    ONNX_INFERENCE = 8

class BusOverflowPolicy(IntEnum):
    REJECT_NEW = 0
    DROP_OLDEST = 1

@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    strategy_id: str
    strategy_version: str
    run_id: str
    generation_id: int = 1
    run_mode: RunMode = RunMode.ANATOMY_AUDIT
    strict_fail_closed: bool = True
    enable_audit_bus: bool = True
    timer_period_ms: int = 250
    max_events_per_cycle: int = 32
    audit_bus_capacity: int = 512
    audit_overflow_policy: BusOverflowPolicy = BusOverflowPolicy.REJECT_NEW

    def validate(self) -> None:
        for name, value in (("strategy_id", self.strategy_id),
                            ("strategy_version", self.strategy_version),
                            ("run_id", self.run_id)):
            if not _SAFE.fullmatch(value):
                raise ValueError(f"invalid {name}")
        if self.generation_id <= 0:
            raise ValueError("generation_id must be positive")
        if not 10 <= self.timer_period_ms <= 60_000:
            raise ValueError("timer_period_ms out of range")
        if not 1 <= self.max_events_per_cycle <= 10_000:
            raise ValueError("max_events_per_cycle out of range")
        if not 8 <= self.audit_bus_capacity <= 1_000_000:
            raise ValueError("audit_bus_capacity out of range")
