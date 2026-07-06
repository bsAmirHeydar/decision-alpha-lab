---
type: canonical_architecture
id: ZONE-AF-0004
status: draft
language: english
project: Decision Alpha Lab
concepts:
  - Fractal Zones
  - Parent Zone
  - Child Zone
  - Multi-Timeframe Context
  - Risk Compression
---

# ZONE-AF-0004 — Fractal Multi-Timeframe Zone Architecture

## 1. Core Thesis

The same zone logic must be observed across multiple timeframes.

The system should not assume that a reversal potential on a higher timeframe is automatically a direct execution opportunity. A broad parent zone may identify the meaningful area, but the actual trade often requires a lower-timeframe child zone with a clearer entry and stop.

```text
Higher timeframe = where the opportunity may exist
Lower timeframe  = where the risk contract becomes executable
```

---

## 2. Parent Zone

A parent zone is a higher-timeframe area created by mechanical context or structural limitation.

It answers:

```text
Where should the system care?
```

A parent zone may be:

- execution-ready if it has a narrow and stable stop;
- a watch zone if the stop is broad or unclear;
- a context zone if it only defines the environment;
- unsafe if it has no meaningful expiration.

Examples:

- broad F2 reversal potential;
- F3 reversal environment;
- HTF Hook Zone;
- HTF F1 waist-related zone;
- HTF structural/RTV/decision area.

---

## 3. Child Zone

A child zone is a lower-timeframe zone inside, near, or structurally attached to a parent zone.

It answers:

```text
Where can the system actually risk?
```

A child zone should ideally provide:

- narrower stop;
- clearer entry edge;
- better MAE profile;
- lower cost of attempt;
- local confirmation without destroying convexity;
- better limit placement.

---

## 4. Parent/Child Relationship

```yaml
parent_zone_id: ZONE_H1_0042
child_zone_ids:
  - ZONE_M15_0101
  - ZONE_M5_0204
relationship_type: inside | edge_aligned | overlap | derived_from_parent | conflict_refinement
```

The relationship is not purely geometric. A child zone may matter because it is:

- fully inside the parent;
- on the entry edge of the parent;
- on the stop edge of the parent;
- derived from a lower-timeframe hook inside the parent;
- created by the same context at a smaller scale;
- created by a conflicting context that gives a better limit opportunity.

---

## 5. Risk Compression Principle

The purpose of fractality is risk compression.

A broad zone can be meaningful but too expensive. The lower timeframe is used to compress risk:

```text
Broad Parent Potential
  -> Narrow Child Risk Contract
  -> Limit Entry
  -> Open Reward
```

If lower-timeframe refinement does not appear, the parent may remain a watch zone.

---

## 6. Multi-Timeframe States

The system should classify timeframe alignment:

```text
HTF supportive + LTF supportive
HTF supportive + LTF corrective
HTF broad + LTF precise
HTF conflict + LTF reversal
HTF unsafe + LTF attractive but isolated
```

The most attractive state for convex limit trading may not always be simple alignment. Sometimes a higher-timeframe broad potential area plus a lower-timeframe precise child zone creates better asymmetry than full obvious confluence.

---

## 7. Execution Policy

### 7.1 Execution-Ready Parent

If a parent zone itself has:

- clear entry edge;
- clear stop edge;
- narrow enough width;
- strong potential;

then direct parent execution may be allowed.

### 7.2 Broad Parent / Child Required

If parent zone is broad or stop is unclear, lower timeframe is mandatory.

Typical sources:

- F2 symmetry zone;
- F2 reversal zone without stable stop;
- F3 broad environment.

### 7.3 Child Without Parent

A lower-timeframe child zone without higher-timeframe context may still be observed, but it should receive lower confidence unless its own risk/reward is exceptional.

### 7.4 Parent Touched / Child Not Formed

No trade unless the parent itself is execution-ready.

### 7.5 Child Triggered Before Parent Fully Touched

This requires classification:

```text
edge-aligned child
front-run child
invalid child
```

A child zone near the entry edge of the parent may be valid. A child zone that activates too early may not express the parent context.

---

## 8. Multi-Timeframe Example Logic

```text
H1 F2 Broad Watch Zone
  -> no direct stop
  -> wait for M15 Hook Zone inside the area
  -> M15 Hook has stop behind hook
  -> limit entry at M15 entry edge
  -> stop behind M15 hook
  -> open reward toward H1 potential path
```

This converts vague reversal potential into an executable risk contract.

---

## 9. Required Dataset Fields

```yaml
parent_zone_id: string | null
child_zone_id: string | null
parent_timeframe: string
child_timeframe: string
relationship_geometry: inside | edge | overlap | outside
relationship_logic: same_source | source_refinement | conflict_refinement | stop_refinement
parent_source_type: string
child_source_type: string
parent_width_atr: float
child_width_atr: float
risk_compression_ratio: parent_width_atr / child_width_atr
parent_quality_score: float
child_quality_score: float
combined_zone_quality_score: float
```

---

## 10. Main Rule

A zone becomes powerful when the higher timeframe tells the system **where potential exists**, and the lower timeframe tells it **where the cost is small enough to buy that potential**.

