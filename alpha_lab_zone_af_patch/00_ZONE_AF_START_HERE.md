---
type: entrypoint
id: ZONE-AF-START
status: draft
language: english
created: 2026-07-06
project: Decision Alpha Lab
aliases:
  - Zone Antifragile Start
  - Zone-Centric Alpha Start
---

# Zone-Centric Antifragile Alpha Architecture

This is the entrypoint for the Zone-Centric Antifragile Trading layer of Decision Alpha Lab.

The central thesis is simple:

> A zone is not a pattern. A zone is a risk contract.

A zone is a bounded price area where:

- the first touch or first tradable edge of the area is the probable limit-entry area;
- the far side of the area is the expiration point of the thesis;
- the loss is bounded by the width and stop policy of the zone;
- the profit is intentionally left open, grown, trailed, or expanded when the market releases energy;
- the trade is justified only when the estimated potential is meaningfully larger than the cost of being wrong.

## Start Here

1. [[docs/obsidian_zone/00_mocs/ZONE_MOC|Zone MOC]]
2. [[docs/zone_af/ZONE-AF-0001_Zone_Centric_Antifragile_Philosophy|ZONE-AF-0001 — Zone-Centric Antifragile Philosophy]]
3. [[docs/zone_af/ZONE-AF-0002_Zone_Object_Lifecycle_and_Risk_Contract|ZONE-AF-0002 — Zone Object, Lifecycle, and Risk Contract]]
4. [[docs/zone_af/ZONE-AF-0003_Mechanical_Zone_Sources_Hook_F1_F2_F3|ZONE-AF-0003 — Mechanical Zone Sources: Hook, F1, F2, F3]]
5. [[docs/zone_af/ZONE-AF-0004_Fractal_Multi_Timeframe_Zone_Architecture|ZONE-AF-0004 — Fractal Multi-Timeframe Zone Architecture]]
6. [[docs/zone_af/ZONE-AF-0005_Limit_Entry_Risk_and_Profit_Growth_Policy|ZONE-AF-0005 — Limit Entry, Risk, and Profit Growth Policy]]
7. [[docs/zone_af/ZONE-AF-0006_Learning_Objective_Dataset_and_Training_Contract|ZONE-AF-0006 — Learning Objective, Dataset, and Training Contract]]
8. [[docs/zone_af/ZONE-AF-0007_Bot_Mind_Internal_Cognitive_Architecture|ZONE-AF-0007 — Bot Mind Internal Cognitive Architecture]]

## Core Rule

The project must not search for decorative or arbitrary chart patterns. It must estimate whether a bounded risk can buy access to an asymmetric, open-ended payoff.

## Core Pipeline

```text
Mechanical Context
  -> Movement Constraint
  -> Approximate Reversal Area
  -> Zone Candidate
  -> Entry Edge
  -> Stop / Expiration Edge
  -> Potential Estimation
  -> Limit Order Decision
  -> Outcome Logging
  -> Antifragile Learning
```

