"""RTHP ContextPackage adapter for the existing UCEE/SAED engine.

This file maps already-canonical RTHP occurrences into the engine's immutable
ContextPackage interface. It does not detect RTHP, mutate semantics, create
labels, generate treatments, train models, submit orders, or change engine code.
"""
from __future__ import annotations

from typing import Any, Mapping

from strategy_factory_contracts_v3 import KnownTimeChain, UtcInstant, canonical_sha256
from strategy_factory_contexts_v3 import (
    AvailabilityMode,
    ClusterKind,
    ClusterRule,
    ComponentReference,
    ContextLifecycleState,
    ContextObservation,
    ContextPackage,
    ContextPackageManifest,
    ContextUpdateScope,
    FeatureDataType,
    FeatureDescriptor,
    FeatureFrame,
    FeatureValue,
    ManualPolicyKind,
    ManualPolicyReference,
    MissingnessPolicy,
    RepresentationKind,
    RepresentationViewDescriptor,
    RequirementStrength,
    SourceRequirement,
    SourceRequirementKind,
    StalenessPolicy,
    TaskKind,
    TaskReference,
)

from .constants import (
    ACTIVE_CYCLE_TYPES,
    ADAPTER_ID,
    ADAPTER_VERSION,
    CONTEXT_ID,
    CONTEXT_VERSION,
    CYCLE_COMPLETENESS,
    DATA_STATUSES,
    DOCTRINE_ID,
    DOCTRINE_VERSION,
    FAMILIES,
    HISTORY_SUFFICIENCIES,
    HUNTER_ROLES,
    LEVEL_SIDES,
    OPTIONAL_GEOMETRY_FIELDS,
    OWNER_ID,
    PACKAGE_ID,
    PACKAGE_VERSION,
    POLARITIES,
    REFERENCE_CYCLE_TYPES,
    REFERENCE_STATES_AT_CUT,
    REQUIRED_SOURCE_FIELDS,
    SEQUENTIALITIES,
    TASKS,
)

_MODES = AvailabilityMode.RESEARCH | AvailabilityMode.TESTER
_VIEW_IDS = (
    "rthp.tabular.v1",
    "rthp.sparse_event.v1",
    "rthp.sequence.v1",
    "rthp.intermarket.v1",
    "rthp.graph.v1",
)


def _instant(value: int, clock_id: str) -> UtcInstant:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{clock_id} must be an integer epoch millisecond")
    return UtcInstant(value, clock_id)


def _bool(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field} must be boolean")
    return value


