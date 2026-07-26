---
id: EXP0018-P05-ELIGIBILITY
title: "P05 Eligibility and Fail-Closed Rules"
project: EXP0018
phase: P05
status: implemented-awaiting-metaeditor-validation
---

# Eligibility

P05 requires a P04 `READY` resolution. Each reference symbol period must be `COMPLETE`. Each current symbol period must be `OPEN` or `COMPLETE` according to the upstream P04 policy.

Invalid, zero, missing, partial, or unavailable reference prices fail closed. No fallback reference, nearest period, previous close, or synthetic price is permitted.
