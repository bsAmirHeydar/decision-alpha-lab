from __future__ import annotations

from typing import Any, Mapping, Sequence

from .canonical import content_hash, merkle_root, stable_id
from .canonicalizer import canonicalize_program
from .enums import PackageStatus
from .errors import ProgramError
from .graph_binding import bind_descriptor, validate_handoff
from .models import (
    CapabilityProfile,
    TreatmentDslPackage,
    TreatmentDslPolicy,
    TreatmentDslRegistry,
    TreatmentProgramSource,
)
from .registry import validate_capability_profile, validate_policy, validate_registry
from .static_analysis import StaticTreatmentAnalyzer, require_accepted
from .validation import validate_package


class TreatmentDslService:
    """Deterministic V4-06 service for finite DSL definition, validation and exact binding."""

    def __init__(self) -> None:
        self.analyzer = StaticTreatmentAnalyzer()

    def build_package(
        self,
        *,
        graph: Mapping[str, Any],
        handoff: Mapping[str, Any],
        registry: TreatmentDslRegistry,
        policy: TreatmentDslPolicy,
        capability_profile: CapabilityProfile,
        sources: Sequence[TreatmentProgramSource],
        package_version: str = "1.0.0",
    ) -> TreatmentDslPackage:
        validate_policy(policy)
        validate_registry(registry, policy)
        validate_capability_profile(capability_profile)
        validate_handoff(graph, handoff)
        if len(sources) > policy.maximum_programs:
            raise ProgramError("program budget exceeded")
        if graph["evidence_role"] not in {item.value for item in policy.allowed_evidence_roles}:
            raise ProgramError("graph Evidence Role is not permitted by policy")
        validations = []
        programs = []
        for source in sorted(sources, key=lambda item: (item.program_name, item.exact_version)):
            result = self.analyzer.analyze(source, registry, policy, capability_profile)
            validations.append(result)
            require_accepted(result)
            programs.append(canonicalize_program(source, registry, capability_profile))
        bindings = []
        for program in programs:
            if program.descriptor_id is not None:
                bindings.append(bind_descriptor(graph, program))
        lineage_root = merkle_root([
            registry.registry_hash,
            policy.policy_hash,
            capability_profile.profile_hash,
            graph["graph_hash"],
            handoff["handoff_hash"],
            *(item.program_hash for item in programs),
            *(item.binding_hash for item in bindings),
        ])
        seed = {
            "package_version": package_version,
            "registry_hash": registry.registry_hash,
            "policy_hash": policy.policy_hash,
            "capability_profile_hash": capability_profile.profile_hash,
            "source_graph_hash": graph["graph_hash"],
            "source_handoff_hash": handoff["handoff_hash"],
            "evidence_role": graph["evidence_role"],
            "known_as_of": graph["known_as_of"],
            "program_hashes": sorted(item.program_hash for item in programs),
            "binding_hashes": sorted(item.binding_hash for item in bindings),
        }
        package_id = stable_id("dslpackage", seed)
        draft = TreatmentDslPackage(
            package_id=package_id,
            package_version=package_version,
            registry_id=registry.registry_id,
            registry_hash=registry.registry_hash,
            policy_id=policy.policy_id,
            policy_hash=policy.policy_hash,
            capability_profile_id=capability_profile.profile_id,
            capability_profile_hash=capability_profile.profile_hash,
            source_graph_id=graph["graph_id"],
            source_graph_hash=graph["graph_hash"],
            source_handoff_id=handoff["handoff_id"],
            source_handoff_hash=handoff["handoff_hash"],
            evidence_role=programs[0].evidence_role if programs else next(iter(policy.allowed_evidence_roles)),
            known_as_of=graph["known_as_of"],
            status=PackageStatus.COMPLETE,
            programs=tuple(programs),
            validations=tuple(validations),
            bindings=tuple(sorted(bindings, key=lambda item: item.binding_id)),
            lineage_root=lineage_root,
            package_hash="",
            limitations=(
                "V4-06 freezes a finite typed Treatment DSL but does not solve or enumerate the V4-07 action lattice.",
                "No program in this package has model, selection, capital, runtime, broker, or order authority.",
                "MQL5 artifacts are diagnostic mirrors until actual MetaEditor evidence is attached.",
            ),
        )
        package = TreatmentDslPackage(**{**draft.__dict__, "package_hash": content_hash(draft.semantic_payload())})
        validate_package(package, registry, policy)
        return package
