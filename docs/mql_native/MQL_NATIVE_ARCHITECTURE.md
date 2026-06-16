# MQL-Native Runtime Architecture

## Decision

The active runtime is now MQL5-native.

Python, FastAPI, React, Parquet caches, CSV bridges, and external watcher loops are removed from the execution path. The archived Python implementation remains historically available in the `archive/python-brain-m0001` branch.

## Runtime Flow

```text
MT5 chart / Strategy Tester
        ↓
DAL_Bars.mqh
        ↓
DAL_LRuleDetector.mqh
        ↓
DAL_M0001Engine.mqh
        ↓
DAL_M0001Visual.mqh
        ↓
M0001_LiveVisualLab.mq5
```

## Source of Truth

MQL5 is now the source of truth for:

- candle access
- L-rule structural node detection
- M0001 RTV event construction
- live-safe visual validation
- Strategy Tester behavior
- validation journal export

## Research Structure

The lab structure remains unchanged:

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

The research discipline stays. Only the active runtime changes.

## Module Layout

```text
mql5/
  Experts/
    DecisionAlphaLab/
      M0001/
        M0001_LiveVisualLab.mq5

  Include/
    DecisionAlphaLab/
      Common/
      Market/
      StructuralNodes/
      M0001/
      Research/

  Scripts/
    DecisionAlphaLab/
      M0001/
        M0001_ExportValidationJournal.mq5
```
