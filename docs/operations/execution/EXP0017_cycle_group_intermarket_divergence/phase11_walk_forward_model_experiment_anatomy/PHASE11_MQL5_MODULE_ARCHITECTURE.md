# Phase 11 — MQL5 Module Architecture

## Expert

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_WalkForward_Model_Experiment_Anatomy.mq5
```

## Include modules

```text
CGWF_Types.mqh
CGWF_CsvReader.mqh
CGWF_Splitter.mqh
CGWF_BaselineModel.mqh
CGWF_Ledger.mqh
CGWF_Display.mqh
CGWF_Engine.mqh
```

## Responsibility split

### CGWF_Types

Defines config, dataset row, fold, bucket model, prediction, metric, summary, and shared utility functions.

### CGWF_CsvReader

Reads `EXP0017_Phase10_Model_Dataset.csv`, maps headers, filters invalid rows, and keeps only `model_ready` rows by default.

### CGWF_Splitter

Sorts rows chronologically and builds rolling train/embargo/test folds.

### CGWF_BaselineModel

Builds leakage-safe training bucket baselines and evaluates future test samples.

### CGWF_Ledger

Writes fold plan, predictions, bucket validation, fold metrics, summary, and diagnostics.

### CGWF_Display

Shows compact chart/expert log summary.

### CGWF_Engine

Coordinates the entire offline experiment.
