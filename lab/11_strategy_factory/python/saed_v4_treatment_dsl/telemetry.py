from __future__ import annotations

from .canonical import stable_id
from .enums import PrimitiveKind, ProgramStatus
from .models import DslTelemetry, TreatmentDslPackage, TreatmentDslRegistry


def build_telemetry(package: TreatmentDslPackage, registry: TreatmentDslRegistry) -> DslTelemetry:
    primitive_index = {item.definition_id: item for item in registry.primitives}
    action_families = {
        primitive_index[component.primitive_definition_id].family
        for program in package.programs
        for component in program.components
        if primitive_index[component.primitive_definition_id].kind == PrimitiveKind.ACTION
    }
    payload = {
        "package_id": package.package_id,
        "package_hash": package.package_hash,
        "program_count": len(package.programs),
        "component_count": sum(len(item.components) for item in package.programs),
        "parameter_count": sum(len(component.parameters) for item in package.programs for component in item.components),
        "constraint_count": sum(len(item.constraints) for item in package.programs),
        "state_count": sum(len(item.states) for item in package.programs),
        "transition_count": sum(len(item.transitions) for item in package.programs),
        "bound_descriptor_count": len(package.bindings),
        "rejected_program_count": sum(item.status == ProgramStatus.REJECTED for item in package.validations),
        "skip_present": "skip" in action_families,
        "abstain_present": "abstain" in action_families,
        "authority_violation_count": 0,
    }
    return DslTelemetry(stable_id("dsltelemetry", payload), **payload)
