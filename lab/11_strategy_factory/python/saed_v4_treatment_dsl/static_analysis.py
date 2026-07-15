from __future__ import annotations

import math
from collections import Counter, defaultdict, deque
from decimal import Decimal, InvalidOperation
from typing import Any

from .enums import ParameterType, PrimitiveKind, ProgramStatus, StateKind
from .errors import ProgramError
from .models import (
    CapabilityProfile,
    PrimitiveDefinition,
    ProgramValidationResult,
    TreatmentDslPolicy,
    TreatmentDslRegistry,
    TreatmentProgramSource,
)
from .registry import IDENTIFIER, VERSION


class StaticTreatmentAnalyzer:
    """Fail-closed static analyzer. It does not solve or enumerate an action lattice."""

    def analyze(
        self,
        source: TreatmentProgramSource,
        registry: TreatmentDslRegistry,
        policy: TreatmentDslPolicy,
        capability_profile: CapabilityProfile,
    ) -> ProgramValidationResult:
        reasons: list[str] = []
        diagnostics: list[str] = []
        primitive_index = {item.exact_key: item for item in registry.primitives}
        if not IDENTIFIER.fullmatch(source.program_name):
            reasons.append("invalid_program_name")
        if not VERSION.fullmatch(source.exact_version):
            reasons.append("invalid_exact_version")
        if source.evidence_role not in policy.allowed_evidence_roles:
            reasons.append("evidence_role_not_allowed")
        if len(source.components) > policy.maximum_components_per_program:
            reasons.append("component_budget_exceeded")
        if len(source.constraints) > policy.maximum_constraints_per_program:
            reasons.append("constraint_budget_exceeded")
        if len(source.states) > policy.maximum_states_per_program:
            reasons.append("state_budget_exceeded")
        if len(source.transitions) > policy.maximum_transitions_per_program:
            reasons.append("transition_budget_exceeded")
        if set(source.side_scope) - {"long", "short", "none"} or not source.side_scope:
            reasons.append("invalid_side_scope")
        slots = [item.slot for item in source.components]
        if len(slots) != len(set(slots)):
            reasons.append("duplicate_component_slot")
        for slot in slots:
            if not IDENTIFIER.fullmatch(slot):
                reasons.append("invalid_component_slot")
        resolved: list[PrimitiveDefinition] = []
        parameter_count = 0
        for component in source.components:
            primitive = primitive_index.get(component.exact_key)
            if primitive is None:
                reasons.append("unknown_exact_primitive")
                diagnostics.append(component.exact_key)
                continue
            resolved.append(primitive)
            if not set(source.side_scope).issubset(set(primitive.supported_sides)):
                reasons.append("unsupported_side")
                diagnostics.append(component.slot)
            supplied = dict(component.parameters)
            definitions = {item.name: item for item in primitive.parameters}
            unknown = sorted(set(supplied) - set(definitions))
            if unknown:
                reasons.append("unknown_parameter")
                diagnostics.extend(f"{component.slot}.{name}" for name in unknown)
            parameter_count += len(definitions)
            for name, definition in definitions.items():
                value = supplied.get(name, definition.default)
                code = self._validate_parameter(definition, value)
                if code:
                    reasons.append(code)
                    diagnostics.append(f"{component.slot}.{name}")
            missing_capabilities = sorted(set(primitive.required_capabilities) - set(capability_profile.capabilities))
            if missing_capabilities:
                reasons.append("missing_capability")
                diagnostics.extend(missing_capabilities)
        if parameter_count > policy.maximum_parameters_per_program:
            reasons.append("parameter_budget_exceeded")
        kind_counts = Counter(item.kind for item in resolved)
        is_action = kind_counts[PrimitiveKind.ACTION] > 0
        if is_action:
            if len(resolved) != 1 or any(kind != PrimitiveKind.ACTION for kind in kind_counts):
                reasons.append("action_must_be_isolated")
            if source.descriptor_id is not None:
                reasons.append("system_action_cannot_bind_descriptor")
        else:
            for required in policy.required_component_kinds:
                if kind_counts[required] == 0:
                    reasons.append(f"missing_required_component:{required.value}")
            for singleton in policy.singleton_component_kinds:
                if kind_counts[singleton] > 1:
                    reasons.append(f"singleton_component_repeated:{singleton.value}")
        lowered_identifiers = " ".join([source.program_name, *(item.slot for item in source.components)]).lower()
        if any(token in lowered_identifiers for token in policy.prohibited_identifier_tokens):
            reasons.append("prohibited_identifier_token")
        self._validate_constraints(source, slots, reasons, diagnostics)
        self._validate_state_machine(source, reasons, diagnostics)
        if len(source.source_artifact_hash) != 64 or any(ch not in "0123456789abcdef" for ch in source.source_artifact_hash):
            reasons.append("invalid_source_artifact_hash")
        unique_reasons = tuple(sorted(set(reasons)))
        return ProgramValidationResult(
            program_name=source.program_name,
            exact_version=source.exact_version,
            status=ProgramStatus.ACCEPTED if not unique_reasons else ProgramStatus.REJECTED,
            reason_codes=unique_reasons,
            diagnostics=tuple(sorted(set(diagnostics))),
            checked_component_count=len(source.components),
            checked_parameter_count=parameter_count,
            checked_constraint_count=len(source.constraints),
            checked_state_count=len(source.states),
            checked_transition_count=len(source.transitions),
        )

    @staticmethod
    def _validate_parameter(definition, value: Any) -> str | None:
        kind = definition.parameter_type
        if value is None and not definition.required:
            return None
        if kind == ParameterType.BOOLEAN:
            if not isinstance(value, bool):
                return "parameter_type_mismatch"
        elif kind in (ParameterType.INTEGER, ParameterType.DURATION_MS):
            if isinstance(value, bool) or not isinstance(value, int):
                return "parameter_type_mismatch"
            if kind == ParameterType.DURATION_MS and value < 0:
                return "negative_duration"
        elif kind == ParameterType.DECIMAL:
            try:
                number = Decimal(str(value))
                if not number.is_finite():
                    return "non_finite_decimal"
            except (InvalidOperation, ValueError):
                return "parameter_type_mismatch"
        elif kind in (ParameterType.STRING, ParameterType.ENUM):
            if not isinstance(value, str):
                return "parameter_type_mismatch"
            if kind == ParameterType.ENUM and value not in definition.allowed_values:
                return "enum_value_not_allowed"
        if kind in (ParameterType.INTEGER, ParameterType.DURATION_MS, ParameterType.DECIMAL):
            try:
                number = Decimal(str(value))
                if definition.minimum is not None and number < Decimal(str(definition.minimum)):
                    return "parameter_below_minimum"
                if definition.maximum is not None and number > Decimal(str(definition.maximum)):
                    return "parameter_above_maximum"
            except InvalidOperation:
                return "parameter_type_mismatch"
        return None

    @staticmethod
    def _validate_constraints(source, slots, reasons, diagnostics):
        names = [item.constraint_name for item in source.constraints]
        if len(names) != len(set(names)):
            reasons.append("duplicate_constraint_name")
        slot_set = set(slots)
        for constraint in source.constraints:
            if not IDENTIFIER.fullmatch(constraint.constraint_name):
                reasons.append("invalid_constraint_name")
            if constraint.left_ref.startswith("component:"):
                slot = constraint.left_ref.split(":", 1)[1].split(".", 1)[0]
                if slot not in slot_set:
                    reasons.append("constraint_unknown_component_ref")
                    diagnostics.append(constraint.left_ref)
            if constraint.right_ref and constraint.right_ref.startswith("component:"):
                slot = constraint.right_ref.split(":", 1)[1].split(".", 1)[0]
                if slot not in slot_set:
                    reasons.append("constraint_unknown_component_ref")
                    diagnostics.append(constraint.right_ref)
            if constraint.right_ref is not None and constraint.right_value is not None:
                reasons.append("constraint_ambiguous_right_operand")
            lowered = f"{constraint.left_ref} {constraint.right_ref or ''}".lower()
            if any(token in lowered for token in ("outcome", "label", "future", "realized_pnl", "forward_return")):
                reasons.append("constraint_prohibited_future_or_outcome_ref")

    @staticmethod
    def _validate_state_machine(source, reasons, diagnostics):
        if not source.states and not source.transitions:
            return
        names = [item.state_name for item in source.states]
        if len(names) != len(set(names)):
            reasons.append("duplicate_state_name")
            return
        initial = [item for item in source.states if item.kind == StateKind.INITIAL]
        terminal = [item for item in source.states if item.kind == StateKind.TERMINAL]
        if len(initial) != 1:
            reasons.append("state_machine_requires_one_initial")
        if not terminal:
            reasons.append("state_machine_requires_terminal")
        state_set = set(names)
        constraint_names = {item.constraint_name for item in source.constraints}
        transition_names = [item.transition_name for item in source.transitions]
        if len(transition_names) != len(set(transition_names)):
            reasons.append("duplicate_transition_name")
        adjacency = defaultdict(set)
        indegree = {name: 0 for name in names}
        for transition in source.transitions:
            if transition.from_state not in state_set or transition.to_state not in state_set:
                reasons.append("transition_unknown_state")
                diagnostics.append(transition.transition_name)
                continue
            if transition.guard_constraint and transition.guard_constraint not in constraint_names:
                reasons.append("transition_unknown_guard")
            if transition.from_state == transition.to_state:
                reasons.append("self_loop_transition")
            if transition.to_state not in adjacency[transition.from_state]:
                adjacency[transition.from_state].add(transition.to_state)
                indegree[transition.to_state] += 1
        queue = deque(sorted(name for name, degree in indegree.items() if degree == 0))
        visited = 0
        while queue:
            node = queue.popleft(); visited += 1
            for nxt in sorted(adjacency[node]):
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
        if visited != len(names):
            reasons.append("cyclic_management_state_machine")


def require_accepted(result: ProgramValidationResult) -> None:
    if result.status != ProgramStatus.ACCEPTED:
        raise ProgramError(
            f"Treatment program rejected: {result.program_name}@{result.exact_version}: "
            + ",".join(result.reason_codes)
        )
