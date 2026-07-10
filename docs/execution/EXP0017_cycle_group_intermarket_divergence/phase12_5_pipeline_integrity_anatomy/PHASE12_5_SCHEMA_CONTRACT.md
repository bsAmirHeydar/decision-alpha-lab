# Phase 12.5 Schema Contract

## Contract philosophy

A column name is an API. Renaming `actual_stop` to `stopped` without a versioned migration is a breaking change.

## Critical row-level contracts

### Phase 07 outcome study

Identity and anatomy:

- `outcome_id`, `signal_id`
- `group`, `group_minutes`, `current_cycle`, `reference_cycle`
- `direction`, `side`, `clean_symbol`, `hunter_symbol`
- `confirmation_ny`

Outcome geometry:

- `entry_price`, `stop_price`, `stop_points`
- `cycle_end_r`, `mfe_r`, `mae_r`
- `stop_hit_intraday`, `daily_range_points`

### Phase 10 model dataset

Must preserve Phase 07 identity and add:

- `sample_id`
- `model_use_status`
- `reference_age_cycles`
- `role_key`
- `primary_window`, `primary_r`
- `label_class`, `label_binary_win`, `label_stopped_intraday`

### Phase 11 predictions

Must preserve Phase 10 identity and add fold/model evidence:

- `fold_id`, `sample_id`, `signal_id`
- `bucket_key`, `bucket_source`
- `predicted_avg_r`, `predicted_win_rate`
- `actual_r`, `actual_win`, `actual_loss`, `actual_stop`

## Aggregate contracts

Phase 08 and Phase 09 files are checked by stable dimension/bucket keys. Phase 10 and Phase 11 summary files use `metric,value` contracts.

## Migration rule

A future schema change requires:

1. producer update;
2. consumer update;
3. contract version update;
4. migration note;
5. fixture update;
6. Phase 12.5 successful rerun.
