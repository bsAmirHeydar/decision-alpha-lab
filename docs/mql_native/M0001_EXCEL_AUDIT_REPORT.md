# M0001 Excel Audit Report

## Input

```text
InpWriteExcelReport = true
```

## Output

When enabled, the expert writes an Excel-readable report file:

```text
<symbol>_M0001_full_audit_report.xls
```

The file is an HTML `.xls` report that opens directly in Excel. It is generated
from MQL without requiring Python or external libraries.

## Report sections

The report contains:

1. Run Summary
2. State Semantics
3. Structural Nodes
4. Node Audit States - Touch / Hunt / Consumption
5. Events / RTV

## Node audit fields

Each node includes:

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
expansion_extreme
territory_lower
territory_upper
```

## Event fields

Each event includes:

```text
revisit_id
entry_time
exit_time
event_length
event_extreme
territory_lower
territory_upper
mean_before
mean_inside
rtv
hunted
consumed
consume_reason
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.33`.
