---
title: "FP-I07 Missed Close Is A Replay Problem"
tags: [atomic, exp0019, fp-i07]
---
# Definition

A later tick cannot reconstruct what was causally known at a missed close.

## Operational consequence

This rule is enforced by FP-I07 contracts, tests, reason codes, and the MQL5 mirror.
