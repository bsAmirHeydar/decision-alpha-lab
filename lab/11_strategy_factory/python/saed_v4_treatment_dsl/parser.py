from __future__ import annotations

from typing import Any, Mapping

from .enums import ConstraintKind, EvidenceRole, Operator, Severity, StateKind
from .errors import ContractError
from .models import (
    ConstraintDeclaration,
    ProgramComponentSource,
    StateDefinition,
    TransitionDefinition,
    TreatmentProgramSource,
)

REQUIRED_PROGRAM_FIELDS = {
    "program_name",
    "exact_version",
    "descriptor_id",
    "side_scope",
    "components",
    "constraints",
    "states",
    "transitions",
    "semantic_labels",
    "evidence_role",
    "known_as_of",
    "source_artifact_hash",
    "limitations",
}


def _closed(document: Mapping[str, Any], expected: set[str], label: str) -> None:
    unknown = set(document) - expected
    missing = expected - set(document)
    if unknown or missing:
        raise ContractError(f"{label} fields invalid; missing={sorted(missing)} unknown={sorted(unknown)}")


def parse_program(document: Mapping[str, Any]) -> TreatmentProgramSource:
    _closed(document, REQUIRED_PROGRAM_FIELDS, "program")
    components = tuple(_parse_component(item) for item in document["components"])
    constraints = tuple(_parse_constraint(item) for item in document["constraints"])
    states = tuple(_parse_state(item) for item in document["states"])
    transitions = tuple(_parse_transition(item) for item in document["transitions"])
    labels = document["semantic_labels"]
    if not isinstance(labels, dict):
        raise ContractError("semantic_labels must be an object")
    return TreatmentProgramSource(
        program_name=document["program_name"],
        exact_version=document["exact_version"],
        descriptor_id=document["descriptor_id"],
        side_scope=tuple(document["side_scope"]),
        components=components,
        constraints=constraints,
        states=states,
        transitions=transitions,
        semantic_labels=tuple(sorted(labels.items())),
        evidence_role=EvidenceRole(document["evidence_role"]),
        known_as_of=document["known_as_of"],
        source_artifact_hash=document["source_artifact_hash"],
        limitations=tuple(document["limitations"]),
    )


def _parse_component(document: Mapping[str, Any]) -> ProgramComponentSource:
    _closed(document, {"slot", "primitive_id", "exact_version", "parameters"}, "component")
    if not isinstance(document["parameters"], dict):
        raise ContractError("component parameters must be an object")
    return ProgramComponentSource(
        slot=document["slot"],
        primitive_id=document["primitive_id"],
        exact_version=document["exact_version"],
        parameters=tuple(sorted(document["parameters"].items())),
    )


def _parse_constraint(document: Mapping[str, Any]) -> ConstraintDeclaration:
    _closed(document, {"constraint_name", "kind", "left_ref", "operator", "right_value", "right_ref", "severity", "description"}, "constraint")
    return ConstraintDeclaration(
        constraint_name=document["constraint_name"],
        kind=ConstraintKind(document["kind"]),
        left_ref=document["left_ref"],
        operator=Operator(document["operator"]),
        right_value=document["right_value"],
        right_ref=document["right_ref"],
        severity=Severity(document["severity"]),
        description=document["description"],
    )


def _parse_state(document: Mapping[str, Any]) -> StateDefinition:
    _closed(document, {"state_name", "kind", "description"}, "state")
    return StateDefinition(document["state_name"], StateKind(document["kind"]), document["description"])


def _parse_transition(document: Mapping[str, Any]) -> TransitionDefinition:
    _closed(document, {"transition_name", "from_state", "to_state", "guard_constraint", "terminal_action"}, "transition")
    return TransitionDefinition(
        document["transition_name"],
        document["from_state"],
        document["to_state"],
        document["guard_constraint"],
        document["terminal_action"],
    )
