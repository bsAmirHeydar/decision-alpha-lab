from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Any

from .canonical import content_hash, stable_id
from .enums import (
    BindingStatus,
    ConstraintKind,
    DiffClass,
    EvidenceRole,
    MonotonicDirection,
    Operator,
    PackageStatus,
    ParameterType,
    PrimitiveKind,
    ProgramStatus,
    Severity,
    StateKind,
)


@dataclass(frozen=True)
class TreatmentDslAuthorityBoundary:
    read_hypergraph: bool = True
    read_handoff: bool = True
    define_finite_dsl: bool = True
    canonicalize_program: bool = True
    validate_program: bool = True
    bind_external_descriptor: bool = True
    replay_and_diff: bool = True
    mutate_ucee_truth: bool = False
    mutate_hypergraph: bool = False
    infer_context_truth: bool = False
    generate_unbounded_actions: bool = False
    solve_action_lattice: bool = False
    select_treatment: bool = False
    train_model: bool = False
    allocate_risk: bool = False
    activate_runtime: bool = False
    send_order: bool = False
    network_access: bool = False

    def to_dict(self) -> dict[str, bool]:
        return asdict(self)


@dataclass(frozen=True)
class ParameterDefinition:
    name: str
    parameter_type: ParameterType
    units: str
    default: Any
    minimum: Any | None = None
    maximum: Any | None = None
    allowed_values: tuple[str, ...] = ()
    required: bool = False
    identity_affecting: bool = True
    monotonic_direction: MonotonicDirection = MonotonicDirection.NONE
    description: str = ""

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "parameter_type": self.parameter_type.value,
            "units": self.units,
            "default": self.default,
            "minimum": self.minimum,
            "maximum": self.maximum,
            "allowed_values": sorted(self.allowed_values),
            "required": self.required,
            "identity_affecting": self.identity_affecting,
            "monotonic_direction": self.monotonic_direction.value,
            "description": self.description,
        }


@dataclass(frozen=True)
class PrimitiveDefinition:
    primitive_id: str
    exact_version: str
    kind: PrimitiveKind
    family: str
    parameters: tuple[ParameterDefinition, ...]
    required_capabilities: tuple[str, ...] = ()
    supported_sides: tuple[str, ...] = ("long", "short")
    semantic_labels: tuple[tuple[str, Any], ...] = ()
    path_dependent: bool = False
    description: str = ""

    @property
    def exact_key(self) -> str:
        return f"{self.primitive_id}@{self.exact_version}"

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "primitive_id": self.primitive_id,
            "exact_version": self.exact_version,
            "kind": self.kind.value,
            "family": self.family,
            "parameters": [
                item.semantic_payload() for item in sorted(self.parameters, key=lambda item: item.name)
            ],
            "required_capabilities": sorted(self.required_capabilities),
            "supported_sides": sorted(self.supported_sides),
            "semantic_labels": {key: value for key, value in sorted(self.semantic_labels)},
            "path_dependent": self.path_dependent,
            "description": self.description,
        }

    @property
    def definition_id(self) -> str:
        return stable_id("dslprim", self.semantic_payload())

    @property
    def definition_hash(self) -> str:
        return content_hash(self.semantic_payload())


@dataclass(frozen=True)
class TreatmentDslRegistry:
    registry_name: str
    exact_version: str
    primitives: tuple[PrimitiveDefinition, ...]
    authority: TreatmentDslAuthorityBoundary
    limitations: tuple[str, ...] = ()

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "registry_name": self.registry_name,
            "exact_version": self.exact_version,
            "primitives": [
                item.semantic_payload() for item in sorted(self.primitives, key=lambda item: item.exact_key)
            ],
            "authority": self.authority.to_dict(),
            "limitations": sorted(self.limitations),
        }

    @property
    def registry_id(self) -> str:
        return stable_id("dslreg", self.semantic_payload())

    @property
    def registry_hash(self) -> str:
        return content_hash(self.semantic_payload())


