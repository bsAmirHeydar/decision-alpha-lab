# RTHP Cross-Symbol Cycle Divergence

Generated context package for `rthp.cross_symbol_cycle_divergence` version `1.0.0`.

## Features
- `rthp.active_cycle_progress` — float; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.active_cycle_type` — category; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.active_range_ticks` — float; known-time: `known_at_rthp_observation_cut`; required: `false`
- `rthp.available_reference_count` — int; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.cycle_completeness` — category; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.data_status` — category; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.day_of_week_ny` — int; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.family` — category; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.history_coverage_ratio` — float; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.history_sufficiency` — category; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.hunter_role` — category; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.hunter_touch_overrun_ticks` — float; known-time: `known_at_rthp_observation_cut`; required: `false`
- `rthp.is_intraday_family` — bool; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.is_m15_cycle_group` — bool; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.is_same_day_reference` — bool; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.is_sequential` — bool; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.level_side` — category; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.max_freshness_age_ms` — int; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.minute_of_day_ny` — int; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.minute_of_session` — int; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.polarity` — category; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.protected_distance_to_level_ticks` — float; known-time: `known_at_rthp_observation_cut`; required: `false`
- `rthp.reference_age_cycles` — int; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.reference_cycle_type` — category; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.reference_range_ticks` — float; known-time: `known_at_rthp_observation_cut`; required: `false`
- `rthp.reference_state_at_cut` — category; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.reference_to_active_gap_cycles` — int; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.required_reference_count` — int; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.sequentiality` — category; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.simultaneous_family_count` — int; known-time: `known_at_rthp_observation_cut`; required: `true`
- `rthp.touch_to_confirmation_ms` — int; known-time: `known_at_rthp_observation_cut`; required: `true`

## Views
- `rthp.tabular.v1` — features: rthp.active_cycle_progress, rthp.active_cycle_type, rthp.active_range_ticks, rthp.available_reference_count, rthp.cycle_completeness, rthp.data_status, rthp.day_of_week_ny, rthp.family, rthp.history_coverage_ratio, rthp.history_sufficiency, rthp.hunter_role, rthp.hunter_touch_overrun_ticks, rthp.is_intraday_family, rthp.is_m15_cycle_group, rthp.is_same_day_reference, rthp.is_sequential, rthp.level_side, rthp.max_freshness_age_ms, rthp.minute_of_day_ny, rthp.minute_of_session, rthp.polarity, rthp.protected_distance_to_level_ticks, rthp.reference_age_cycles, rthp.reference_cycle_type, rthp.reference_range_ticks, rthp.reference_state_at_cut, rthp.reference_to_active_gap_cycles, rthp.required_reference_count, rthp.sequentiality, rthp.simultaneous_family_count, rthp.touch_to_confirmation_ms; shape: [31]
- `rthp.sparse_event.v1` — features: rthp.family, rthp.level_side, rthp.polarity, rthp.hunter_role, rthp.reference_state_at_cut, rthp.sequentiality, rthp.data_status; shape: [1]
- `rthp.sequence.v1` — features: rthp.active_cycle_progress, rthp.available_reference_count, rthp.history_coverage_ratio, rthp.max_freshness_age_ms, rthp.minute_of_session, rthp.reference_age_cycles, rthp.reference_to_active_gap_cycles, rthp.simultaneous_family_count, rthp.touch_to_confirmation_ms; shape: [9, 16]
- `rthp.intermarket.v1` — features: rthp.hunter_touch_overrun_ticks, rthp.protected_distance_to_level_ticks, rthp.reference_range_ticks, rthp.active_range_ticks; shape: [2, 4]
- `rthp.graph.v1` — features: rthp.family, rthp.level_side, rthp.polarity, rthp.hunter_role, rthp.reference_state_at_cut, rthp.sequentiality, rthp.data_status; shape: [1]

## Authority
This package cannot send orders, bypass shared economics, or read future data.
