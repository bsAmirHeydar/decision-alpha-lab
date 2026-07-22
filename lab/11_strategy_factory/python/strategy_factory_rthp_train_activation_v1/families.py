from __future__ import annotations

from dataclasses import dataclass

from .cycles import CycleAggregate


@dataclass(frozen=True, slots=True)
class RelationCandidate:
    family: str
    active: CycleAggregate
    reference: CycleAggregate
    active_cycle_type: str
    reference_cycle_type: str
    required_reference_count: int
    available_reference_count: int
    reference_age_cycles: int
    reference_to_active_gap_cycles: int
    is_same_day_reference: bool
    sequentiality: str


def _before(cycles: tuple[CycleAggregate, ...], active: CycleAggregate, cycle_type: str, *, complete_only: bool = True, exclude_same_day: bool = False) -> list[CycleAggregate]:
    out = []
    for cycle in cycles:
        if cycle.key.cycle_type != cycle_type or cycle.key.end_ms > active.key.start_ms:
            continue
        if complete_only and cycle.key.completeness != "COMPLETE":
            continue
        if exclude_same_day and cycle.key.trading_day_ny == active.key.trading_day_ny:
            continue
        out.append(cycle)
    return sorted(out, key=lambda x: x.key.end_ms, reverse=True)


def build_relation_candidates(cycles: tuple[CycleAggregate, ...]) -> tuple[RelationCandidate, ...]:
    result: list[RelationCandidate] = []
    for active in cycles:
        t = active.key.cycle_type
        specs: list[tuple[str, list[CycleAggregate], str, str, int]] = []
        if t == "WEEKLY":
            specs.append(("WW", _before(cycles, active, "WEEKLY")[:1], "CURRENT_WEEK", "PREVIOUS_COMPLETED_WEEK", 1))
        if t == "DAILY":
            specs.append(("DD", _before(cycles, active, "DAILY")[:12], "CURRENT_DAILY", "PREVIOUS_DAILY", 12))
        if t == "N":
            specs.append(("NN", _before(cycles, active, "N")[:12], "CURRENT_N", "PREVIOUS_N", 12))
            same_l = [x for x in cycles if x.key.cycle_type == "L" and x.key.trading_day_ny == active.key.trading_day_ny and x.key.end_ms <= active.key.start_ms]
            prev_l = _before(cycles, active, "L", exclude_same_day=True)[:12]
            specs.append(("LN", same_l + prev_l, "CURRENT_N", "CURRENT_L_OR_PREVIOUS_L", 12))
            specs.append(("AN", _before(cycles, active, "A", exclude_same_day=True)[:12], "CURRENT_N", "PREVIOUS_A", 12))
            same_l_pmi = [x for x in same_l if x.key.completeness in ("COMPLETE", "PARTIAL")]
            specs.append(("PMI", same_l_pmi[:1], "CURRENT_N", "CURRENT_L", 0))
        if t == "L":
            specs.append(("NL", _before(cycles, active, "N")[:12], "CURRENT_L", "PREVIOUS_N", 12))
        if t == "A":
            specs.append(("NA", _before(cycles, active, "N", exclude_same_day=True)[:12], "CURRENT_A", "PREVIOUS_N", 12))
        if t == "FCR_2":
            refs = [x for x in cycles if x.key.cycle_type == "FCR_1" and x.key.trading_day_ny == active.key.trading_day_ny]
            specs.append(("FCR", refs[:1], "FCR_2", "FCR_1", 0))
        if t == "PP_2":
            refs = [x for x in cycles if x.key.cycle_type == "PP_1" and x.key.trading_day_ny == active.key.trading_day_ny]
            specs.append(("PP", refs[:1], "PP_2", "PP_1", 0))
        if t == "M15":
            refs = [x for x in cycles if x.key.cycle_type == "M15" and x.key.trading_day_ny == active.key.trading_day_ny and x.key.end_ms <= active.key.start_ms]
            refs = sorted(refs, key=lambda x: x.key.start_ms, reverse=True)
            specs.append(("M15_CYCLE_GROUP", refs, "CURRENT_M15_IN_N", "PRIOR_M15_IN_SAME_N", 0))
        for family, refs, active_type, reference_type, required in specs:
            available = len(refs)
            for index, reference in enumerate(refs):
                same_day = reference.key.trading_day_ny == active.key.trading_day_ny
                age = 0 if same_day and reference.key.end_ms == active.key.start_ms else index + 1
                ref_type = reference_type
                if family == "LN":
                    ref_type = "CURRENT_L" if same_day else "PREVIOUS_L"
                sequentiality = "NOT_APPLICABLE"
                if family == "M15_CYCLE_GROUP":
                    sequentiality = "SEQUENTIAL" if reference.key.end_ms == active.key.start_ms else "NON_SEQUENTIAL"
                result.append(RelationCandidate(
                    family,
                    active,
                    reference,
                    active_type,
                    ref_type,
                    required,
                    available,
                    age,
                    age,
                    same_day,
                    sequentiality,
                ))
    return tuple(sorted(result, key=lambda x: (x.active.key.start_ms, x.family, x.reference.key.end_ms, x.reference.key.cycle_instance_id)))
