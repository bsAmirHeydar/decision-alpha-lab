# Decision Alpha Lab

A research-first quantitative trading laboratory.

## Runtime Direction

The active runtime is now **MQL5-native**.

Python, FastAPI, React, Parquet cache pipelines, and external bridge/watch loops have been removed from the active execution path. The archived Python implementation should remain in the branch:

```text
archive/python-brain-m0001
```

Current active development should happen on:

```text
mql-native-migration
```

## Why MQL-native

The project needs fast, live-safe, visually auditable iteration inside MT5 Strategy Tester and charts. A separate Python process introduced asynchronous delay, shared-file friction, CSV adapter complexity, and live-semantics ambiguity.

MQL5 now owns:

- market data access
- L-rule structural node detection
- M0001 RTV event construction
- visual validation
- tester behavior
- validation journal export

## MQL5 Entry Points

Expert:

```text
mql5/Experts/DecisionAlphaLab/M0001/M0001_LiveVisualLab.mq5
```

Includes:

```text
mql5/Include/DecisionAlphaLab/
```

Validation export script:

```text
mql5/Scripts/DecisionAlphaLab/M0001/M0001_ExportValidationJournal.mq5
```

## Research Structure

The lab workflow remains:

```text
lab/01_observation
lab/02_hypotheses
lab/03_experiments
lab/04_analysis
lab/05_validation
lab/06_production
lab/07_monitoring
lab/08_archive
```

The runtime changed. The research discipline did not.

## Apply Locally

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\apply_mql_native_migration.ps1
```

To also copy files into an MT5 terminal data folder:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\apply_mql_native_migration.ps1 -TerminalDataPath "C:\Users\<YOU>\AppData\Roaming\MetaQuotes\Terminal\<TERMINAL_ID>"
```

Then compile:

```text
MQL5/Experts/DecisionAlphaLab/M0001/M0001_LiveVisualLab.mq5
```

## Documentation

- `docs/mql_native/MQL_NATIVE_ARCHITECTURE.md`
- `docs/mql_native/M0001_MQL_NATIVE_SPEC.md`
- `docs/mql_native/MODULE_MAP.md`
