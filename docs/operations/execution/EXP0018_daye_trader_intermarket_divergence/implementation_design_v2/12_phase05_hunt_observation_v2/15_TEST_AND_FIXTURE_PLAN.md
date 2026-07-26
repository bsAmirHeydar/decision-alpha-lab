---
id: EXP0018-P05-TESTS
title: "P05 Test and Fixture Plan"
project: EXP0018
phase: P05
status: implemented-awaiting-metaeditor-validation
---

# Required fixtures

- no touch on HIGH and LOW;
- A-only and B-only touch;
- double touch;
- exact equality for each symbol and side;
- invalid reference price;
- unavailable relationship;
- deterministic observation identity;
- open-period state transitions;
- no refresh suppression when current-period availability advances.

The machine-readable fixture catalog contains ten positive classification cases. Embedded MQL5 tests cover one-sided, equality, low-side, double-touch, and identity behavior.
