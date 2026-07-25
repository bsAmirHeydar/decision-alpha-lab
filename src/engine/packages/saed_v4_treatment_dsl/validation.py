from __future__ import annotations

from .canonical import content_hash, merkle_root
from .enums import PackageStatus, PrimitiveKind, ProgramStatus
from .errors import IntegrityError, ProgramError
from .models import TreatmentDslPackage, TreatmentDslPolicy, TreatmentDslRegistry


def validate_package(package: TreatmentDslPackage, registry: TreatmentDslRegistry, policy: TreatmentDslPolicy) -> None:
    if package.registry_id != registry.registry_id or package.registry_hash != registry.registry_hash:
        raise IntegrityError("registry identity mismatch")
    if package.policy_id != policy.policy_id or package.policy_hash != policy.policy_hash:
        raise IntegrityError("policy identity mismatch")
    if package.status not in (PackageStatus.COMPLETE, PackageStatus.DEGRADED):
        raise IntegrityError("only complete or explicitly degraded packages may be accepted")
    if any(item.status != ProgramStatus.ACCEPTED for item in package.programs):
        raise ProgramError("package contains non-accepted program")
    ids = [item.program_id for item in package.programs]
    hashes = [item.program_hash for item in package.programs]
    if len(ids) != len(set(ids)) or len(hashes) != len(set(hashes)):
        raise IntegrityError("duplicate canonical program identity")
    for item in package.programs:
        if content_hash(item.semantic_payload()) != item.program_hash:
            raise IntegrityError(f"program hash mismatch: {item.program_id}")
    for binding in package.bindings:
        if content_hash(binding.semantic_payload()) != binding.binding_hash:
            raise IntegrityError(f"binding hash mismatch: {binding.binding_id}")
        if binding.program_id not in set(ids):
            raise IntegrityError("binding references unknown program")
    action_families = set()
    primitive_index = {item.definition_id: item for item in registry.primitives}
    for program in package.programs:
        for component in program.components:
            primitive = primitive_index[component.primitive_definition_id]
            if primitive.kind == PrimitiveKind.ACTION:
                action_families.add(primitive.family)
    if policy.require_skip and "skip" not in action_families:
        raise IntegrityError("Skip action missing")
    if policy.require_abstain and "abstain" not in action_families:
        raise IntegrityError("Abstain action missing")
    expected_lineage = merkle_root([
        package.registry_hash,
        package.policy_hash,
        package.capability_profile_hash,
        package.source_graph_hash,
        package.source_handoff_hash,
        *(item.program_hash for item in package.programs),
        *(item.binding_hash for item in package.bindings),
    ])
    if expected_lineage != package.lineage_root:
        raise IntegrityError("lineage root mismatch")
    if content_hash(package.semantic_payload()) != package.package_hash:
        raise IntegrityError("package hash mismatch")
