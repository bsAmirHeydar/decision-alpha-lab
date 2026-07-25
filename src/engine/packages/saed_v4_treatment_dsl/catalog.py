from __future__ import annotations

from .enums import EvidenceRole, MonotonicDirection, ParameterType, PrimitiveKind
from .models import (
    CapabilityProfile,
    ParameterDefinition,
    PrimitiveDefinition,
    TreatmentDslAuthorityBoundary,
    TreatmentDslPolicy,
    TreatmentDslRegistry,
)


def p(name, kind, units, default, minimum=None, maximum=None, allowed=(), required=False, monotonic=MonotonicDirection.NONE, description=""):
    return ParameterDefinition(name, kind, units, default, minimum, maximum, tuple(allowed), required, True, monotonic, description)


def primitive(identifier, kind, family, parameters=(), capabilities=(), sides=("long", "short"), labels=(), path_dependent=False, description=""):
    return PrimitiveDefinition(identifier, "1.0.0", kind, family, tuple(parameters), tuple(capabilities), tuple(sides), tuple(labels), path_dependent, description)


def institutional_registry() -> TreatmentDslRegistry:
    primitives = (
        primitive("action.skip", PrimitiveKind.ACTION, "skip", sides=("none",), description="Do not create an executable path."),
        primitive("action.abstain", PrimitiveKind.ACTION, "abstain", sides=("none",), description="Withhold decision because support or certainty is insufficient."),
        primitive("payoff.asymmetric_r_multiple", PrimitiveKind.PAYOFF, "asymmetric", (
            p("minimum_reward_r", ParameterType.DECIMAL, "r_multiple", "2.0", "0.1", "20", monotonic=MonotonicDirection.INCREASING),
            p("maximum_holding_ms", ParameterType.DURATION_MS, "milliseconds", 1800000, 1000, 86400000),
        ), labels=(("payoff_profile", "P3"),)),
        primitive("direction.context_declared", PrimitiveKind.DIRECTION, "context_declared", (
            p("direction_source", ParameterType.ENUM, "enum", "context", allowed=("context", "manual")),
        )),
        primitive("entry.market", PrimitiveKind.ENTRY, "market", (
            p("maximum_quote_age_ms", ParameterType.DURATION_MS, "milliseconds", 1000, 0, 60000),
        ), capabilities=("order.market",), labels=(("entry_mechanism", "market"),)),
        primitive("entry.breakout_stop", PrimitiveKind.ENTRY, "breakout", (
            p("reference_feature", ParameterType.STRING, "feature_ref", "structure_view:breakout_level", required=True),
            p("buffer_points", ParameterType.DECIMAL, "points", "2.0", "0", "10000"),
            p("ttl_ms", ParameterType.DURATION_MS, "milliseconds", 300000, 1, 86400000),
        ), capabilities=("order.stop", "order.expiration"), labels=(("entry_mechanism", "breakout"),)),
        primitive("entry.passive_limit", PrimitiveKind.ENTRY, "passive", (
            p("offset_points", ParameterType.DECIMAL, "points", "5.0", "0", "100000"),
            p("ttl_ms", ParameterType.DURATION_MS, "milliseconds", 300000, 1, 86400000),
        ), capabilities=("order.limit", "order.expiration"), labels=(("entry_mechanism", "passive"),)),
        primitive("trigger.context_feature", PrimitiveKind.TRIGGER, "feature_predicate", (
            p("feature_ref", ParameterType.STRING, "feature_ref", "structure_view:breakout_state", required=True),
            p("operator", ParameterType.ENUM, "enum", "eq", allowed=("eq", "ne", "lt", "le", "gt", "ge", "in", "exists")),
            p("expected_value", ParameterType.STRING, "scalar", "confirmed"),
        )),
        primitive("stop.context_invalidation", PrimitiveKind.STOP, "context_invalidation", (
            p("reference_feature", ParameterType.STRING, "feature_ref", "structure_view:invalidation_level", required=True),
            p("buffer_points", ParameterType.DECIMAL, "points", "1.0", "0", "10000"),
        ), capabilities=("protection.server_stop",)),
        primitive("stop.fixed_distance", PrimitiveKind.STOP, "fixed_distance", (
            p("distance_points", ParameterType.DECIMAL, "points", "100", "1", "1000000", monotonic=MonotonicDirection.INCREASING),
        ), capabilities=("protection.server_stop",)),
        primitive("target.fixed_r_multiple", PrimitiveKind.TARGET, "fixed_r", (
            p("reward_r", ParameterType.DECIMAL, "r_multiple", "3.0", "0.1", "20", monotonic=MonotonicDirection.INCREASING),
        ), capabilities=("exit.take_profit",)),
        primitive("exit.time_stop", PrimitiveKind.EXIT, "time_stop", (
            p("maximum_holding_ms", ParameterType.DURATION_MS, "milliseconds", 1800000, 1000, 86400000),
        ), capabilities=("exit.market",), path_dependent=True),
        primitive("trail.none", PrimitiveKind.TRAIL, "none"),
        primitive("trail.break_even", PrimitiveKind.TRAIL, "break_even", (
            p("activation_r", ParameterType.DECIMAL, "r_multiple", "1.0", "0.1", "10"),
            p("offset_points", ParameterType.DECIMAL, "points", "0", "0", "1000"),
        ), capabilities=("protection.modify_stop",), path_dependent=True),
        primitive("management.none", PrimitiveKind.MANAGEMENT, "none"),
        primitive("management.partial_scale", PrimitiveKind.MANAGEMENT, "partial_scale", (
            p("activation_r", ParameterType.DECIMAL, "r_multiple", "1.5", "0.1", "20"),
            p("quantity_fraction", ParameterType.DECIMAL, "fraction", "0.5", "0.01", "0.99"),
        ), capabilities=("exit.partial",), path_dependent=True),
        primitive("time.session_window", PrimitiveKind.TIME, "session_window", (
            p("session_id", ParameterType.ENUM, "enum", "new_york", allowed=("asia", "london", "new_york", "overlap")),
            p("start_offset_ms", ParameterType.DURATION_MS, "milliseconds", 0, 0, 86400000),
            p("duration_ms", ParameterType.DURATION_MS, "milliseconds", 7200000, 1000, 86400000),
        )),
        primitive("cost.maximum_spread", PrimitiveKind.COST, "spread_guard", (
            p("maximum_spread_points", ParameterType.DECIMAL, "points", "3.0", "0", "10000"),
        )),
        primitive("capability.mt5_hedging", PrimitiveKind.CAPABILITY, "mt5_hedging", (
            p("required_profile", ParameterType.ENUM, "enum", "mt5_hedging_reference", allowed=("mt5_hedging_reference",)),
        ), capabilities=("platform.mt5", "account.hedging")),
    )
    return TreatmentDslRegistry(
        "institutional.treatment_dsl",
        "1.0.0",
        primitives,
        TreatmentDslAuthorityBoundary(),
        (
            "The registry is a finite declaration surface, not a generator of arbitrary actions.",
            "Capital sizing, portfolio allocation, runtime activation and broker orders are outside V4-06 authority.",
        ),
    )


