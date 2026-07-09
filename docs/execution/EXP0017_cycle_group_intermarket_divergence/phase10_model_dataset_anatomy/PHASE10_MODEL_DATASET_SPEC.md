# Phase 10 — Model Dataset Specification

## Purpose

Phase 10 is the first explicit model-preparation layer. It takes the research ledger produced by Phase 07 and turns it into a stable rectangular dataset.

The dataset is designed for:

- offline statistical analysis;
- supervised model experiments;
- feature importance studies;
- train/test split design;
- later Phase 11 feature-store export;
- future AI analyst/ranker integration.

## Non-execution boundary

The dataset may contain labels such as `WIN`, `LOSS`, `label_hit_1r`, and `label_stopped_intraday`. These labels are historical facts. They do not authorize execution.

## Main row contract

One Phase 10 row equals one Phase 07 outcome sample.

A row contains:

1. identity fields;
2. anatomy fields;
3. time/session fields;
4. role fields;
5. risk geometry fields;
6. multi-window outcome fields;
7. label fields;
8. ranking enrichment fields;
9. model-use status fields.

## Labeling policy

The primary label window is configurable:

- cycle end;
- +1 cycle;
- +2 cycles;
- +3 cycles;
- day end;
- MFE.

The default is cycle-end. That preserves the current doctrine: target study begins at the end of the active cycle.
