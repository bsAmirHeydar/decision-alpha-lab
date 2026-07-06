---
type: canonical_policy
id: ZONE-AF-0005
status: draft
language: english
project: Decision Alpha Lab
concepts:
  - Limit Entry
  - Stop Policy
  - Profit Growth
  - Convexity
  - Risk Management
---

# ZONE-AF-0005 — Limit Entry, Risk, and Profit Growth Policy

## 1. Limit Entry Policy

The default execution style of the Zone-Centric Antifragile Engine is limit-based.

Limit entry is justified when:

- the zone has a stable entry edge;
- the stop/expiration edge is known;
- potential is large enough relative to zone width;
- the area is mechanically derived, not visually guessed;
- the system is willing to accept a small bounded loss before confirmation.

Limit entry is not justified when:

- there is no stable stop;
- the zone is only a vague broad reversal area;
- price has already moved away and the trader is chasing;
- confirmation would be required to define the stop;
- the zone is too wide and no child zone exists.

---

## 2. Entry Edge

The entry edge is the first tradable part of the zone where the risk contract begins.

It is not always the exact extreme. The user explicitly clarified:

> Entry is not only the extreme. It is the zone. The zone must have a known start and a known stop.

Therefore, the system must support:

- entry at edge;
- entry inside zone;
- scaled entry across zone;
- child-zone entry inside parent zone.

---

## 3. Stop as Expiration

The stop is the expiration edge of the zone.

Stop types:

```text
behind_hook
behind_f1_waist
behind_child_zone
behind_micro_structure
parent_zone_expiration
context_based_expiration
time_expiration
```

No stable stop means no execution zone.

---

## 4. Wide Zone Policy

If a zone is broad but meaningful:

```text
Do not reject the idea automatically.
Do not execute blindly.
Search for lower-timeframe child zone.
```

If no child zone appears, classify as watch zone.

---

## 5. Confirmation Policy

Confirmation must be evaluated by its effect on convexity.

Good confirmation:

- clarifies zone survival;
- improves stop stability;
- does not greatly increase risk;
- helps avoid dead zones;
- preserves reward potential.

Bad confirmation:

- enters after most reward is already gone;
- doubles or triples risk;
- converts convex trade into ordinary trade;
- satisfies psychology but damages payoff asymmetry.

---

## 6. Profit Growth Policy

The system should not automatically cap reward at a fixed target. It should evaluate whether the zone produced an expansion path worth holding.

Profit management can include:

- partial exit plus runner;
- break-even after displacement;
- structure-based trailing;
- opposite-zone objective;
- path smoothness hold;
- pyramiding only after favorable structure.

---

## 7. Risk/Reward Estimation

Before entry, the system should estimate:

```text
risk = entry_price - stop_price, adjusted for direction, spread, and buffer
potential = estimated open reward path
potential_to_width = potential / zone_width
```

The exact minimum threshold is learnable, but the philosophical requirement is fixed:

> The possible reward must justify the bounded cost.

---

## 8. Good Trade vs Good Zone

A single trade can be a small win while the zone was high-potential. A single trade can be a loss while the zone was statistically valid. Therefore, training should start from zone outcome, not only trade PnL.

Track:

- zone potential realized;
- MFE after touch;
- MAE before expansion;
- whether entry style captured the potential;
- whether management killed the tail;
- whether lower-timeframe refinement would have improved results.

---

## 9. Policy Summary

```text
A zone is tradable only when entry and stop are defined.
A broad potential area requires lower-timeframe refinement.
A small loss is acceptable if it buys access to open reward.
Confirmation is useful only if it does not destroy convexity.
Profit should be allowed to grow when path quality supports it.
```

