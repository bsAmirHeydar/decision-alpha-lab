---
type: strategy-factory-document
status: canonical
title: "Outcome Engine and Path Accounting"
tags:
  - strategy-factory
---

# Outcome Engine and Path Accounting

The outcome engine replays each candidate under explicit fill, ambiguity, stop, target, and time rules and produces a canonical path record.

## Outputs

For every candidate record fill status/time/price, exit time/price/reason, gross and net R, MFE, MAE, time to extrema, holding time, cost components, ambiguous-bar count, and label end time. Multi-stage policies also record transitions.

## Conservative ambiguity

When stop and target appear inside the same OHLC bar and tick sequence is unavailable, official reports use a declared conservative policy, normally stop-first or reject-ambiguous. Target-first may be shown as an optimistic sensitivity bound, never as the sole result.

## No fill behavior

Unfilled candidates remain in the opportunity dataset. Fill rate, missed positive paths, and adverse selection are part of policy evaluation. Dropping unfilled orders overstates deployability.

## Path versus execution R

MFE and structural path distances are descriptive. Net execution R uses the actual initial risk and all costs. Reports label them separately.

