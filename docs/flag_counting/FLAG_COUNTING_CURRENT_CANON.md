# Flag Counting Current Canon

Status: **active source of truth for Phoenix implementation**.
Scope: docs, code patches, audit, renderer, validation, and future execution modules related to Flag Counting.

This document exists to remove decision drift. If any older Flag Counting document conflicts with this file, this file wins.

---

## 1. Active implementation target

The only active implementation path is Phoenix:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
mql5/Include/FlagCountingPhoenix/
```

Legacy paths are retained only as research history or reference material:

```text
mql5/Experts/M0007/M0007_FlagCountingF1.mq5
mql5/Include/M0007/
FlagCountingVNext*
FlagCountingV6*
```

Do not start new code from M0007, VNext, V6, old checklists, or old sequence contracts.

---

## 2. Canon hierarchy

Use the following hierarchy when implementing or auditing Phoenix:

1. **This file** — final decision source and conflict resolver.
2. `docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md` — semantic sequence contract.
3. `docs/flag_counting/FLAG_COUNTING_ENGINEERING_PACK_V5.md` and `docs/flag_counting/engineering_pack_v5/` — definitions, algorithms, and explanations.
4. `docs/flag_counting/implementation_ladder_v1/` — implementation order, interfaces, acceptance gates, and freeze protocol.
5. `docs/flag_counting/phoenix_rebuild/` — Phoenix-specific repair notes. These are valid only where they do not conflict with this canon.
6. Current Phoenix code under `mql5/Include/FlagCountingPhoenix/` — implementation reality. If code and docs differ, patch docs and code together under the correct ladder level.

Older documents are archived context unless explicitly referenced by this canon.

---

## 3. Non-negotiable invariants

These rules cannot be relaxed by renderer settings or tactical patches:

1. Structural decisions use candle `high` and `low` only.
2. `open`, `close`, candle body, candle color, volume, indicators, and external signals are not structural inputs.
3. Equality is not a break. A level is broken only by strict passage beyond it.
4. Nodes are L-based structural highs/lows with plateau handling.
5. Raw observations must remain auditable even when compressed views are used.
6. A flag body is always `Origin -> Leg1 -> Waist -> Leg2`.
7. F1, F2, and F3 share the same body shape; they differ by lifecycle, authorization, confirmation, invalidation, and terminal behavior.
8. The engine is a stateful sequence system, not a sliding-window pattern scanner.
9. Renderer is non-authoritative. It draws only engine-emitted objects.
10. Main chart and audit output are separate products.
11. Every visible or hidden decision must carry a reason.
12. Given the same bars, inputs, and range, Phoenix must emit deterministic output.
13. Phoenix structural engines must consume the Level 01 canonical closed-bar stream by default. Direct private `CopyRates` calls are not allowed in higher structural modules.
14. Canonical bar indexing is fixed: `rates[0]` is the oldest closed bar, and newer bars have higher indices.

---

## 4. Final resolved decisions

### 4.1 Phase reset

Default phase reset is strict:

```text
PHASE_RESET_OPPOSITE_F3_LOCK_ONLY
```

Meaning:

- Same-direction F1 ownership is not reset by a failed F2/F3 child.
- Same-direction F1 ownership is not reset merely because a new same-direction body appears.
- A completed F3 becomes locked only when a first confirmed opposite F1 appears.
- Broader reset modes may exist only as named diagnostic inputs, never as silent defaults.

Allowed future variants:

```text
PHASE_RESET_OPPOSITE_CONFIRMED_F1
PHASE_RESET_OPPOSITE_HOOK_OR_F1
```

If added, they must be logged in audit and cannot change the meaning of the strict default.

### 4.2 F1 root preference

Root ownership is semantic, not visual.

Default winner order inside the same phase/direction conflict:

1. valid lifecycle status over weaker status;
2. confirmed/qualified over merely developing;
3. Hook/phase-boundary root over fail-open root;
4. completed child chain over single isolated root;
5. lower-L local structure over higher-L umbrella structure when semantic quality is equal;
6. earlier stable origin over later duplicate when semantic quality is equal;
7. deterministic `event_id` as final tie-breaker.

Every losing candidate remains audit-visible with a hidden reason.

### 4.3 Fail-open

Fail-open is diagnostic recovery, not semantic truth.

Default:

- Fail-open may be scanned.
- Fail-open may be main-visible only when no hook-owned canonical root exists in the same phase and it passes the same body/lifecycle rules.
- Fail-open must be explicitly tagged: `from_fail_open=true` and hidden/visible reason must include `fail_open`.

### 4.4 Main-chart visibility

Default main chart is **canonical clean**:

- Show canonical visible F1/F2/F3 structures only.
- F1 may be visible once it has a valid body and has not violated its lifecycle boundary, but it must be tagged as developing until confirmation.
- F2 main visibility requires authorized parent context and size qualification, unless candidate display is explicitly enabled.
- F3 main visibility requires authorized parent context and OR qualification or terminal/completed state, unless candidate display is explicitly enabled.
- Developing, undersized, duplicate, failed, and diagnostic structures remain in audit.

Optional display profiles may expose more detail, but they must not change emitted logical events:

```text
CLEAN_LOCAL
BALANCED
STRUCTURAL_AUDIT
```

### 4.5 High-L versus lower-L ownership

When a higher-L umbrella and a lower-L local structure overlap:

- Main chart chooses the canonical owner using the winner order above.
- Lower-L wins when semantic quality is equal because it gives a more local state reading.
- Higher-L remains audit-visible unless it owns a distinct, non-overlapping phase.
- Renderer must not decide this; the canonicalization/ownership layer decides it.

### 4.6 Pending nodes

Default:

- Pending nodes may support Hook/ND live inspection.
- Confirmed F bodies require confirmed nodes.
- Pending-node F bodies are allowed only in explicit live diagnostic mode and must never be treated as canonical historical truth.

### 4.7 Backfill window

Default strict window:

- F2 origin is backfilled from the deepest adverse correction after F1 Leg2 and before F1 confirmation.
- F3 origin is backfilled from the deepest adverse correction after F2 Leg2 and before F2 confirmation.

Extended post-confirmation backfill may exist only behind a named diagnostic input and must be visible in audit.

### 4.8 F2 size and F3 authorization

Default:

- F2 candidate may exist in audit before size qualification.
- Main-chart F2 requires size qualification unless candidate display is enabled.
- F3 authorization requires confirmed and size-qualified F2.
- If F2 later extends and reaches required size, update the same candidate/Leg2 extension path; do not emit a duplicate child unless identity truly changes.

### 4.9 F3 completion and lock

Default:

- F3 is authorized after confirmed qualified F2.
- F3 completion uses the documented OR rule: parent size ratio or Leg1 L ratio.
- A developing F3 is not rejected merely because the OR condition is not reached yet.
- Once terminal/completed and later locked by opposite confirmed F1, locked F3 never disappears from historical audit/main output.

### 4.10 Hook/ND display

Default:

- Hook/ND is a first-class context layer.
- Main chart shows Hook/ND only when connected to visible canonical ownership or when Hook debug display is enabled.
- Branch numbers belong in audit by default.
- Hook/ND must not starve all F structures.

### 4.11 Audit/export is mandatory

Before renderer is treated as trustworthy, Phoenix must expose:

```text
raw_nodes
scaled_nodes
hooks
raw_events
visible_events
hidden_events
hidden_reason
sequence_transitions
canonical_winners
candidate/qualified/confirmed/invalidated/locked counts
```

CSV/JSON export is the target audit form. Until file export exists, structured log output must expose the same fields.

---

## 4.12 Level 01 candle stream

Default structural input is the Level 01 canonical closed-bar stream:

```text
FP_LoadCanonicalRates -> canonical MqlRates[] -> node/hook/flag engines
```

Default settings:

```text
InpUseClosedBarsOnly = true
InpStrictTimebase = true
InpMinClosedBars = 200
InpPrintTimebaseSanity = true
```

`InpBarsToScan` means requested closed bars in default mode. Phoenix copies one extra raw terminal bar and drops the current forming live candle before detection.

Canonical convention:

```text
rates[0] = oldest closed bar
rates[canonical_bars - 1] = newest closed bar
newer bars have higher indices
time is display metadata, not structural x-axis authority
```

Level 01 must emit an `FP_LEVEL01` sanity line before downstream detection is trusted. If the timebase contract fails under strict mode, Phoenix must stop before node/flag detection.

---


## 4.13 Level 02 node engine

Default structural node path:

```text
Level 01 canonical MqlRates[]
-> FP_BuildCanonicalNodesForScale
-> raw FP_Node[]
-> canonical alternating FP_Node[]
-> Hook/F engines
```

Level 02 is modularized into plateau detection, L-clearance scans, canonicalization, scale-list construction, and node audit. `FP_NodeEngine.mqh` is the facade; higher layers must not duplicate node extraction logic.

Node rules:

- structural inputs are high/low only;
- adjacent equal highs/lows form one plateau candidate;
- plateau anchor is the last equal touch;
- equality is not a break and does not count as L clearance;
- confirmed nodes and live-pending candidates are explicitly tagged;
- canonical nodes are sorted by anchor index and compressed into alternating high/low runs before Hook/F layers consume them.

Default Level 02 audit inputs:

```text
InpPrintNodeSanity = true
InpPrintNodeSamples = false
InpNodeSampleLimit = 6
```

`FP_LEVEL02_RAW` and `FP_LEVEL02_CANONICAL` logs are the current audit form until raw CSV/JSON export is implemented. Renderer output is not accepted as node evidence.

---

## 5. Interface decision

Current Phoenix uses these active shared structs:

```text
FP_Node
FP_InternalPack
FP_HookBranch
FP_FlagEvent
FP_Config
FP_DetectResult
```

The older interface names below are not required active structs:

```text
FP_FlagBody
FP_PhaseState
FP_AuditRecord
```

Their responsibilities are represented by `FP_FlagEvent`, canonical visibility fields, reason strings, and audit/export output. If separate structs are later introduced, they must be added through Level 01/03/11.5 and must not duplicate authority.

---

## 6. Validation policy

Validation has two phases:

1. **Baseline creation**: first accepted validation run records deterministic outputs for pinned chart ranges.
2. **Regression comparison**: later patches compare their output to the baseline and explain any expected change.

Do not fake expected counts without broker/range data. If a count is not yet baselined, mark the case as `baseline_required`, not `passed`.

---

## 7. Patch policy

Every future patch must state:

```text
Highest touched ladder level:
Canon version used: FLAG_COUNTING_CURRENT_CANON.md
Files touched:
Invariant preserved:
Invariant intentionally changed:
Tests/audit evidence:
Known limitations:
```

If a patch conflicts with this canon, update this canon first in a separate governance patch.
