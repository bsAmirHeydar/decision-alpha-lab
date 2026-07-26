# CH20 — CG Overlap Complexity and Future Decision Gate

## 1. Why CG overlap matters

The strategy architect identified CG overlap as a possible source of model complexity.

This is accurate because the strategy allows all CGs to remain active, independent, and valid before statistical testing. That creates a rich but complex signal field.

## 2. Forms of CG overlap

CG overlap may appear as:

- same-direction overlap;
- opposite-direction overlap;
- overlap between small CG and large CG;
- multiple CGs confirming on the same candle;
- multiple CGs confirming close to each other;
- one CG entering while another is still open;
- overlapping time targets;
- overlapping stops;
- overlapping clean-symbol roles;
- overlapping hunter roles;
- hedge creation;
- signal clusters across the day.

## 3. Base doctrine toward overlap

The base doctrine does not eliminate overlap.

Overlap is allowed. It is recorded. It is measured. It is not treated as automatically good or bad.

This means:

- overlap does not automatically strengthen a signal;
- overlap does not automatically weaken a signal;
- overlap does not automatically cancel a signal;
- opposite-direction overlap does not automatically block trade permission;
- same-direction overlap does not automatically increase position size;
- multi-CG agreement does not become confluence before statistics.

## 4. Why overlap may complicate the model

Overlap complicates analysis because one market moment can belong to several families at once.

A single confirmed divergence may have relationships to:

- a specific CG;
- another overlapping CG;
- a direction cluster;
- a symbol-role cluster;
- a time-window cluster;
- a reference-distance cluster;
- a position-cluster state;
- a stop-pressure state;
- a hedge-state field.

The model must avoid double-counting or false conclusions.

## 5. Recommended tracking fields for overlap

The reporting layer should preserve at least these overlap fields:

- number of active confirmed signals at entry time;
- number of active CG families in same direction;
- number of active CG families in opposite direction;
- smallest active CG;
- largest active CG;
- current signal is alone or clustered;
- current signal is part of hedge cluster or not;
- same-symbol exposure count;
- opposite-symbol exposure count;
- same-cycle simultaneous confirmations;
- nearby confirmations inside a chosen time distance;
- overlap result compared to non-overlap result.

## 6. Future decision gate

After statistics, the strategy architect may decide whether overlap becomes:

- just a report field;
- a warning field;
- a ranking field;
- a filter;
- a position-sizing modifier;
- an exposure-control rule;
- a hedge-control rule;
- a future AI score component.

But not now.

## 7. Chapter 20 overlap statement

CG overlap is a likely source of complexity and potential information. It should be measured deeply, not suppressed early.
