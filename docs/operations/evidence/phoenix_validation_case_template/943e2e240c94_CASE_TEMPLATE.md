# Phoenix Validation Case Template

```yaml
case_id:
title:
status: baseline_required
broker_symbol:
timeframe:
bars_to_scan:
from_time:
to_time:
timezone_or_broker_time:
mt5_build:
source_commit:
phoenix_version:
identity_config_hash:
inputs_summary:
expected_min_bars:
expected_max_bars:
expected_min_scales:
expected_max_scales:
expected_min_raw_nodes:
expected_max_raw_nodes:
expected_min_canonical_nodes:
expected_max_canonical_nodes:
expected_min_hooks:
expected_max_hooks:
expected_min_nd:
expected_max_nd:
expected_min_events:
expected_max_events:
expected_min_visible_events:
expected_max_visible_events:
expected_min_hidden_events:
expected_max_hidden_events:
expected_min_f1:
expected_max_f1:
expected_min_f2:
expected_max_f2:
expected_min_f3:
expected_max_f3:
expected_min_locked_f3:
expected_max_locked_f3:
validation_csv:
events_csv:
hooks_csv:
summary_csv:
manifest_csv:
known_screenshot:
notes:
```

## Acceptance notes

- Validation must be run after Level 11.5 export and Level 12 renderer.
- Missing expected ranges are allowed only while `status=baseline_required`.
- When a case becomes `baselined`, every important expected count must be set as an exact value or a narrow documented range.
