from __future__ import annotations

from .canonical import content_hash, stable_id
from .enums import ProgramStatus
from .models import (
    CanonicalComponent,
    CanonicalTreatmentProgram,
    CapabilityProfile,
    TreatmentDslRegistry,
    TreatmentProgramSource,
)


def canonicalize_program(
    source: TreatmentProgramSource,
    registry: TreatmentDslRegistry,
    capability_profile: CapabilityProfile,
) -> CanonicalTreatmentProgram:
    index = {item.exact_key: item for item in registry.primitives}
    components = []
    for item in source.components:
        primitive = index[item.exact_key]
        supplied = dict(item.parameters)
        bound = tuple(
            sorted(
                (parameter.name, supplied.get(parameter.name, parameter.default))
                for parameter in primitive.parameters
                if parameter.identity_affecting
            )
        )
        payload = {
            "slot": item.slot,
            "primitive_definition_id": primitive.definition_id,
            "primitive_key": primitive.exact_key,
            "kind": primitive.kind.value,
            "parameters": dict(bound),
        }
        components.append(
            CanonicalComponent(
                slot=item.slot,
                primitive_definition_id=primitive.definition_id,
                primitive_key=primitive.exact_key,
                kind=primitive.kind,
                parameters=bound,
                component_hash=content_hash(payload),
            )
        )
    seed = {
        "program_name": source.program_name,
        "exact_version": source.exact_version,
        "descriptor_id": source.descriptor_id,
        "side_scope": sorted(source.side_scope),
        "components": [item.semantic_payload() for item in sorted(components, key=lambda x: x.slot)],
        "constraints": [item.semantic_payload() for item in sorted(source.constraints, key=lambda x: x.constraint_name)],
        "states": [
            {"state_name": item.state_name, "kind": item.kind.value, "description": item.description}
            for item in sorted(source.states, key=lambda x: x.state_name)
        ],
        "transitions": [
            {
                "transition_name": item.transition_name,
                "from_state": item.from_state,
                "to_state": item.to_state,
                "guard_constraint": item.guard_constraint,
                "terminal_action": item.terminal_action,
            }
            for item in sorted(source.transitions, key=lambda x: x.transition_name)
        ],
        "semantic_labels": dict(sorted(source.semantic_labels)),
        "evidence_role": source.evidence_role.value,
        "known_as_of": source.known_as_of,
        "source_artifact_hash": source.source_artifact_hash,
        "registry_hash": registry.registry_hash,
        "capability_profile_hash": capability_profile.profile_hash,
        "status": ProgramStatus.ACCEPTED.value,
        "reason_codes": [],
        "limitations": sorted(set(source.limitations) | {
            "V4-06 defines and validates a finite program; it does not solve an action lattice.",
            "The program cannot allocate capital, select itself, activate runtime, or send orders.",
        }),
    }
    program_id = stable_id("treatment", seed)
    draft = CanonicalTreatmentProgram(
        program_id=program_id,
        program_name=source.program_name,
        exact_version=source.exact_version,
        descriptor_id=source.descriptor_id,
        side_scope=tuple(sorted(source.side_scope)),
        components=tuple(sorted(components, key=lambda x: x.slot)),
        constraints=tuple(sorted(source.constraints, key=lambda x: x.constraint_name)),
        states=tuple(sorted(source.states, key=lambda x: x.state_name)),
        transitions=tuple(sorted(source.transitions, key=lambda x: x.transition_name)),
        semantic_labels=tuple(sorted(source.semantic_labels)),
        evidence_role=source.evidence_role,
        known_as_of=source.known_as_of,
        source_artifact_hash=source.source_artifact_hash,
        registry_hash=registry.registry_hash,
        capability_profile_hash=capability_profile.profile_hash,
        status=ProgramStatus.ACCEPTED,
        reason_codes=(),
        program_hash="",
        limitations=tuple(seed["limitations"]),
    )
    return CanonicalTreatmentProgram(**{**draft.__dict__, "program_hash": content_hash(draft.semantic_payload())})
