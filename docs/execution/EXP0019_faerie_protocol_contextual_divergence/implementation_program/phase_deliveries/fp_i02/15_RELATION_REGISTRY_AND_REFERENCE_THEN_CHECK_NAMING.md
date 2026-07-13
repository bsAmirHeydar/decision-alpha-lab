---
title: "FP-I02 — Relation Registry and Reference-Then-Check Naming"
tags: [exp0019, faerie-protocol, fp-i02, contracts, obsidian]
status: normative
phase: FP-I02
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Relation Registry and Reference-Then-Check Naming

## Purpose

The relation registry contains exactly seven descriptors. The first letter is the reference window; the second is the check window. WW is both tradeable and the directional gate, and is not gated by itself.

## Normative invariants

1. **Registry is closed to AL/AN/LN/NA/NL/NN/WW.**
2. **Relation code letters match descriptor kinds.**
3. **NA/NL/NN use exact prior calendar offsets.**
4. **WW uses previous completed and current NY weeks.**
5. **Quota session is explicit.**

## Primary surfaces

- `Relation descriptor fields`
- `Same-day relations`
- `Cross-day N relations`
- `WW descriptor`
- `Registry hash`

## Contract architecture

```text
owner/source decision
        │ authority classification
        ▼
closed enum or immutable record
        │ validation + canonicalization
        ▼
canonical payload hash / compact ID
        │ exact-version registry
        ▼
downstream phase consumer
        │ append-only evidence
        ▼
replay/restart parity
```

## Failure matrix

| Failure | Detection | Required disposition |
|---|---|---|
| Missing required field | constructor/schema validation | reject record; do not default silently |
| Unknown enum/reason/relation | closed registry resolution | fail closed with registered code |
| Non-finite price/value | canonical serializer/contract | reject before identity construction |
| Conflicting payload for same ID | identity ledger | critical identity conflict |
| Illegal lifecycle transition | transition registry | reject transition and preserve evidence |
| Dependency/config version drift | exact hash/version check | BLOCKED until explicit rebaseline |
| Live authority while Q12 open | manifest/config guard | reject live profile |

## Evidence requirements

- Exact schema and object version.
- Canonical SHA-256 and compact identifier.
- Parent/source lineage IDs.
- Semantic configuration and dependency snapshot hashes.
- Registered reason code for every non-normal outcome.
- Fixture or test identifier for acceptance evidence.
- Honest compile/runtime status; static validation is not compilation.

## Executable test obligations

1. Repeat the same input and obtain the same hash and compact ID.
2. Change one behavior-bearing field and prove semantic identity changes.
3. Change one projection-only field and prove semantic signal identity is preserved.
4. Submit one unknown enum/reason/property and prove fail-closed rejection.
5. Attempt one illegal state transition and prove rejection.
6. Verify that no broker/order/position/network/chart-object authority is imported.

## Operational rule

No downstream module may reconstruct omitted semantics from filenames, comments, enum ordinals, chart state, or implementation details. It must consume the exact public contract and registry version.

## Navigation

- [[00_FP_I02_DELIVERY_MOC|FP-I02 Delivery MOC]]
- [[../fp_i01/00_FP_I01_DELIVERY_MOC|FP-I01 Compatibility Handoff]]
- [[../../phases/FP_I02_CONTRACTS_ENUMS_IDENTITY_CONFIGURATION_AND_REASON_CODES|Canonical FP-I02 Phase Specification]]

## Field-level review checklist

- [ ] Is the field semantic, projection, or operational?
- [ ] Is the field included in the correct identity hash?
- [ ] Is its enum/value space closed?
- [ ] Is the field immutable after record construction?
- [ ] Is missingness represented explicitly?
- [ ] Does MQL5 mirror the same meaning and version?
- [ ] Is the source/owner authority classification recorded?
- [ ] Does a negative test reject an invalid value?

## Downstream integration constraints

Later phases may populate these fields but may not rename them, change enum meaning, omit identity-bearing axes, or add hidden defaults. A semantic change requires a new public version, migration rule, golden vector, registry hash, and downstream rebaseline.

## Residual risk

The record contract can be correct while the future producer is wrong. FP-I03 through FP-I09 must separately prove time conversion, data coverage, references, hunt ordering, confirmation, WW resolution, and quota arbitration. FP-I02 only makes those future claims explicit and testable.
