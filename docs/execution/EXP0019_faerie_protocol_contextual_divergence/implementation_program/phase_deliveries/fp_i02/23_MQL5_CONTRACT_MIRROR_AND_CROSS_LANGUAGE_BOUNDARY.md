---
title: "FP-I02 — MQL5 Contract Mirror and Cross-Language Boundary"
tags: [exp0019, faerie-protocol, fp-i02, contracts, obsidian]
status: normative
phase: FP-I02
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# MQL5 Contract Mirror and Cross-Language Boundary

## Purpose

Eleven MQL5 headers mirror enums, reasons, relations, types, config, identity, state transitions, validation, and self-test behavior. The mirror is read-only and does not calculate market semantics.

## Normative invariants

1. **Relation/reason counts match Python.**
2. **MQL5 has no order, broker, chart-object, or network authority.**
3. **Cryptographic IDs use SHA-256 helper.**
4. **MetaEditor compile remains a separate local gate.**

## Primary surfaces

- `FP_I02_All.mqh`
- `Contract self-test EA`
- `Diagnostic EA`
- `Static parity checks`
- `Compile logs`

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
