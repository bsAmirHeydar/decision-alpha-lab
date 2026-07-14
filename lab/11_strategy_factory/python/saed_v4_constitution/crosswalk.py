"""Exact UCEE I01-I18 authority and artifact crosswalk."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import content_hash


@dataclass(frozen=True)
class CrosswalkEntry:
    phase: str
    capability: str
    saed_consumes: tuple[str, ...]
    saed_emits: tuple[str, ...]
    authority_owner: str
    mutation_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "phase": self.phase,
            "capability": self.capability,
            "saed_consumes": list(self.saed_consumes),
            "saed_emits": list(self.saed_emits),
            "authority_owner": self.authority_owner,
            "mutation_allowed": self.mutation_allowed,
        }


DEFAULT_CROSSWALK = (
    CrosswalkEntry("I01-I04", "canonical context truth and known-time lifecycle", ("context packages", "occurrences"), ("read-only references",), "UCEE", False),
    CrosswalkEntry("I05-I10", "features, labels, datasets, folds and multiview support", ("feature snapshots", "fold manifests"), ("research manifests",), "UCEE", False),
    CrosswalkEntry("I11", "experiment orchestration and complete trial identity", ("experiment contracts",), ("trial/exposure events",), "UCEE", False),
    CrosswalkEntry("I12", "statistical challenge and promotion", ("candidate dossiers",), ("challenge evidence",), "UCEE", False),
    CrosswalkEntry("I13", "bounded manual/AI/hybrid policy", ("promotion admission",), ("policy proposal only",), "UCEE", False),
    CrosswalkEntry("I14", "immutable runtime and parity", ("compiled bundle contracts",), ("runtime handoff request",), "UCEE", False),
    CrosswalkEntry("I15", "context treatment tournament", ("tournament template",), ("candidate treatment evidence",), "UCEE", False),
    CrosswalkEntry("I16", "context onboarding", ("context specification",), ("cell onboarding artifacts",), "UCEE", False),
    CrosswalkEntry("I17", "risk reservation, portfolio allocation and capacity", ("portfolio constraints",), ("edge genome proposal",), "UCEE", False),
    CrosswalkEntry("I18", "production qualification, authorization and recovery", ("release evidence policy",), ("qualification evidence request",), "UCEE", False),
)


def build_crosswalk(entries: tuple[CrosswalkEntry, ...] = DEFAULT_CROSSWALK) -> dict[str, Any]:
    payload = {"schema_version": "4.0.0", "entries": [e.to_dict() for e in entries]}
    payload["crosswalk_hash"] = content_hash(payload)
    return payload


def validate_no_mutation(crosswalk: dict[str, Any]) -> bool:
    return all(not bool(entry.get("mutation_allowed")) for entry in crosswalk.get("entries", []))
