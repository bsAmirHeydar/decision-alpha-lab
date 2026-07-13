---
title: "FP-I01 — Dependency Pinning and Version Resolution"
tags: [exp0019, faerie-protocol, fp-i01, compatibility, adapter-contracts]
status: normative
phase: FP-I01
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Dependency Pinning and Version Resolution

## Purpose

Nineteen shared dependency groups are pinned by exact aggregate SHA-256 and file count. A mismatch blocks initialization and requires an explicit rebaseline.

## Pin construction

The aggregate hash is computed from an ordered list of `{relative_path, file_sha256, size_bytes}` records. The aggregate is therefore sensitive to file content, path, presence, and count. Renaming, adding, deleting, or editing any selected source file invalidates the pin.

## Rebaseline rule

A hash mismatch is not repaired by updating the expected hash in isolation. The owner must review source changes, rerun previous-context tests, regenerate FP-I00 baseline evidence, update the compatibility matrix, and issue a new phase version.

## Normative contract

- The source context remains the semantic owner of its snapshot.
- The adapter is a pure projection and has no mutation, storage, drawing, trading, or network authority.
- Every behavior-bearing field used by the projection is declared in the adapter registry.
- Every output retains `source_context`, `source_type`, and `source_fingerprint`.
- Unknown versions, missing fields, invalid enum values, or dependency hash mismatch fail closed.

## Data flow

```text
hash-pinned source module
        │
        ▼
immutable source snapshot
        │ validate exact fields
        ▼
versioned adapter function
        │ canonical projection
        ▼
neutral compatibility snapshot
        │ evidence hash + reason code
        ▼
FP-I02 or later consumer
```

## Required evidence

| Evidence | Requirement |
|---|---|
| Dependency identity | exact file count and aggregate SHA-256 |
| Source identity | canonical fingerprint before adaptation |
| Mutation proof | fingerprint and deep value unchanged afterward |
| Output identity | canonical output hash |
| Determinism | repeated output hash is identical |
| Health | READY, DEGRADED, or BLOCKED with reason code |
| Authority | broker/order/position/network flags are false |
| Version | exact adapter ID and semantic version |

## Failure matrix

| Failure | Detection | Disposition |
|---|---|---|
| Shared file changed | aggregate hash mismatch | block adapter availability and rebaseline explicitly |
| Missing source field | contract validation | reject source payload; do not manufacture defaults |
| Unknown adapter key | exact registry resolution | hard failure |
| Source mutation | before/after hash or deep equality | phase blocker |
| Repeated output changes | differential fixture | phase blocker |
| Previous-context compile fails | MetaEditor log | stop acceptance |
| Forbidden authority token | boundary scanner | phase blocker |
| Incomplete data | source readiness/status | DEGRADED or BLOCKED; never READY |

## Test obligations

1. Positive golden fixture produces the expected neutral output hash.
2. The same fixture is adapted twice with identical output.
3. Source payload remains byte/semantic equivalent.
4. One required-field deletion fails closed.
5. One expected dependency hash mutation is rejected.
6. Static scan finds no duplicate time logic or runtime authority.
7. MQL5 self-test and diagnostic compile locally.
8. Previous-context entry points compile without source changes.

## Operational checklist

- [ ] Confirm FP-I00 baseline and source-control evidence are present.
- [ ] Run dependency hash verification before any adapter test.
- [ ] Inspect every WARN/FAIL reason; do not waive by prose.
- [ ] Run Python tests and static MQL5 checks.
- [ ] Run MetaEditor compilation on Windows and retain logs.
- [ ] Confirm the patch index contains no EXP0017/EXP0018 shared-core path.
- [ ] Confirm FP-DEC-012 remains open and execution authority remains disabled.

## Residual risk

Python fixtures prove projection determinism and hash guards prove source immutability in the repository snapshot. They do not replace MetaEditor compilation or runtime execution of previous-context diagnostics. A parallel or alternate adapter implementation requires its own parity evidence and exact-version registration.

## Related code

- `lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01/python/fp_i01_compatibility`
- `mql5/Include/FaerieProtocol/EXP0019/Compatibility`
- `lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01/artifacts`

## Navigation

- [[00_FP_I01_DELIVERY_MOC|FP-I01 Delivery MOC]]
- [[../fp_i00/00_FP_I00_DELIVERY_MOC|FP-I00 Governance Baseline]]
- [[../../phases/FP_I02_CORE_CONTEXT_TYPES_IDENTITY_AND_REASON_CODE_KERNEL|FP-I02 Handoff]]
