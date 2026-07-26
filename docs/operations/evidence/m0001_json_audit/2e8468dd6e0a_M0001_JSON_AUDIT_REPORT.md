# M0001 JSON Audit Report

## Input

```text
InpWriteJsonReport = true
InpJsonReportUseFullHistorySnapshot = true
```

## Output

```text
reports\mql_native\M0001\<symbol>_M0001_full_audit_report.json
```

If the prefixed path fails, the writer falls back to:

```text
<symbol>_M0001_full_audit_report.json
```

inside the MT5 Files sandbox.

## JSON sections

```json
{
  "schema": "decision-alpha-lab.m0001.audit_report.v1",
  "run": {},
  "semantics": {},
  "nodes": [],
  "node_audit_states": [],
  "events": []
}
```

## Fields

The JSON includes all state-machine fields discussed:

```text
touch_started
first_touch_time
touch_confirmed
touch_confirmed_time
hunted
hunt_time
consumed
consumed_time
consume_reason
active
territory_lower
territory_upper
expansion_extreme
revisit_id
entry_time
exit_time
mean_before
mean_inside
rtv
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.38`.
