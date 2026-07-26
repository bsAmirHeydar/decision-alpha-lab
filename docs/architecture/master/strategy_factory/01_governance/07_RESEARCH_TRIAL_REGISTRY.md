---
type: strategy-factory-document
status: canonical
title: "Research Trial Registry"
tags:
  - strategy-factory
---

# Research Trial Registry

Overfitting begins when the project forgets how many ideas, filters, thresholds, models, and candidate combinations were tried. The trial registry makes the search surface explicit.

## What counts as a trial

Changing a feature set, entry parameter, stop buffer, target R, session, symbol pair, model family, selection metric, threshold, fold plan, or data period counts. Cosmetic report changes do not. A trial is counted even if it is abandoned before publication.

## Family accounting

Trials are grouped by hypothesis family so false-discovery and deflated-performance controls use a defensible number of attempts. The registry stores hypothesis hash, dataset hash, feature hash, candidate hash, start time, status, and selection metric. Deleted notebooks do not erase trials.

## Operational rule

No promotion report may state a Sharpe, expectancy, or p-value without also stating the number of related trials. The anti-overfit suite uses this count for Deflated Sharpe and research-selection context.

