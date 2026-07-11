"""Canonical event, feature, candidate, and outcome dataset assembly."""
from __future__ import annotations

from dataclasses import asdict
from typing import Iterable, Mapping, Sequence

import pandas as pd

from .contracts import AnatomyEvent, FeatureSnapshot, OutcomeRecord, TradeCandidate


def events_to_frame(events: Iterable[AnatomyEvent]) -> pd.DataFrame:
    rows = []
    for event in events:
        payload = event.canonical_payload()
        metadata = payload.pop("metadata", {})
        row = dict(payload)
        row.update({f"anatomy__{key}": value for key, value in metadata.items()})
        rows.append(row)
    return pd.DataFrame(rows)


def snapshots_to_frame(snapshots: Iterable[FeatureSnapshot]) -> pd.DataFrame:
    return pd.DataFrame([snapshot.as_flat_dict() for snapshot in snapshots])


def candidates_to_frame(candidates: Iterable[TradeCandidate]) -> pd.DataFrame:
    rows = []
    for candidate in candidates:
        candidate.validate()
        payload = asdict(candidate)
        payload["direction"] = candidate.direction.value
        payload["state"] = candidate.state.value
        payload["created_time_utc"] = candidate.created_time_utc.isoformat()
        payload["eligible_from_utc"] = candidate.eligible_from_utc.isoformat()
        payload["expires_at_utc"] = candidate.expires_at_utc.isoformat()
        payload["policy_parameters"] = dict(candidate.policy_parameters)
        rows.append(payload)
    return pd.DataFrame(rows)


def outcomes_to_frame(outcomes: Iterable[OutcomeRecord]) -> pd.DataFrame:
    rows = []
    for outcome in outcomes:
        outcome.validate()
        payload = asdict(outcome)
        for key in ("fill_time_utc", "exit_time_utc", "label_end_time_utc"):
            value = payload[key]
            payload[key] = value.isoformat() if value is not None else None
        payload["metadata"] = dict(outcome.metadata)
        rows.append(payload)
    return pd.DataFrame(rows)


def assemble_model_dataset(
    events: pd.DataFrame,
    snapshots: pd.DataFrame,
    candidates: pd.DataFrame,
    outcomes: pd.DataFrame,
) -> pd.DataFrame:
    """Build a candidate-level model table without silently dropping rows."""
    for frame, keys, name in (
        (events, ("event_id",), "events"),
        (snapshots, ("event_id",), "snapshots"),
        (candidates, ("candidate_id", "event_id"), "candidates"),
        (outcomes, ("candidate_id", "event_id"), "outcomes"),
    ):
        missing = [key for key in keys if key not in frame.columns]
        if missing:
            raise KeyError(f"{name} missing keys: {missing}")

    if events["event_id"].duplicated().any():
        raise ValueError("events.event_id must be unique")
    if snapshots["event_id"].duplicated().any():
        raise ValueError("snapshots.event_id must be unique")
    if candidates["candidate_id"].duplicated().any():
        raise ValueError("candidates.candidate_id must be unique")
    if outcomes["candidate_id"].duplicated().any():
        raise ValueError("outcomes.candidate_id must be unique")

    event_cols = [col for col in events.columns if col != "metadata"]
    snapshot_cols = [col for col in snapshots.columns if col not in {"snapshot_id"}]
    result = candidates.merge(outcomes, on=["candidate_id", "event_id"], how="left", validate="one_to_one", suffixes=("", "__outcome"))
    result = result.merge(events[event_cols], on="event_id", how="left", validate="many_to_one", suffixes=("", "__event"))
    result = result.merge(snapshots[snapshot_cols], on="event_id", how="left", validate="many_to_one", suffixes=("", "__feature"))
    if result["strategy_id"].isna().any():
        raise ValueError("candidate references missing event")
    if result["snapshot_time_utc"].isna().any():
        raise ValueError("candidate references missing snapshot")
    return result