def institutional_policy() -> TreatmentDslPolicy:
    return TreatmentDslPolicy(
        policy_name="institutional.treatment_dsl.policy",
        exact_version="1.0.0",
        maximum_programs=4096,
        maximum_components_per_program=16,
        maximum_parameters_per_program=128,
        maximum_constraints_per_program=64,
        maximum_states_per_program=32,
        maximum_transitions_per_program=64,
        allowed_units=("unitless", "enum", "boolean", "integer", "decimal", "milliseconds", "points", "r_multiple", "fraction", "feature_ref", "scalar"),
        allowed_evidence_roles=(EvidenceRole.DEVELOPMENT, EvidenceRole.CALIBRATION, EvidenceRole.SELECTION_VALIDATION, EvidenceRole.LOCKED_FINAL, EvidenceRole.PROSPECTIVE, EvidenceRole.SHADOW, EvidenceRole.EXTERNAL_STATIC, EvidenceRole.EXTERNAL_ACTUAL),
        required_component_kinds=(PrimitiveKind.PAYOFF, PrimitiveKind.DIRECTION, PrimitiveKind.ENTRY, PrimitiveKind.STOP, PrimitiveKind.TARGET, PrimitiveKind.TIME, PrimitiveKind.COST, PrimitiveKind.CAPABILITY),
        singleton_component_kinds=tuple(PrimitiveKind),
        prohibited_identifier_tokens=("future", "outcome", "label", "realized", "forward_return"),
        prohibited_parameter_tokens=("lot", "volume", "leverage", "capital", "allocation", "position_size", "risk_cash", "equity_fraction"),
        require_skip=True,
        require_abstain=True,
        require_exact_hypergraph_handoff=True,
        deterministic_partition_count=8,
    )


def institutional_capability_profile() -> CapabilityProfile:
    return CapabilityProfile(
        profile_name="mt5.hedging.reference",
        exact_version="1.0.0",
        capabilities=(
            "platform.mt5", "account.hedging", "order.market", "order.limit", "order.stop", "order.expiration",
            "protection.server_stop", "protection.modify_stop", "exit.take_profit", "exit.market", "exit.partial",
        ),
        order_types=("market", "limit", "stop"),
        time_in_force=("gtc", "day", "specified"),
        maximum_entry_legs=8,
        supports_server_stop=True,
        supports_partial_exit=True,
        supports_trailing=True,
        supports_expiration=True,
        diagnostic_only=True,
    )
