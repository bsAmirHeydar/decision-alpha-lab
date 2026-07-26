---
title: "LCM-08B — 07 Data Normalization Contract"
status: accepted-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-08b, pilot-migration]
phase_id: LCM-08B
---
# Data Normalization Contract

Accepted time columns are `time`, `time_utc`, `datetime`, and `date`. OHLC are mandatory. Missing volume becomes zero. Numeric coercion uses pandas semantics. Rows with missing time or OHLC are dropped. Rows sort ascending. Duplicate timestamps keep the last row. Series align by exact timestamp inner join. Every rule is preserved from the source rather than improved.
