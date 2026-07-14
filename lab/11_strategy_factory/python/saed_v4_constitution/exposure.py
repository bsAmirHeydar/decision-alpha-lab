"""Complete search, query, narrative, and agent exposure accounting."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .canonical import content_hash
from .enums import DecisionStatus, ReasonCode
from .models import ExposureEvent


@dataclass(frozen=True)
class ExposureBudget:
    family_id: str
    maximum_total: int
    maximum_hidden_submissions: int


@dataclass(frozen=True)
class ExposureEvaluation:
    status: DecisionStatus
    reasons: tuple[ReasonCode, ...]
    details: tuple[str, ...]
    total_exposures: int
    hidden_submissions: int


class ExposureLedger:
    def __init__(self, events: Iterable[ExposureEvent] = ()) -> None:
        self._events: list[ExposureEvent] = []
        self._ids: set[str] = set()
        for event in events:
            self.append(event)

    def append(self, event: ExposureEvent) -> str:
        eid = event.exposure_id
        if eid in self._ids:
            return eid
        self._events.append(event)
        self._ids.add(eid)
        return eid

    def events(self, family_id: str | None = None) -> tuple[ExposureEvent, ...]:
        items = self._events if family_id is None else [e for e in self._events if e.family_id == family_id]
        return tuple(sorted(items, key=lambda e: (e.known_time, e.exposure_id)))

    def evaluate(self, budget: ExposureBudget) -> ExposureEvaluation:
        events = self.events(budget.family_id)
        hidden = sum(1 for e in events if e.exposure_kind == "hidden_evaluation_submission")
        if len(events) > budget.maximum_total or hidden > budget.maximum_hidden_submissions:
            return ExposureEvaluation(
                DecisionStatus.REJECT,
                (ReasonCode.EXPOSURE_BUDGET_EXHAUSTED,),
                ("research family exposure budget is exhausted",),
                len(events),
                hidden,
            )
        return ExposureEvaluation(DecisionStatus.ALLOW, (ReasonCode.OK,), (), len(events), hidden)

    def digest(self) -> str:
        return content_hash([{"exposure_id": e.exposure_id, **e.__dict__} for e in self.events()])
