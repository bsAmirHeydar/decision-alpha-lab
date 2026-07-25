from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum

class RuntimeState(IntEnum):
    CREATED = 0
    INITIALIZING = 1
    READY = 2
    RUNNING = 3
    DEGRADED = 4
    STOPPING = 5
    STOPPED = 6
    FAILED = 7

_ALLOWED = {
    RuntimeState.CREATED: {RuntimeState.INITIALIZING},
    RuntimeState.INITIALIZING: {RuntimeState.READY, RuntimeState.FAILED},
    RuntimeState.READY: {RuntimeState.RUNNING, RuntimeState.STOPPING, RuntimeState.FAILED},
    RuntimeState.RUNNING: {RuntimeState.DEGRADED, RuntimeState.STOPPING, RuntimeState.FAILED},
    RuntimeState.DEGRADED: {RuntimeState.RUNNING, RuntimeState.STOPPING, RuntimeState.FAILED},
    RuntimeState.STOPPING: {RuntimeState.STOPPED, RuntimeState.FAILED},
    RuntimeState.STOPPED: {RuntimeState.INITIALIZING},
    RuntimeState.FAILED: set(),
}

@dataclass(slots=True)
class RuntimeStateMachine:
    state: RuntimeState = RuntimeState.CREATED
    previous: RuntimeState = RuntimeState.CREATED
    last_transition_utc_msc: int = 0
    reason: str = "created"

    def transition(self, next_state: RuntimeState, now_utc_msc: int, reason: str) -> None:
        if next_state not in _ALLOWED[self.state]:
            raise ValueError(f"illegal transition: {self.state.name} -> {next_state.name}")
        self.previous = self.state
        self.state = next_state
        self.last_transition_utc_msc = now_utc_msc
        self.reason = reason
