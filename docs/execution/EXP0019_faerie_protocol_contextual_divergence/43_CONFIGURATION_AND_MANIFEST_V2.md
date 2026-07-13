---
title: "43 - Configuration and Manifest v2"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 43 - Configuration and Manifest v2


## Canonical Profile

The canonical manifest is represented by `contracts/fp_context_manifest.v2.example.json`. It must include:

- context ID and semantic version,
- decision-set ID and hash,
- pair descriptor,
- resolved host chart timeframe,
- New York time/session/week definitions,
- calendar-day N lookback policy,
- M1 first-sweep authority,
- strict confirmation deadline policy,
- WW activation/neutralization/recency/tradeability,
- quota scope and arbitration,
- explicit quota-consumption policy (`UNSET` until answered),
- SELL stop spread policy,
- visual reason/style registry versions,
- shared-core and adapter versions,
- data revision and coverage policy.

## Identity-Bearing Fields

| Field | Why identity-bearing |
|---|---|
| resolved confirmation timeframe | Changes which closed candle can confirm and whether it closes before session end. |
| calendar-day lookback depth | Changes historical reference universe. |
| session and week intervals | Changes reference/check ownership. |
| relation registry version | Changes enabled relations and selectors. |
| first-sweep authority | Changes hunter ordering. |
| WW policy | Changes eligibility and direct setups. |
| quota scope/arbitration/consumption | Changes which order may exist. |
| spread policy | Changes stop, size, and economic result. |
| data coverage revision | Changes source facts. |

## Initialization Rules

```text
manifest = resolve(raw_inputs, chart_state, dependency_versions)
validate(manifest)
if manifest.live_execution_enabled and manifest.quota_consumption_policy == UNSET:
    fail initialization
context_epoch_id = sha256(canonical_json(manifest))
```

## Profile Separation

- `CANONICAL_RESEARCH`: detection, drawing, historical/paper outputs; Q12 may be UNSET.
- `CANONICAL_LIVE`: requires all decisions including Q12 and all broker/data checks.
- `NON_CANONICAL_EXPERIMENT`: any override; visually and structurally labelled, never mixed with canonical statistics.

## Authority Classification

| Classification | Meaning |
|---|---|
| `OWNER_CONFIRMED` | Explicitly selected by the owner in the 15-question decision response. |
| `SOURCE_CONFIRMED` | Directly present in the original Faerie Protocol source package or owner narrative. |
| `ARCHITECTURAL_DERIVATION` | Required to make the confirmed behavior deterministic, modular, testable, or compatible with shared cores. |
| `LEGACY_OBSERVATION` | Behavior observed in `FP 101.mq5`; not automatically canonical. |
| `OPEN_DECISION` | Must not be silently hard-coded. |

Canonical priority is: `OWNER_CONFIRMED` > `SOURCE_CONFIRMED` > reviewed `ARCHITECTURAL_DERIVATION` > `LEGACY_OBSERVATION`.

## Navigation

- [[00_EXP0019_MOC|EXP0019 Master MOC]]
- [[38_OWNER_DECISION_FREEZE_V2|Owner Decision Freeze v2]]
- [[33_AMBIGUITY_AND_DECISION_REGISTER|Decision Register]]
- [[40_NORMATIVE_ALGORITHM_SPECIFICATION|Normative Algorithm Specification]]
- [[44_ACCEPTANCE_GATE_FOR_CODING|Acceptance Gate for Coding]]
