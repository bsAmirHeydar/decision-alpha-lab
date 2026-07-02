# Flag Counting Stabilization Patch 01 — Level 24-30 No-Send Chain

## Purpose

This patch is not a new feature level.

It stabilizes the no-send chain after Level 30.

The patch focuses on compile-risk reduction, export-switch consistency, ledger snapshot correctness, and small guard fixes.

## Scope

The patch touches only the generated Level 24 and Level 27-30 support modules:

```text
FP_SafetyGateRules.mqh
FP_BrokerRequestLedgerExport.mqh
FP_BrokerRequestLedgerEngine.mqh
FP_BrokerRequestAuditExport.mqh
FP_BrokerRequestAuditEngine.mqh
FP_PaperBrokerAdapterExport.mqh
FP_PaperBrokerAdapterEngine.mqh
FP_PaperBrokerLifecycleExport.mqh
FP_PaperBrokerLifecycleEngine.mqh
```

## What changed

### 1. Export master switch consistency

Level 27, Level 28, Level 29, and Level 30 all had an `export_csv` config field.

This patch makes the latest and append exporters respect that master switch:

```text
if export_csv is false, no latest CSV and no append CSV are written.
```

This keeps behavior consistent with Level 19-26.

### 2. Latest / append row flags

The latest CSV and append ledger rows now receive the intended write-state flags before serialization.

This prevents rows from saying:

```text
latest_written=false
ledger_written=false
```

inside files that were actually written.

The stabilized rows now set expected values from config before export:

```text
latest_written = export_csv && write_latest_csv
ledger/audit/adapter/lifecycle_written = export_csv && append_enabled && !duplicate_skipped
```

### 3. Safety Gate allow-list trimming

Level 24 allow-list token trimming now assigns the trimmed value back to the token.

This avoids silent whitespace issues in inputs such as:

```text
GOLD*, EURUSD, PERIOD_M5
```

### 4. Prefix wildcard support

Level 24 symbol/timeframe allow-list now supports simple prefix wildcard tokens such as:

```text
GOLD*
XAU*
PERIOD_M*
```

`*` alone still means allow all.

## What did not change

This patch does not add:

```text
OrderSend
OrderCheck
CTrade
broker request
real order
position
volume sizing
risk sizing
real execution
renderer mutation
chart-object mutation
```

## No-send boundary

The no-send chain remains intact:

```text
Level 25 Broker Dry Run Preview
Level 26 Broker Validator / No Send
Level 27 Broker Request Ledger / No Send
Level 28 Broker Request Audit / No Send
Level 29 Paper Broker Adapter / No Send
Level 30 Paper Broker Lifecycle / No Send
```

## Correct next step

After applying this patch, compile in MetaEditor.

Do not add Level 31 before compile is clean.

The next engineering step should be one of:

```text
compile-fix patch if MetaEditor reports errors
consolidation patch if compile is clean
final_decision_state.csv if the CSV chain is behaving correctly
```