@dataclass(frozen=True)
class TreatmentDslPolicy:
    policy_name: str
    exact_version: str
    maximum_programs: int
    maximum_components_per_program: int
    maximum_parameters_per_program: int
    maximum_constraints_per_program: int
    maximum_states_per_program: int
    maximum_transitions_per_program: int
    allowed_units: tuple[str, ...]
    allowed_evidence_roles: tuple[EvidenceRole, ...]
    required_component_kinds: tuple[PrimitiveKind, ...]
    singleton_component_kinds: tuple[PrimitiveKind, ...]
    prohibited_identifier_tokens: tuple[str, ...]
    prohibited_parameter_tokens: tuple[str, ...]
    require_skip: bool
    require_abstain: bool
    require_exact_hypergraph_handoff: bool
    deterministic_partition_count: int

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "policy_name": self.policy_name,
            "exact_version": self.exact_version,
            "maximum_programs": self.maximum_programs,
            "maximum_components_per_program": self.maximum_components_per_program,
            "maximum_parameters_per_program": self.maximum_parameters_per_program,
            "maximum_constraints_per_program": self.maximum_constraints_per_program,
            "maximum_states_per_program": self.maximum_states_per_program,
            "maximum_transitions_per_program": self.maximum_transitions_per_program,
            "allowed_units": sorted(self.allowed_units),
            "allowed_evidence_roles": sorted(item.value for item in self.allowed_evidence_roles),
            "required_component_kinds": sorted(item.value for item in self.required_component_kinds),
            "singleton_component_kinds": sorted(item.value for item in self.singleton_component_kinds),
            "prohibited_identifier_tokens": sorted(self.prohibited_identifier_tokens),
            "prohibited_parameter_tokens": sorted(self.prohibited_parameter_tokens),
            "require_skip": self.require_skip,
            "require_abstain": self.require_abstain,
            "require_exact_hypergraph_handoff": self.require_exact_hypergraph_handoff,
            "deterministic_partition_count": self.deterministic_partition_count,
        }

    @property
    def policy_id(self) -> str:
        return stable_id("dslpolicy", self.semantic_payload())

    @property
    def policy_hash(self) -> str:
        return content_hash(self.semantic_payload())


@dataclass(frozen=True)
class CapabilityProfile:
    profile_name: str
    exact_version: str
    capabilities: tuple[str, ...]
    order_types: tuple[str, ...]
    time_in_force: tuple[str, ...]
    maximum_entry_legs: int
    supports_server_stop: bool
    supports_partial_exit: bool
    supports_trailing: bool
    supports_expiration: bool
    diagnostic_only: bool = True

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "profile_name": self.profile_name,
            "exact_version": self.exact_version,
            "capabilities": sorted(self.capabilities),
            "order_types": sorted(self.order_types),
            "time_in_force": sorted(self.time_in_force),
            "maximum_entry_legs": self.maximum_entry_legs,
            "supports_server_stop": self.supports_server_stop,
            "supports_partial_exit": self.supports_partial_exit,
            "supports_trailing": self.supports_trailing,
            "supports_expiration": self.supports_expiration,
            "diagnostic_only": self.diagnostic_only,
        }

    @property
    def profile_id(self) -> str:
        return stable_id("capability", self.semantic_payload())

    @property
    def profile_hash(self) -> str:
        return content_hash(self.semantic_payload())


@dataclass(frozen=True)
class ProgramComponentSource:
    slot: str
    primitive_id: str
    exact_version: str
    parameters: tuple[tuple[str, Any], ...]

    @property
    def exact_key(self) -> str:
        return f"{self.primitive_id}@{self.exact_version}"


@dataclass(frozen=True)
class ConstraintDeclaration:
    constraint_name: str
    kind: ConstraintKind
    left_ref: str
    operator: Operator
    right_value: Any | None
    right_ref: str | None
    severity: Severity
    description: str = ""

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "constraint_name": self.constraint_name,
            "kind": self.kind.value,
            "left_ref": self.left_ref,
            "operator": self.operator.value,
            "right_value": self.right_value,
            "right_ref": self.right_ref,
            "severity": self.severity.value,
            "description": self.description,
        }


