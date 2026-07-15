from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation

from .authority import validate_authority
from .enums import ParameterType, PrimitiveKind
from .errors import RegistryError
from .models import CapabilityProfile, PrimitiveDefinition, TreatmentDslPolicy, TreatmentDslRegistry

IDENTIFIER = re.compile(r"^[a-z][a-z0-9_.-]{1,127}$")
VERSION = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?$")


def validate_identifier(value: str, field: str) -> None:
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise RegistryError(f"invalid {field}: {value!r}")


def validate_version(value: str) -> None:
    if not VERSION.fullmatch(value):
        raise RegistryError(f"invalid exact version: {value!r}")


def validate_registry(registry: TreatmentDslRegistry, policy: TreatmentDslPolicy | None = None) -> None:
    validate_authority(registry.authority)
    validate_identifier(registry.registry_name, "registry_name")
    validate_version(registry.exact_version)
    keys = [item.exact_key for item in registry.primitives]
    if len(keys) != len(set(keys)):
        raise RegistryError("duplicate exact primitive key")
    definition_ids = [item.definition_id for item in registry.primitives]
    if len(definition_ids) != len(set(definition_ids)):
        raise RegistryError("duplicate primitive definition identity")
    for primitive in registry.primitives:
        validate_primitive(primitive, policy)
    if not any(item.kind == PrimitiveKind.ACTION and item.family == "skip" for item in registry.primitives):
        raise RegistryError("registry must define a first-class Skip action")
    if not any(item.kind == PrimitiveKind.ACTION and item.family == "abstain" for item in registry.primitives):
        raise RegistryError("registry must define a first-class Abstain action")


def validate_primitive(primitive: PrimitiveDefinition, policy: TreatmentDslPolicy | None = None) -> None:
    validate_identifier(primitive.primitive_id, "primitive_id")
    validate_identifier(primitive.family, "family")
    validate_version(primitive.exact_version)
    if not primitive.supported_sides or set(primitive.supported_sides) - {"long", "short", "none"}:
        raise RegistryError(f"invalid supported_sides for {primitive.exact_key}")
    names = [item.name for item in primitive.parameters]
    if len(names) != len(set(names)):
        raise RegistryError(f"duplicate parameter name in {primitive.exact_key}")
    for parameter in primitive.parameters:
        validate_identifier(parameter.name, "parameter_name")
        validate_identifier(parameter.units, "parameter_units")
        if policy and parameter.units not in policy.allowed_units:
            raise RegistryError(f"unit {parameter.units} not allowed by policy")
        if parameter.parameter_type == ParameterType.ENUM and not parameter.allowed_values:
            raise RegistryError(f"enum parameter {parameter.name} requires allowed_values")
        validate_parameter_value(parameter, parameter.default)
        if parameter.minimum is not None:
            validate_parameter_value(parameter, parameter.minimum, range_endpoint=True)
        if parameter.maximum is not None:
            validate_parameter_value(parameter, parameter.maximum, range_endpoint=True)
        if parameter.minimum is not None and parameter.maximum is not None:
            try:
                if Decimal(str(parameter.minimum)) > Decimal(str(parameter.maximum)):
                    raise RegistryError(f"minimum exceeds maximum for {parameter.name}")
            except InvalidOperation as exc:
                raise RegistryError(f"non-numeric range for {parameter.name}") from exc
        if policy:
            lowered = parameter.name.lower()
            if any(token in lowered for token in policy.prohibited_parameter_tokens):
                raise RegistryError(f"prohibited parameter token in {primitive.exact_key}:{parameter.name}")
    for capability in primitive.required_capabilities:
        validate_identifier(capability, "required_capability")


def validate_parameter_value(parameter, value, range_endpoint: bool = False):
    kind = parameter.parameter_type
    if value is None and not parameter.required and not range_endpoint:
        return None
    if kind == ParameterType.BOOLEAN:
        if not isinstance(value, bool):
            raise RegistryError(f"{parameter.name} expects boolean")
        return value
    if kind in (ParameterType.INTEGER, ParameterType.DURATION_MS):
        if isinstance(value, bool) or not isinstance(value, int):
            raise RegistryError(f"{parameter.name} expects integer")
        if kind == ParameterType.DURATION_MS and value < 0:
            raise RegistryError(f"{parameter.name} duration cannot be negative")
        return value
    if kind == ParameterType.DECIMAL:
        try:
            return Decimal(str(value))
        except InvalidOperation as exc:
            raise RegistryError(f"{parameter.name} expects decimal") from exc
    if kind in (ParameterType.STRING, ParameterType.ENUM):
        if not isinstance(value, str):
            raise RegistryError(f"{parameter.name} expects string")
        if kind == ParameterType.ENUM and value not in parameter.allowed_values:
            raise RegistryError(f"{parameter.name} enum value not allowed")
        return value
    raise RegistryError(f"unknown parameter type: {kind}")


def validate_policy(policy: TreatmentDslPolicy) -> None:
    validate_identifier(policy.policy_name, "policy_name")
    validate_version(policy.exact_version)
    integer_fields = (
        policy.maximum_programs,
        policy.maximum_components_per_program,
        policy.maximum_parameters_per_program,
        policy.maximum_constraints_per_program,
        policy.maximum_states_per_program,
        policy.maximum_transitions_per_program,
        policy.deterministic_partition_count,
    )
    if any(value < 1 for value in integer_fields):
        raise RegistryError("all V4-06 policy budgets must be positive")
    if not policy.allowed_units or not policy.allowed_evidence_roles:
        raise RegistryError("policy must declare units and Evidence Roles")
    if PrimitiveKind.ACTION in policy.required_component_kinds:
        raise RegistryError("action cannot be required for ordinary treatment programs")
    if len(policy.singleton_component_kinds) != len(set(policy.singleton_component_kinds)):
        raise RegistryError("duplicate singleton component kind")
    if any(not token.strip() for token in policy.prohibited_identifier_tokens + policy.prohibited_parameter_tokens):
        raise RegistryError("prohibited token lists cannot contain empty entries")


def validate_capability_profile(profile: CapabilityProfile) -> None:
    validate_identifier(profile.profile_name, "profile_name")
    validate_version(profile.exact_version)
    if profile.maximum_entry_legs < 1:
        raise RegistryError("maximum_entry_legs must be positive")
    for value in profile.capabilities:
        validate_identifier(value, "capability")
    if len(profile.capabilities) != len(set(profile.capabilities)):
        raise RegistryError("duplicate capability")
    if len(profile.order_types) != len(set(profile.order_types)):
        raise RegistryError("duplicate order type")
