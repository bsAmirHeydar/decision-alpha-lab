---
type: policy
status: canonical
language: english
project: Decision Alpha Lab
related:
  - F2_Waist_Hit_Point1_Point2
  - No_Stop_No_Trade
  - Wide_Zone_Requires_Child_Zone
---

# F2 Waist-Hit Execution Policy

## Rule

The F2 waist-hit Point-1/Point-2 structure creates reversal potential, not automatic execution permission.

## Direct Trade Policy

```text
Direct parent-timeframe F2 waist-hit trade = not allowed by default.
```

Exception only exists if the parent timeframe itself produces a stable, narrow stop edge. Otherwise, lower-timeframe refinement is mandatory.

## Child-Zone Requirement

A valid child zone must provide:

- a clear start edge;
- a clear expiration/stop edge;
- acceptable width;
- asymmetric potential;
- no violation of the parent context;
- limit-entry compatibility.

## Why

The doctrine is antifragile: the system must pay small, bounded costs for open-ended potential. A broad parent F2 field does not satisfy that requirement by itself.
