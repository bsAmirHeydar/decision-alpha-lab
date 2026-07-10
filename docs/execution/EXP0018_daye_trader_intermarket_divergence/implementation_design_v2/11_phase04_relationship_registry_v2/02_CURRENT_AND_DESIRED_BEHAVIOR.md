---
id: EXP0018-P04-BEHAVIOR
title: "P04 Current and Desired Behavior"
type: behavior-contract
status: active
project: EXP0018
phase: P04
---
# Current and Desired Behavior

Before P04, previous-period links existed as indexing aids in P03 but no module owned the meaning of `PA`, `AL`, `LN`, `p4a1`, or the other Daye aliases. Desired behavior is a single registry that removes conditional-code drift and right-to-left alias ambiguity.

The same registry drives live processing, replay, tests, audit, and documentation. A relationship is resolved only when the exact current period and exact expected reference period are present under the selector declared by that record.
