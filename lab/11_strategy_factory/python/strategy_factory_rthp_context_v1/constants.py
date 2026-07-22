"""Closed RTHP AI-input vocabulary. This module contains no engine logic."""
from __future__ import annotations

CONTEXT_ID = "CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1"
CONTEXT_VERSION = "1.0.2"
PACKAGE_ID = "rthp.cross_symbol_cycle_divergence"
PACKAGE_VERSION = "1.0.0"
PACKAGE_KEY = f"{PACKAGE_ID}@{PACKAGE_VERSION}"
OWNER_ID = "rthp.context.owner"
DOCTRINE_ID = "rthp.cross_symbol_cycle_divergence.doctrine"
DOCTRINE_VERSION = "1.0.2"
ADAPTER_ID = "rthp.acl03.canonical_occurrence_adapter"
ADAPTER_VERSION = "1.0.0"

FAMILIES = (
    "WW", "DD", "NN", "LN", "AN", "NL", "NA", "FCR", "PMI", "PP", "M15_CYCLE_GROUP"
)
LEVEL_SIDES = ("HIGH", "LOW")
POLARITIES = ("BULLISH_DIVERGENCE", "BEARISH_DIVERGENCE")
SEQUENTIALITIES = ("SEQUENTIAL", "NON_SEQUENTIAL", "NOT_APPLICABLE")
DATA_STATUSES = ("VALID", "PARTIAL_HISTORY")
HISTORY_SUFFICIENCIES = ("FULL", "PARTIAL")
CYCLE_COMPLETENESS = ("COMPLETE", "PARTIAL", "PARTIAL_MARKET_WEEK_END")
HUNTER_ROLES = ("PRIMARY", "SECONDARY")
REFERENCE_STATES_AT_CUT = ("DIVERGENCE_CONFIRMED",)
ACTIVE_CYCLE_TYPES = (
    "CURRENT_WEEK", "CURRENT_DAILY", "CURRENT_L", "CURRENT_N", "CURRENT_A", "FCR_2", "PP_2", "CURRENT_M15_IN_N"
)
REFERENCE_CYCLE_TYPES = (
    "PREVIOUS_COMPLETED_WEEK", "PREVIOUS_DAILY", "PREVIOUS_N", "CURRENT_L", "PREVIOUS_L", "PREVIOUS_A", "FCR_1", "PP_1", "PRIOR_M15_IN_SAME_N"
)

REQUIRED_SOURCE_FIELDS = (
    "context_id", "context_version", "event_id", "confirmed_context_event", "family", "pair_id",
    "cycle_definition_version", "active_cycle_id", "reference_cycle_id", "active_cycle_type",
    "reference_cycle_type", "level_side", "polarity", "primary_symbol", "secondary_symbol",
    "hunter_symbol", "protected_symbol", "event_time_ms", "known_time_ms", "confirmation_time_ms",
    "observation_cut_ms", "decision_time_ms", "confirmation_close_time_ms", "data_status",
    "history_sufficiency", "available_reference_count", "required_reference_count", "reference_age_cycles",
    "reference_to_active_gap_cycles", "sequentiality", "cycle_completeness", "is_same_day_reference",
    "minute_of_session", "minute_of_day_ny", "day_of_week_ny", "active_cycle_progress",
    "simultaneous_family_count", "primary_freshness_age_ms", "secondary_freshness_age_ms",
    "reference_state_at_cut", "trading_day_ny", "source_revision", "source_content_hash", "auxiliary",
)

OPTIONAL_GEOMETRY_FIELDS = (
    "hunter_touch_overrun_ticks", "protected_distance_to_level_ticks", "reference_range_ticks", "active_range_ticks"
)