def _int(value: Any, field: str, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError(f"{field} must be an integer >= {minimum}")
    return value


def _float(value: Any, field: str, minimum: float | None = None, maximum: float | None = None) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{field} must be numeric")
    out = float(value)
    if minimum is not None and out < minimum:
        raise ValueError(f"{field} must be >= {minimum}")
    if maximum is not None and out > maximum:
        raise ValueError(f"{field} must be <= {maximum}")
    return out


def _category(value: Any, field: str, domain: tuple[str, ...]) -> str:
    if not isinstance(value, str) or value not in domain:
        raise ValueError(f"{field} must be one of {domain}")
    return value


def validate_source_record(source: Mapping[str, Any], *, strict: bool = True) -> tuple[str, ...]:
    """Return deterministic validation findings; never alter the source record."""
    findings: list[str] = []
    missing = [field for field in REQUIRED_SOURCE_FIELDS if field not in source]
    if missing:
        findings.append("missing_required_fields:" + ",".join(sorted(missing)))
        return tuple(findings)

    def capture(code: str, fn) -> None:
        try:
            fn()
        except Exception as exc:  # deterministic preflight evidence, not silent coercion
            findings.append(f"{code}:{type(exc).__name__}:{exc}")

    capture("context_id", lambda: (_ for _ in ()).throw(ValueError("context_id mismatch")) if source["context_id"] != CONTEXT_ID else None)
    capture("context_version", lambda: (_ for _ in ()).throw(ValueError("context_version mismatch")) if source["context_version"] != CONTEXT_VERSION else None)
    capture("confirmed_context_event", lambda: _bool(source["confirmed_context_event"], "confirmed_context_event"))
    if source.get("confirmed_context_event") is not True:
        findings.append("not_confirmed_context_event")
    capture("family", lambda: _category(source["family"], "family", FAMILIES))
    capture("level_side", lambda: _category(source["level_side"], "level_side", LEVEL_SIDES))
    capture("polarity", lambda: _category(source["polarity"], "polarity", POLARITIES))
    capture("sequentiality", lambda: _category(source["sequentiality"], "sequentiality", SEQUENTIALITIES))
    capture("data_status", lambda: _category(source["data_status"], "data_status", DATA_STATUSES))
    capture("history_sufficiency", lambda: _category(source["history_sufficiency"], "history_sufficiency", HISTORY_SUFFICIENCIES))
    capture("cycle_completeness", lambda: _category(source["cycle_completeness"], "cycle_completeness", CYCLE_COMPLETENESS))
    capture("active_cycle_type", lambda: _category(source["active_cycle_type"], "active_cycle_type", ACTIVE_CYCLE_TYPES))
    capture("reference_cycle_type", lambda: _category(source["reference_cycle_type"], "reference_cycle_type", REFERENCE_CYCLE_TYPES))
    capture("reference_state_at_cut", lambda: _category(source["reference_state_at_cut"], "reference_state_at_cut", REFERENCE_STATES_AT_CUT))

    for field in (
        "event_time_ms", "known_time_ms", "confirmation_time_ms", "observation_cut_ms", "decision_time_ms",
        "confirmation_close_time_ms", "available_reference_count", "required_reference_count", "reference_age_cycles",
        "reference_to_active_gap_cycles", "minute_of_session", "minute_of_day_ny", "day_of_week_ny",
        "simultaneous_family_count", "primary_freshness_age_ms", "secondary_freshness_age_ms",
    ):
        minimum = 1 if field == "simultaneous_family_count" else 0
        capture(field, lambda field=field, minimum=minimum: _int(source[field], field, minimum))

    capture("active_cycle_progress", lambda: _float(source["active_cycle_progress"], "active_cycle_progress", 0.0, 1.0))
    capture("is_same_day_reference", lambda: _bool(source["is_same_day_reference"], "is_same_day_reference"))
    for field in OPTIONAL_GEOMETRY_FIELDS:
        if source.get(field) is not None:
            capture(field, lambda field=field: _float(source[field], field))

    if not findings:
        ordered = (
            int(source["event_time_ms"]),
            int(source["known_time_ms"]),
            int(source["confirmation_time_ms"]),
            int(source["observation_cut_ms"]),
            int(source["decision_time_ms"]),
        )
        if list(ordered) != sorted(ordered):
            findings.append("causal_time_order_invalid")
        if int(source["confirmation_close_time_ms"]) > int(source["observation_cut_ms"]):
            findings.append("confirmation_close_after_observation_cut")
        if source["hunter_symbol"] not in (source["primary_symbol"], source["secondary_symbol"]):
            findings.append("hunter_not_in_symbol_pair")
        if source["protected_symbol"] not in (source["primary_symbol"], source["secondary_symbol"]):
            findings.append("protected_not_in_symbol_pair")
        if source["hunter_symbol"] == source["protected_symbol"]:
            findings.append("hunter_equals_protected")
        expected_polarity = "BEARISH_DIVERGENCE" if source["level_side"] == "HIGH" else "BULLISH_DIVERGENCE"
        if source["polarity"] != expected_polarity:
            findings.append("polarity_level_side_mismatch")
        required = int(source["required_reference_count"])
        available = int(source["available_reference_count"])
        expected_sufficiency = "FULL" if required == 0 or available >= required else "PARTIAL"
        if source["history_sufficiency"] != expected_sufficiency:
            findings.append("history_sufficiency_mismatch")
        if source["data_status"] == "VALID" and source["history_sufficiency"] != "FULL":
            findings.append("valid_data_requires_full_history")
        if source["data_status"] == "PARTIAL_HISTORY" and source["history_sufficiency"] != "PARTIAL":
            findings.append("partial_history_status_mismatch")
        if source["reference_age_cycles"] > max(available, 0) and available > 0:
            findings.append("reference_age_exceeds_available_history")
        if source.get("auxiliary") != build_auxiliary_payload(source):
            findings.append("auxiliary_projection_mismatch")
        if source.get("auxiliary") != build_auxiliary_payload(source):
            findings.append("auxiliary_projection_mismatch")
        if strict and any(str(key).startswith("future_") for key in source):
            findings.append("future_prefixed_field_forbidden")
    return tuple(sorted(set(findings)))


def _feature_descriptors() -> tuple[FeatureDescriptor, ...]:
    required = MissingnessPolicy.REJECT
    optional = MissingnessPolicy.EXPLICIT_MISSING
    reject_stale = StalenessPolicy.REJECT
    allow_age = StalenessPolicy.ALLOW_WITH_AGE
    items = (
        FeatureDescriptor("rthp.active_cycle_progress", "1.0.0", OWNER_ID, FeatureDataType.FLOAT64, "fraction", (), required, reject_stale, 0, (), _MODES, True, (), "Progress of the active cycle at the confirmation cut."),
        FeatureDescriptor("rthp.active_cycle_type", "1.0.0", OWNER_ID, FeatureDataType.CATEGORY, "cycle_type", (), required, reject_stale, 0, (), _MODES, True, ACTIVE_CYCLE_TYPES, "Registered active-cycle type."),
        FeatureDescriptor("rthp.active_range_ticks", "1.0.0", OWNER_ID, FeatureDataType.FLOAT64, "ticks", (), optional, allow_age, 0, (), _MODES, True, (), "Optional active-cycle range normalized by local tick size."),
        FeatureDescriptor("rthp.available_reference_count", "1.0.0", OWNER_ID, FeatureDataType.INT64, "cycles", (), required, reject_stale, 0, (), _MODES, True, (), "Available completed reference cycles at the cut."),
        FeatureDescriptor("rthp.cycle_completeness", "1.0.0", OWNER_ID, FeatureDataType.CATEGORY, "state", (), required, reject_stale, 0, (), _MODES, True, CYCLE_COMPLETENESS, "Completeness class of the active cycle."),
        FeatureDescriptor("rthp.data_status", "1.0.0", OWNER_ID, FeatureDataType.CATEGORY, "state", (), required, reject_stale, 0, (), _MODES, True, DATA_STATUSES, "Confirmed-event data sufficiency status."),
        FeatureDescriptor("rthp.day_of_week_ny", "1.0.0", OWNER_ID, FeatureDataType.INT64, "iso_weekday", (), required, reject_stale, 0, (), _MODES, True, (), "ISO weekday in America/New_York at the cut."),
        FeatureDescriptor("rthp.family", "1.0.0", OWNER_ID, FeatureDataType.CATEGORY, "family", (), required, reject_stale, 0, (), _MODES, True, FAMILIES, "Registered RTHP relationship family."),
        FeatureDescriptor("rthp.history_coverage_ratio", "1.0.0", OWNER_ID, FeatureDataType.FLOAT64, "fraction", (), required, reject_stale, 0, (), _MODES, True, (), "Available divided by required reference count; one when lookback is zero."),
        FeatureDescriptor("rthp.history_sufficiency", "1.0.0", OWNER_ID, FeatureDataType.CATEGORY, "state", (), required, reject_stale, 0, (), _MODES, True, HISTORY_SUFFICIENCIES, "Full or partial reference history at confirmation."),
        FeatureDescriptor("rthp.hunter_role", "1.0.0", OWNER_ID, FeatureDataType.CATEGORY, "pair_role", (), required, reject_stale, 0, (), _MODES, True, HUNTER_ROLES, "Whether the hunter is the primary or secondary pair member; raw symbol identity is excluded."),
        FeatureDescriptor("rthp.hunter_touch_overrun_ticks", "1.0.0", OWNER_ID, FeatureDataType.FLOAT64, "ticks", (), optional, allow_age, 0, (), _MODES, True, (), "Optional hunter overrun beyond its local reference level."),
        FeatureDescriptor("rthp.is_intraday_family", "1.0.0", OWNER_ID, FeatureDataType.BOOL, "boolean", (), required, reject_stale, 0, (), _MODES, True, (), "True for intraday families other than WW and DD."),
        FeatureDescriptor("rthp.is_m15_cycle_group", "1.0.0", OWNER_ID, FeatureDataType.BOOL, "boolean", (), required, reject_stale, 0, (), _MODES, True, (), "True only for M15_CYCLE_GROUP."),
        FeatureDescriptor("rthp.is_same_day_reference", "1.0.0", OWNER_ID, FeatureDataType.BOOL, "boolean", (), required, reject_stale, 0, (), _MODES, True, (), "Source-declared same-day relation; not inferred from family alone."),
        FeatureDescriptor("rthp.is_sequential", "1.0.0", OWNER_ID, FeatureDataType.BOOL, "boolean", (), required, reject_stale, 0, (), _MODES, True, (), "True only when sequentiality is SEQUENTIAL."),
        FeatureDescriptor("rthp.level_side", "1.0.0", OWNER_ID, FeatureDataType.CATEGORY, "side", (), required, reject_stale, 0, (), _MODES, True, LEVEL_SIDES, "High-side or low-side divergence."),
        FeatureDescriptor("rthp.max_freshness_age_ms", "1.0.0", OWNER_ID, FeatureDataType.INT64, "milliseconds", (), required, reject_stale, 0, (), _MODES, True, (), "Maximum source freshness age across pair members at the confirmation cut."),
        FeatureDescriptor("rthp.minute_of_day_ny", "1.0.0", OWNER_ID, FeatureDataType.INT64, "minute", (), required, reject_stale, 0, (), _MODES, True, (), "Minute of New York day at confirmation."),
        FeatureDescriptor("rthp.minute_of_session", "1.0.0", OWNER_ID, FeatureDataType.INT64, "minute", (), required, reject_stale, 0, (), _MODES, True, (), "Minute offset inside the active registered cycle/session."),
        FeatureDescriptor("rthp.polarity", "1.0.0", OWNER_ID, FeatureDataType.CATEGORY, "polarity", (), required, reject_stale, 0, (), _MODES, True, POLARITIES, "Intrinsic RTHP polarity; not an entry or order instruction."),
        FeatureDescriptor("rthp.protected_distance_to_level_ticks", "1.0.0", OWNER_ID, FeatureDataType.FLOAT64, "ticks", (), optional, allow_age, 0, (), _MODES, True, (), "Optional protected-symbol distance to its local level at confirmation."),
        FeatureDescriptor("rthp.reference_age_cycles", "1.0.0", OWNER_ID, FeatureDataType.INT64, "cycles", (), required, reject_stale, 0, (), _MODES, True, (), "Age of the selected reference in completed eligible cycles."),
        FeatureDescriptor("rthp.reference_cycle_type", "1.0.0", OWNER_ID, FeatureDataType.CATEGORY, "cycle_type", (), required, reject_stale, 0, (), _MODES, True, REFERENCE_CYCLE_TYPES, "Registered reference-cycle type."),
        FeatureDescriptor("rthp.reference_range_ticks", "1.0.0", OWNER_ID, FeatureDataType.FLOAT64, "ticks", (), optional, allow_age, 0, (), _MODES, True, (), "Optional reference-cycle range normalized by local tick size."),
        FeatureDescriptor("rthp.reference_state_at_cut", "1.0.0", OWNER_ID, FeatureDataType.CATEGORY, "state", (), required, reject_stale, 0, (), _MODES, True, REFERENCE_STATES_AT_CUT, "Reference state frozen at the training observation cut."),
        FeatureDescriptor("rthp.reference_to_active_gap_cycles", "1.0.0", OWNER_ID, FeatureDataType.INT64, "cycles", (), required, reject_stale, 0, (), _MODES, True, (), "Cycle distance from reference to active cycle."),
        FeatureDescriptor("rthp.required_reference_count", "1.0.0", OWNER_ID, FeatureDataType.INT64, "cycles", (), required, reject_stale, 0, (), _MODES, True, (), "Configured reference lookback requirement."),
        FeatureDescriptor("rthp.sequentiality", "1.0.0", OWNER_ID, FeatureDataType.CATEGORY, "state", (), required, reject_stale, 0, (), _MODES, True, SEQUENTIALITIES, "Sequential, non-sequential, or not-applicable cycle relation."),
        FeatureDescriptor("rthp.simultaneous_family_count", "1.0.0", OWNER_ID, FeatureDataType.INT64, "count", (), required, reject_stale, 0, (), _MODES, True, (), "Number of separate registered family events at the same confirmation cut."),
        FeatureDescriptor("rthp.touch_to_confirmation_ms", "1.0.0", OWNER_ID, FeatureDataType.INT64, "milliseconds", (), required, reject_stale, 0, (), _MODES, True, (), "Elapsed time from first touch to synchronized confirmation."),
    )
    return tuple(sorted(items, key=lambda item: item.feature_id))


def _view_descriptors(features: tuple[FeatureDescriptor, ...]) -> tuple[RepresentationViewDescriptor, ...]:
    all_ids = tuple(item.feature_id for item in features)
    sequence_ids = (
        "rthp.active_cycle_progress", "rthp.available_reference_count", "rthp.history_coverage_ratio",
        "rthp.max_freshness_age_ms", "rthp.minute_of_session", "rthp.reference_age_cycles",
        "rthp.reference_to_active_gap_cycles", "rthp.simultaneous_family_count", "rthp.touch_to_confirmation_ms",
    )
    intermarket_ids = (
        "rthp.hunter_touch_overrun_ticks", "rthp.protected_distance_to_level_ticks",
        "rthp.reference_range_ticks", "rthp.active_range_ticks",
    )
    sparse_ids = (
        "rthp.family", "rthp.level_side", "rthp.polarity", "rthp.hunter_role",
        "rthp.reference_state_at_cut", "rthp.sequentiality", "rthp.data_status",
    )
    return (
        RepresentationViewDescriptor("rthp.tabular.v1", "1.0.0", OWNER_ID, RepresentationKind.TABULAR, all_ids, (len(all_ids),), _MODES, True, {"ordering": "lexicographic", "raw_symbol_identity": "excluded"}),
        RepresentationViewDescriptor("rthp.sparse_event.v1", "1.0.0", OWNER_ID, RepresentationKind.SPARSE_EVENT, sparse_ids, (1,), _MODES, False, {"event_schema": "RTHP_CANONICAL_OCCURRENCE"}),
        RepresentationViewDescriptor("rthp.sequence.v1", "1.0.0", OWNER_ID, RepresentationKind.SEQUENCE, sequence_ids, (len(sequence_ids), 16), _MODES, False, {"window": 16, "ordering": "known_time_then_event_id"}),
        RepresentationViewDescriptor("rthp.intermarket.v1", "1.0.0", OWNER_ID, RepresentationKind.INTERMARKET, intermarket_ids, (2, 4), _MODES, False, {"rows": ["hunter", "protected"], "normalization": "symbol_local_ticks"}),
        RepresentationViewDescriptor("rthp.graph.v1", "1.0.0", OWNER_ID, RepresentationKind.GRAPH, sparse_ids, (1,), _MODES, False, {"node_types": ["symbol_pair", "symbol_role", "cycle", "reference", "occurrence", "family"], "identity": "context_occurrence_id"}),
    )


def _cluster_rules() -> tuple[ClusterRule, ...]:
    return (
        ClusterRule("rthp.opportunity.v1", "1.0.0", OWNER_ID, ClusterKind.OPPORTUNITY, ("pair_id", "family", "reference_cycle_id", "active_cycle_id", "level_side", "confirmation_close_time_ms"), {"sibling_lock": True}),
        ClusterRule("rthp.reference.v1", "1.0.0", OWNER_ID, ClusterKind.PARENT_CHILD, ("pair_id", "family", "reference_cycle_id", "level_side"), {"shared_reference": True}),
        ClusterRule("rthp.session_day.v1", "1.0.0", OWNER_ID, ClusterKind.SYMBOL_SESSION_DAY, ("pair_id", "trading_day_ny"), {"timezone": "America/New_York"}),
        ClusterRule("rthp.overlapping_path.v1", "1.0.0", OWNER_ID, ClusterKind.OVERLAPPING_PATH, ("pair_id", "confirmation_close_time_ms", "label_horizon_group"), {"purge_overlap": True}),
    )


def _task_references() -> tuple[TaskReference, ...]:
    mapping = {"binary": TaskKind.BINARY, "regression": TaskKind.REGRESSION, "survival": TaskKind.SURVIVAL, "ranking": TaskKind.RANKING, "quantile": TaskKind.QUANTILE}
    allowed = ("rthp.tabular.v1", "rthp.sparse_event.v1", "rthp.sequence.v1", "rthp.intermarket.v1", "rthp.graph.v1")
    return tuple(TaskReference(task_id, version, mapping[kind], label_id, allowed) for task_id, version, kind, label_id in TASKS)


class RTHPContextPackage(ContextPackage):
    """Immutable adapter over ACL-03 canonical RTHP occurrence records."""

    def __init__(self) -> None:
        self._features = _feature_descriptors()
        self._views = _view_descriptors(self._features)
        self._clusters = _cluster_rules()
        feature_hash = canonical_sha256([item.material() for item in self._features])
        self._manifest = ContextPackageManifest(
            package_id=PACKAGE_ID,
            version=PACKAGE_VERSION,
            owner_id=OWNER_ID,
            doctrine_id=DOCTRINE_ID,
            doctrine_version=DOCTRINE_VERSION,
            anatomy_adapter_id=ADAPTER_ID,
            anatomy_adapter_version=ADAPTER_VERSION,
            update_scope=ContextUpdateScope.NEW_BAR | ContextUpdateScope.REPLAY | ContextUpdateScope.HISTORY_REBUILD,
            runtime_modes=_MODES,
            source_requirements=(
                SourceRequirement(
                    "rthp_canonical_occurrence",
                    SourceRequirementKind.ANATOMY_EVENT,
                    RequirementStrength.REQUIRED,
                    ("PRIMARY", "SECONDARY"),
                    900,
                    1,
                    0,
                    "rthp_pair_m15_confirmation",
                    "Canonical ACL-03 RTHP confirmed occurrence with equal synchronized M15 confirmation identity.",
                ),
                SourceRequirement(
                    "rthp_reference_state",
                    SourceRequirementKind.EXTERNAL_LEDGER,
                    RequirementStrength.REQUIRED,
                    ("PRIMARY", "SECONDARY"),
                    0,
                    1,
                    0,
                    "rthp_reference_lineage",
                    "Append-only reference-state lineage used for factual exhaustion labels after maturity.",
                ),
            ),
            feature_packs=(ComponentReference("rthp.ai_input.core_features.v1", "1.0.0", feature_hash, True),),
            representation_views=tuple(ComponentReference(item.view_id, item.version, item.descriptor_hash, True) for item in self._views),
            cluster_rules=tuple(ComponentReference(item.rule_id, item.version, item.rule_hash, True) for item in self._clusters),
            manual_policies=(ManualPolicyReference("rthp.context_observation_only", "1.0.0", ManualPolicyKind.LABEL_ONLY, ("rthp.family", "rthp.level_side", "rthp.polarity")),),
            tasks=_task_references(),
            description="Context-only RTHP package exposing canonical, known-time-safe occurrence features to the existing AI engine without changing central process or authority.",
            metadata={
                "canonical_context_id": CONTEXT_ID,
                "canonical_context_version": CONTEXT_VERSION,
                "acl03_state": "CONTEXT_COMPILED",
                "entry_treatment_execution": "OUT_OF_SCOPE",
                "real_data_binding": "EXTERNAL_ARTIFACT_REQUIRED",
            },
        )

    @property
    def manifest(self) -> ContextPackageManifest:
        return self._manifest

    def feature_descriptors(self) -> tuple[FeatureDescriptor, ...]:
        return self._features

    def view_descriptors(self) -> tuple[RepresentationViewDescriptor, ...]:
        return self._views

    def cluster_rules(self) -> tuple[ClusterRule, ...]:
        return self._clusters

    def observe(self, source_record: Mapping[str, Any]) -> tuple[ContextObservation, ...]:
        if validate_source_record(source_record):
            return ()
        chain = KnownTimeChain(
            _instant(int(source_record["event_time_ms"]), "rthp.event_time"),
            _instant(int(source_record["known_time_ms"]), "rthp.known_time"),
            _instant(int(source_record["confirmation_time_ms"]), "rthp.confirmation_time"),
            _instant(int(source_record["observation_cut_ms"]), "rthp.observation_cut"),
            _instant(int(source_record["decision_time_ms"]), "rthp.decision_time"),
        )
        payload_keys = (
            "event_id", "family", "pair_id", "cycle_definition_version", "active_cycle_id", "reference_cycle_id",
            "active_cycle_type", "reference_cycle_type", "level_side", "polarity", "primary_symbol", "secondary_symbol",
            "hunter_symbol", "protected_symbol", "confirmation_close_time_ms", "data_status", "history_sufficiency",
            "available_reference_count", "required_reference_count", "reference_age_cycles", "reference_to_active_gap_cycles",
            "sequentiality", "cycle_completeness", "is_same_day_reference", "minute_of_session", "minute_of_day_ny",
            "day_of_week_ny", "active_cycle_progress", "simultaneous_family_count", "primary_freshness_age_ms",
            "secondary_freshness_age_ms", "reference_state_at_cut", "trading_day_ny", "source_revision",
            "source_content_hash", *OPTIONAL_GEOMETRY_FIELDS,
        )
        payload = {key: source_record.get(key) for key in payload_keys}
        source_ids = tuple(sorted(set((str(source_record["event_id"]), *tuple(str(x) for x in source_record.get("source_event_ids", ()))))))
        return (
            ContextObservation(
                self.manifest.package_id,
                self.manifest.version,
                source_ids,
                (str(source_record["primary_symbol"]), str(source_record["secondary_symbol"])),
                (900,),
                ContextLifecycleState.CONFIRMED,
                chain,
                payload,
                str(source_record.get("parent_observation_id", "none")),
                str(source_record.get("supersedes_observation_id", "none")),
            ),
        )

    def build_feature_frame(self, observation: ContextObservation, source_record: Mapping[str, Any]) -> FeatureFrame:
        findings = validate_source_record(source_record)
        if findings:
            raise ValueError("invalid RTHP source record: " + ";".join(findings))
        available = int(source_record["available_reference_count"])
        required = int(source_record["required_reference_count"])
        coverage = 1.0 if required == 0 else min(1.0, available / required)
        raw: dict[str, Any] = {
            "rthp.active_cycle_progress": float(source_record["active_cycle_progress"]),
            "rthp.active_cycle_type": str(source_record["active_cycle_type"]),
            "rthp.active_range_ticks": source_record.get("active_range_ticks"),
            "rthp.available_reference_count": available,
            "rthp.cycle_completeness": str(source_record["cycle_completeness"]),
            "rthp.data_status": str(source_record["data_status"]),
            "rthp.day_of_week_ny": int(source_record["day_of_week_ny"]),
            "rthp.family": str(source_record["family"]),
            "rthp.history_coverage_ratio": coverage,
            "rthp.history_sufficiency": str(source_record["history_sufficiency"]),
            "rthp.hunter_role": "PRIMARY" if source_record["hunter_symbol"] == source_record["primary_symbol"] else "SECONDARY",
            "rthp.hunter_touch_overrun_ticks": source_record.get("hunter_touch_overrun_ticks"),
            "rthp.is_intraday_family": source_record["family"] not in ("WW", "DD"),
            "rthp.is_m15_cycle_group": source_record["family"] == "M15_CYCLE_GROUP",
            "rthp.is_same_day_reference": bool(source_record["is_same_day_reference"]),
            "rthp.is_sequential": source_record["sequentiality"] == "SEQUENTIAL",
            "rthp.level_side": str(source_record["level_side"]),
            "rthp.max_freshness_age_ms": max(int(source_record["primary_freshness_age_ms"]), int(source_record["secondary_freshness_age_ms"])),
            "rthp.minute_of_day_ny": int(source_record["minute_of_day_ny"]),
            "rthp.minute_of_session": int(source_record["minute_of_session"]),
            "rthp.polarity": str(source_record["polarity"]),
            "rthp.protected_distance_to_level_ticks": source_record.get("protected_distance_to_level_ticks"),
            "rthp.reference_age_cycles": int(source_record["reference_age_cycles"]),
            "rthp.reference_cycle_type": str(source_record["reference_cycle_type"]),
            "rthp.reference_range_ticks": source_record.get("reference_range_ticks"),
            "rthp.reference_state_at_cut": str(source_record["reference_state_at_cut"]),
            "rthp.reference_to_active_gap_cycles": int(source_record["reference_to_active_gap_cycles"]),
            "rthp.required_reference_count": required,
            "rthp.sequentiality": str(source_record["sequentiality"]),
            "rthp.simultaneous_family_count": int(source_record["simultaneous_family_count"]),
            "rthp.touch_to_confirmation_ms": int(source_record["confirmation_close_time_ms"]) - int(source_record["event_time_ms"]),
        }
        values: list[FeatureValue] = []
        for descriptor in self._features:
            value = raw[descriptor.feature_id]
            missing = value is None
            values.append(
                FeatureValue(
                    descriptor.feature_id,
                    descriptor.version,
                    None if missing else value,
                    observation.time_chain.observation_cut,
                    observation.time_chain.confirmation_time,
                    missing,
                    "not_provided_by_canonical_event" if missing else "none",
                )
            )
        return FeatureFrame(
            observation.observation_id,
            self.manifest.package_id,
            self.manifest.version,
            observation.time_chain.observation_cut,
            self._features,
            tuple(values),
        )


def build_auxiliary_payload(source_record: Mapping[str, Any]) -> Mapping[str, Any]:
    """Build optional view inputs without changing central view compilers."""
    event = {
        "event_id": source_record["event_id"],
        "family": source_record["family"],
        "level_side": source_record["level_side"],
        "polarity": source_record["polarity"],
        "reference_cycle_id": source_record["reference_cycle_id"],
        "active_cycle_id": source_record["active_cycle_id"],
        "known_time_ms": source_record["known_time_ms"],
    }
    graph = {
        "nodes": [
            f"pair:{source_record['pair_id']}",
            "role:hunter", "role:protected",
            f"reference:{source_record['reference_cycle_id']}",
            f"active:{source_record['active_cycle_id']}",
            f"family:{source_record['family']}",
            f"event:{source_record['event_id']}",
        ],
        "edges": [
            [f"pair:{source_record['pair_id']}", "role:hunter", "HAS_ROLE"],
            [f"pair:{source_record['pair_id']}", "role:protected", "HAS_ROLE"],
            [f"event:{source_record['event_id']}", f"reference:{source_record['reference_cycle_id']}", "USES_REFERENCE"],
            [f"event:{source_record['event_id']}", f"active:{source_record['active_cycle_id']}", "OCCURS_IN"],
            [f"event:{source_record['event_id']}", f"family:{source_record['family']}", "BELONGS_TO_FAMILY"],
        ],
        "node_features": {
            "role:hunter": {"role": "hunter"},
            "role:protected": {"role": "protected"},
        },
    }
    geometry = [
        source_record.get("hunter_touch_overrun_ticks"),
        source_record.get("protected_distance_to_level_ticks"),
        source_record.get("reference_range_ticks"),
        source_record.get("active_range_ticks"),
    ]
    hunter_row = [0.0 if value is None else float(value) for value in geometry]
    protected_row = [
        0.0,
        0.0 if source_record.get("protected_distance_to_level_ticks") is None else float(source_record["protected_distance_to_level_ticks"]),
        0.0 if source_record.get("reference_range_ticks") is None else float(source_record["reference_range_ticks"]),
        0.0 if source_record.get("active_range_ticks") is None else float(source_record["active_range_ticks"]),
    ]
    return {
        "sparse_events": [event],
        "graph": graph,
        "intermarket_symbols": ["HUNTER_ROLE", "PROTECTED_ROLE"],
        "intermarket_matrix": [hunter_row, protected_row],
    }


def cluster_dimensions(source_record: Mapping[str, Any], *, label_horizon_group: str = "unbound") -> Mapping[str, Any]:
    return {
        "pair_id": source_record["pair_id"],
        "family": source_record["family"],
        "reference_cycle_id": source_record["reference_cycle_id"],
        "active_cycle_id": source_record["active_cycle_id"],
        "level_side": source_record["level_side"],
        "confirmation_close_time_ms": source_record["confirmation_close_time_ms"],
        "trading_day_ny": source_record["trading_day_ny"],
        "label_horizon_group": label_horizon_group,
    }
