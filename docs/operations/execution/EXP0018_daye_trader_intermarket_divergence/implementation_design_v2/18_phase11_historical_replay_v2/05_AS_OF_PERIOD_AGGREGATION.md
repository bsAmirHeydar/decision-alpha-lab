---
id: EXP0018-P11-05_AS_OF_PERIOD_AGGREGATION
title: "As-of period aggregation"
project: EXP0018
phase: P11
status: implemented
tags: [exp0018, daye, phase11, replay]
---

# As-of period aggregation

P11 calls the P03 pure aggregator on the visible prefix. Daily, session, and subcycle snapshots preserve OPEN/PARTIAL/COMPLETE semantics at each cursor. The 17–18 New York gap remains excluded, p4 remains thirty minutes, and DST changes expected UTC bar counts without changing local Daye boundaries.
