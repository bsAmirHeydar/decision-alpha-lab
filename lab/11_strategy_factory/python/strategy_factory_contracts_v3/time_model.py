"""UTC-only known-time chain and causal ordering validation."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Mapping
from .errors import KnownTimeError
from .validation import require_safe_identifier

MAX_EPOCH_MS=253402300799999

@dataclass(frozen=True, slots=True, order=True)
class UtcInstant:
    epoch_ms: int
    clock_id: str="utc"

    def __post_init__(self) -> None:
        if not isinstance(self.epoch_ms, int) or isinstance(self.epoch_ms, bool) or self.epoch_ms < 0 or self.epoch_ms > MAX_EPOCH_MS:
            raise KnownTimeError("invalid_epoch_ms", "epoch_ms is outside the supported UTC range", {"epoch_ms": self.epoch_ms})
        require_safe_identifier(self.clock_id, "clock_id", max_length=96)

    @classmethod
    def from_datetime(cls, value: datetime, clock_id: str="utc") -> "UtcInstant":
        if value.tzinfo is None or value.utcoffset() is None:
            raise KnownTimeError("naive_datetime", "datetime must carry explicit timezone information")
        utc=value.astimezone(timezone.utc)
        return cls(int(utc.timestamp()*1000), clock_id)

    def material(self) -> dict[str, object]:
        return {"clock_id":self.clock_id,"epoch_ms":self.epoch_ms,"timezone":"UTC"}

@dataclass(frozen=True, slots=True)
class KnownTimeChain:
    event_time: UtcInstant
    known_time: UtcInstant
    confirmation_time: UtcInstant
    observation_cut: UtcInstant
    decision_time: UtcInstant
    action_time: UtcInstant | None=None
    fill_time: UtcInstant | None=None
    label_maturity_time: UtcInstant | None=None

    def __post_init__(self) -> None:
        ordered=[("event_time",self.event_time), ("known_time",self.known_time), ("confirmation_time",self.confirmation_time), ("observation_cut",self.observation_cut), ("decision_time",self.decision_time)]
        previous_name, previous=ordered[0]
        for name,current in ordered[1:]:
            if current.epoch_ms < previous.epoch_ms:
                raise KnownTimeError("causal_time_reversal", f"{name} precedes {previous_name}", {previous_name: previous.epoch_ms, name: current.epoch_ms})
            previous_name,previous=name,current
        cursor=self.decision_time
        for name,current in (("action_time",self.action_time),("fill_time",self.fill_time),("label_maturity_time",self.label_maturity_time)):
            if current is None: continue
            if current.epoch_ms < cursor.epoch_ms:
                raise KnownTimeError("causal_time_reversal", f"{name} precedes the previous present stage", {"previous": cursor.epoch_ms, name: current.epoch_ms})
            cursor=current
        if self.fill_time is not None and self.action_time is None:
            raise KnownTimeError("fill_without_action", "fill_time requires action_time")

    def material(self) -> Mapping[str, object]:
        def value(item: UtcInstant | None) -> object:
            return None if item is None else item.material()
        return {name:value(getattr(self,name)) for name in (
            "event_time","known_time","confirmation_time","observation_cut","decision_time","action_time","fill_time","label_maturity_time")}

    def assert_feature_known(self, feature_known_time: UtcInstant) -> None:
        if feature_known_time.epoch_ms > self.observation_cut.epoch_ms:
            raise KnownTimeError("future_feature", "feature became known after observation_cut", {"feature_known_time":feature_known_time.epoch_ms,"observation_cut":self.observation_cut.epoch_ms})

    def assert_label_mature(self, evaluation_time: UtcInstant) -> None:
        if self.label_maturity_time is None:
            raise KnownTimeError("missing_label_maturity", "label maturity is not present")
        if evaluation_time.epoch_ms < self.label_maturity_time.epoch_ms:
            raise KnownTimeError("immature_label", "label was consumed before maturity")