TASKS = (
    ('rthp.reference_exhausted.15m', '1.0.0', 'binary', 'rthp.label.reference_exhausted_900s'),
    ('rthp.reference_exhausted.30m', '1.0.0', 'binary', 'rthp.label.reference_exhausted_1800s'),
    ('rthp.reference_exhausted.60m', '1.0.0', 'binary', 'rthp.label.reference_exhausted_3600s'),
    ('rthp.reference_exhausted.by_active_cycle_end', '1.0.0', 'binary', 'rthp.label.reference_exhausted_by_active_cycle_end'),
    ('rthp.time_to_reference_exhaustion', '1.0.0', 'survival', 'rthp.label.time_to_reference_exhaustion'),
    ('rthp.hunter.polarity_signed_log_return.15m', '1.0.0', 'regression', 'rthp.label.hunter_polarity_signed_log_return_900s'),
    ('rthp.hunter.polarity_aligned_direction.15m', '1.0.0', 'binary', 'rthp.label.hunter_polarity_aligned_direction_900s'),
    ('rthp.hunter.polarity_signed_log_return.30m', '1.0.0', 'regression', 'rthp.label.hunter_polarity_signed_log_return_1800s'),
    ('rthp.hunter.polarity_aligned_direction.30m', '1.0.0', 'binary', 'rthp.label.hunter_polarity_aligned_direction_1800s'),
    ('rthp.hunter.polarity_signed_log_return.60m', '1.0.0', 'regression', 'rthp.label.hunter_polarity_signed_log_return_3600s'),
    ('rthp.hunter.polarity_aligned_direction.60m', '1.0.0', 'binary', 'rthp.label.hunter_polarity_aligned_direction_3600s'),
    ('rthp.hunter.polarity_signed_log_return.active_cycle_end', '1.0.0', 'regression', 'rthp.label.hunter_polarity_signed_log_return_active_cycle_end'),
    ('rthp.hunter.polarity_aligned_direction.active_cycle_end', '1.0.0', 'binary', 'rthp.label.hunter_polarity_aligned_direction_active_cycle_end'),
    ('rthp.hunter.mfe.60m', '1.0.0', 'regression', 'rthp.label.hunter_mfe_3600s'),
    ('rthp.hunter.mae.60m', '1.0.0', 'regression', 'rthp.label.hunter_mae_3600s'),
    ('rthp.family_relative_strength.hunter.60m', '1.0.0', 'ranking', 'rthp.label.hunter_polarity_signed_log_return_3600s'),
    ('rthp.reference_age_effectiveness.hunter.60m', '1.0.0', 'ranking', 'rthp.label.hunter_polarity_signed_log_return_3600s'),
    ('rthp.protected.polarity_signed_log_return.15m', '1.0.0', 'regression', 'rthp.label.protected_polarity_signed_log_return_900s'),
    ('rthp.protected.polarity_aligned_direction.15m', '1.0.0', 'binary', 'rthp.label.protected_polarity_aligned_direction_900s'),
    ('rthp.protected.polarity_signed_log_return.30m', '1.0.0', 'regression', 'rthp.label.protected_polarity_signed_log_return_1800s'),
    ('rthp.protected.polarity_aligned_direction.30m', '1.0.0', 'binary', 'rthp.label.protected_polarity_aligned_direction_1800s'),
    ('rthp.protected.polarity_signed_log_return.60m', '1.0.0', 'regression', 'rthp.label.protected_polarity_signed_log_return_3600s'),
    ('rthp.protected.polarity_aligned_direction.60m', '1.0.0', 'binary', 'rthp.label.protected_polarity_aligned_direction_3600s'),
    ('rthp.protected.polarity_signed_log_return.active_cycle_end', '1.0.0', 'regression', 'rthp.label.protected_polarity_signed_log_return_active_cycle_end'),
    ('rthp.protected.polarity_aligned_direction.active_cycle_end', '1.0.0', 'binary', 'rthp.label.protected_polarity_aligned_direction_active_cycle_end'),
    ('rthp.protected.mfe.60m', '1.0.0', 'regression', 'rthp.label.protected_mfe_3600s'),
    ('rthp.protected.mae.60m', '1.0.0', 'regression', 'rthp.label.protected_mae_3600s'),
    ('rthp.family_relative_strength.protected.60m', '1.0.0', 'ranking', 'rthp.label.protected_polarity_signed_log_return_3600s'),
    ('rthp.reference_age_effectiveness.protected.60m', '1.0.0', 'ranking', 'rthp.label.protected_polarity_signed_log_return_3600s'),
    ('rthp.family_relative_exhaustion_strength.60m', '1.0.0', 'ranking', 'rthp.label.reference_exhausted_3600s'),
)
