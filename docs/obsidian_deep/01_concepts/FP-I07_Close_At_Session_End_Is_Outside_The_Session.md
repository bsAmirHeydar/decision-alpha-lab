---
title: "FP-I07 Close At Session End Is Outside The Session"
tags: [atomic, exp0019, fp-i07]
---
# Definition

Session windows are half-open; equality with the end is expiry, not confirmation.

## Operational consequence

This rule is enforced by FP-I07 contracts, tests, reason codes, and the MQL5 mirror.