@dataclass(frozen=True)
class StateDefinition:
    state_name: str
    kind: StateKind
    description: str = ""


@dataclass(frozen=True)
class TransitionDefinition:
    transition_name: str
    from_state: str
    to_state: str
    guard_constraint: str | None
    terminal_action: str | None


@dataclass(frozen=True)
class TreatmentProgramSource:
    program_name: str
    exact_version: str
    descriptor_id: str | None
    side_scope: tuple[str, ...]
    components: tuple[ProgramComponentSource, ...]
    constraints: tuple[ConstraintDeclaration, ...]
    states: tuple[StateDefinition, ...]
    transitions: tuple[TransitionDefinition, ...]
    semantic_labels: tuple[tuple[str, Any], ...]
    evidence_role: EvidenceRole
    known_as_of: str
    source_artifact_hash: str
    limitations: tuple[str, ...] = ()


@dataclass(frozen=True)
class CanonicalComponent:
    slot: str
    primitive_definition_id: str
    primitive_key: str
    kind: PrimitiveKind
    parameters: tuple[tuple[str, Any], ...]
    component_hash: str

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "slot": self.slot,
            "primitive_definition_id": self.primitive_definition_id,
            "primitive_key": self.primitive_key,
            "kind": self.kind.value,
            "parameters": {key: value for key, value in sorted(self.parameters)},
        }


@dataclass(frozen=True)
class CanonicalTreatmentProgram:
    program_id: str
    program_name: str
    exact_version: str
    descriptor_id: str | None
    side_scope: tuple[str, ...]
    components: tuple[CanonicalComponent, ...]
    constraints: tuple[ConstraintDeclaration, ...]
    states: tuple[StateDefinition, ...]
    transitions: tuple[TransitionDefinition, ...]
    semantic_labels: tuple[tuple[str, Any], ...]
    evidence_role: EvidenceRole
    known_as_of: str
    source_artifact_hash: str
    registry_hash: str
    capability_profile_hash: str
    status: ProgramStatus
    reason_codes: tuple[str, ...]
    program_hash: str
    limitations: tuple[str, ...]

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "program_id": self.program_id,
            "program_name": self.program_name,
            "exact_version": self.exact_version,
            "descriptor_id": self.descriptor_id,
            "side_scope": sorted(self.side_scope),
            "components": [item.semantic_payload() | {"component_hash": item.component_hash} for item in sorted(self.components, key=lambda x: x.slot)],
            "constraints": [item.semantic_payload() for item in sorted(self.constraints, key=lambda x: x.constraint_name)],
            "states": [asdict(item) | {"kind": item.kind.value} for item in sorted(self.states, key=lambda x: x.state_name)],
            "transitions": [asdict(item) for item in sorted(self.transitions, key=lambda x: x.transition_name)],
            "semantic_labels": {key: value for key, value in sorted(self.semantic_labels)},
            "evidence_role": self.evidence_role.value,
            "known_as_of": self.known_as_of,
            "source_artifact_hash": self.source_artifact_hash,
            "registry_hash": self.registry_hash,
            "capability_profile_hash": self.capability_profile_hash,
            "status": self.status.value,
            "reason_codes": sorted(self.reason_codes),
            "limitations": sorted(self.limitations),
        }


@dataclass(frozen=True)
class ProgramValidationResult:
    program_name: str
    exact_version: str
    status: ProgramStatus
    reason_codes: tuple[str, ...]
    diagnostics: tuple[str, ...]
    checked_component_count: int
    checked_parameter_count: int
    checked_constraint_count: int
    checked_state_count: int
    checked_transition_count: int

    @property
    def result_id(self) -> str:
        return stable_id("dslvalidation", asdict(self))


