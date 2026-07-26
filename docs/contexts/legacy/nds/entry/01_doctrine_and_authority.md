---
title: NDS Entry Doctrine and Authority
status: normative
version: 1.0.0
---
# NDS Entry Doctrine and Authority

## 1. Core doctrine

NDS structure is evidence. A Setup is an interpretation of that evidence. A Trade Plan is a bounded-risk proposal. A Command is an operational instruction. These objects must never collapse into one boolean signal.

```text
Structure ≠ Setup
Setup ≠ Trade Plan
Trade Plan ≠ Command
Command ≠ Broker Authorization
Broker Authorization ≠ Capital Authorization
```

## 2. Authority hierarchy

The authority chain is:

```text
Hook Canon
→ Zone Canon
→ Entry/Stop/Target Canon
→ Setup Policy
→ Risk Policy
→ Broker Policy
→ Operator/Deployment Authorization
```

A downstream layer may narrow or block an upstream opportunity. It may not rewrite the upstream anatomy.

## 3. Hard rules already available

The current repository establishes that:

- only valid Hook families are primary Hook-zone sources;
- Hook-after-Hook and Hook-after-opposing-F3 are the principal valid families;
- Hook validity precedes Zone validity;
- a Zone is a risk contract, not a decorative rectangle;
- broad Zones may require lower-timeframe child refinement;
- the system values convexity and open reward more than raw pattern frequency;
- Hook and Zone detection must remain causal and auditable.

## 4. Open doctrine

The current questionnaire has not yet locked:

- exact Zone source points;
- exact upper/lower boundary construction;
- entry edge policy;
- stop/death policy;
- target policy;
- activation, consumption, invalidation, and expiry;
- Hook-direction-to-trade-direction mapping;
- family priority and quality thresholds;
- multi-timeframe conflict resolution.

The implementation therefore exposes these as explicit profiles, enums, lock flags, and adapter seams. It does not bury an assumption in price arithmetic.

## 5. Required separation of state

Every event must be reconstructable through separate records:

```text
NDSStructureRow
NDSZoneRow
NDSSetupRow
NDSTradePlanRow
NDSCommandPreviewRow
```

This allows a reviewer to answer:

- Which exact Hook generated the opportunity?
- Which Zone contract was used?
- Why was the Setup ready or blocked?
- Which entry, stop, and target model were selected?
- Which command would have been produced?
- Why was sending still forbidden?

## 6. Failure policy

Unresolved or missing information must produce a named block reason. It must never fall back to a generic trading heuristic.

Examples:

```text
NDS_ZONE_BLOCKED_PRE_CANON_PROFILE
NDS_SETUP_BLOCKED_DIRECTION_POLICY
NDS_SETUP_BLOCKED_ORDER_MODEL
NDS_TRADE_PLAN_BLOCKED_DIRECTIONAL_GEOMETRY
NDS_COMMAND_BLOCKED_PREVIEW_LOCK_DISABLED
```