@dataclass(frozen=True)
class DescriptorBinding:
    binding_id: str
    descriptor_id: str
    graph_node_id: str
    graph_node_hash: str
    program_id: str
    program_hash: str
    status: BindingStatus
    evidence_role: EvidenceRole
    known_as_of: str
    matched_labels: tuple[str, ...]
    reason_codes: tuple[str, ...]
    binding_hash: str

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "binding_id": self.binding_id,
            "descriptor_id": self.descriptor_id,
            "graph_node_id": self.graph_node_id,
            "graph_node_hash": self.graph_node_hash,
            "program_id": self.program_id,
            "program_hash": self.program_hash,
            "status": self.status.value,
            "evidence_role": self.evidence_role.value,
            "known_as_of": self.known_as_of,
            "matched_labels": sorted(self.matched_labels),
            "reason_codes": sorted(self.reason_codes),
        }


@dataclass(frozen=True)
class TreatmentDslPackage:
    package_id: str
    package_version: str
    registry_id: str
    registry_hash: str
    policy_id: str
    policy_hash: str
    capability_profile_id: str
    capability_profile_hash: str
    source_graph_id: str
    source_graph_hash: str
    source_handoff_id: str
    source_handoff_hash: str
    evidence_role: EvidenceRole
    known_as_of: str
    status: PackageStatus
    programs: tuple[CanonicalTreatmentProgram, ...]
    validations: tuple[ProgramValidationResult, ...]
    bindings: tuple[DescriptorBinding, ...]
    lineage_root: str
    package_hash: str
    limitations: tuple[str, ...]

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "package_id": self.package_id,
            "package_version": self.package_version,
            "registry_id": self.registry_id,
            "registry_hash": self.registry_hash,
            "policy_id": self.policy_id,
            "policy_hash": self.policy_hash,
            "capability_profile_id": self.capability_profile_id,
            "capability_profile_hash": self.capability_profile_hash,
            "source_graph_id": self.source_graph_id,
            "source_graph_hash": self.source_graph_hash,
            "source_handoff_id": self.source_handoff_id,
            "source_handoff_hash": self.source_handoff_hash,
            "evidence_role": self.evidence_role.value,
            "known_as_of": self.known_as_of,
            "status": self.status.value,
            "programs": [item.semantic_payload() | {"program_hash": item.program_hash} for item in sorted(self.programs, key=lambda x: x.program_id)],
            "validations": [asdict(item) | {"status": item.status.value} for item in sorted(self.validations, key=lambda x: x.program_name)],
            "bindings": [item.semantic_payload() | {"binding_hash": item.binding_hash} for item in sorted(self.bindings, key=lambda x: x.binding_id)],
            "lineage_root": self.lineage_root,
            "limitations": sorted(self.limitations),
        }


@dataclass(frozen=True)
class DslIntegrityReceipt:
    receipt_id: str
    package_id: str
    package_hash: str
    registry_hash: str
    policy_hash: str
    capability_profile_hash: str
    source_graph_hash: str
    source_handoff_hash: str
    program_hashes: tuple[str, ...]
    binding_hashes: tuple[str, ...]
    lineage_root: str
    verified: bool
    reason_codes: tuple[str, ...]


@dataclass(frozen=True)
class DslReplayReceipt:
    replay_id: str
    original_package_hash: str
    rebuilt_package_hash: str
    identical: bool
    differing_paths: tuple[str, ...]


@dataclass(frozen=True)
class DslDiff:
    diff_id: str
    left_package_hash: str
    right_package_hash: str
    classification: DiffClass
    added_program_ids: tuple[str, ...]
    removed_program_ids: tuple[str, ...]
    changed_program_ids: tuple[str, ...]
    changed_binding_ids: tuple[str, ...]


@dataclass(frozen=True)
class DslTelemetry:
    telemetry_id: str
    package_id: str
    package_hash: str
    program_count: int
    component_count: int
    parameter_count: int
    constraint_count: int
    state_count: int
    transition_count: int
    bound_descriptor_count: int
    rejected_program_count: int
    skip_present: bool
    abstain_present: bool
    authority_violation_count: int


@dataclass(frozen=True)
class DslPartitionManifest:
    manifest_id: str
    package_id: str
    package_hash: str
    partition_count: int
    assignments: tuple[tuple[str, int], ...]
    manifest_hash: str
