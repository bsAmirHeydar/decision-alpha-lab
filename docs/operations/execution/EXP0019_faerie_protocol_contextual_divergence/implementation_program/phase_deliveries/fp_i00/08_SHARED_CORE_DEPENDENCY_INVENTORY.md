---
title: "FP-I00 — Shared-Core Dependency Inventory"
tags: [exp0019, faerie-protocol, fp-i00, governance, obsidian]
status: implemented
experiment: EXP0019
context_id: FP-CONTEXT-001
phase_id: FP-I00
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Shared-Core Dependency Inventory

## Purpose

Nineteen dependency records pin the existing reusable cores by exact file set and aggregate SHA-256.

## Normative scope

- Inventory EXP0017 CGT/CGR/CGH/CGD/CGC/CGV/CGX surfaces.
- Inventory EXP0018 time, data, period, relationship, hunt, confirmation, lifecycle, render, replay, and session-box surfaces.
- Inventory Strategy Factory Market, Economics, Paper Execution, and Live Safety surfaces.

## Non-bypassable invariants

1. **Every dependency has one semantic owner.**
2. **`mutation_allowed=false` for FP-I00.**
3. **Hash-pinned components without explicit SemVer use `HASH_PINNED` as the exact version mechanism.**


## Deterministic control flow

```text
accepted upstream contract
        │
        ▼
closed policy/configuration
        │
        ▼
canonical scanner or validator
        │
        ├─ PASS → content-addressed evidence
        └─ FAIL → stable reason code + BLOCKED health
        │
        ▼
append-only phase handoff evidence
```

## Required evidence

| Evidence | Required content | Failure disposition |
|---|---|---|
| Identity | exact phase/context/version and SHA-256 | block on omission or mismatch |
| Authority | explicit false values for runtime authority | block on any positive/unknown authority |
| Source | filename, size where available, and frozen SHA-256 | block on mismatch |
| Decisions | exact decision set, status, policy, and open IDs | block on hidden default |
| Dependencies | owner, path, file count, version/hash, reuse class | block on missing dependency |
| Tests | exact context, test ID, path, type, and command | block when undiscoverable |
| Ownership | path prefix, phase owner, mutation and rollback policy | block on overlap or wrong owner |

## Edge cases

### Archive delivery without `.git`

The source-control snapshot reports `ARCHIVE_OR_NON_GIT`, `git_available=false`, and unknown branch/HEAD. It does not fabricate a commit. The local operator regenerates the baseline after extraction in the real repository.

### Patch files make the tree dirty

Raw `git clean` may be false. The harness separately calculates `phase_clean` by excluding explicitly owned FP-I00 prefixes. Unrelated changes remain visible and require review.

### Hash-pinned module without SemVer

When a component exposes no canonical version constants, the aggregate ordered file hash is the exact version and the textual version is `HASH_PINNED`.

### Missing previous-context executable environment

FP-I00 requires test entry-point discoverability. Actual MetaEditor compilation and differential execution become mandatory in FP-I01. The distinction is explicit in the test inventory.

## Failure behavior

- Missing input: return a stable error and keep phase `BLOCKED`.
- Malformed JSON/CSV/hash row: reject the contract; do not normalize silently.
- Duplicate ID: stop before manifest generation.
- Dependency drift: generate a semantic diff and require reviewed rebaseline.
- Authority leakage: block immediately, even if no order was sent.
- Manifest tampering: reject when the embedded hash differs from canonical content.

## Test obligations

1. Repeat the same input and prove identical evidence hash.
2. Change one behavior-bearing field and prove identity changes.
3. Inject at least one invalid/missing input and assert the exact reason code.
4. Confirm the phase owns no MQL5 runtime path.
5. Confirm FP-DEC-012 remains the only open decision.
6. Confirm EXP0017 and EXP0018 compatibility entry points remain discoverable.

## Operator review checklist

- [ ] Run the phase PowerShell check from repository root.
- [ ] Inspect `health`, errors, warnings, and evidence hash.
- [ ] Inspect `source_control.unrelated_changed_paths`.
- [ ] Confirm all dependency roots and aggregate hashes are populated.
- [ ] Confirm no runtime Faerie Protocol path exists.
- [ ] Confirm only the phase file index is staged.
- [ ] Preserve the accepted evidence for FP-I01.

## Code surfaces

- `fp_i00_governance/canonical.py`
- `fp_i00_governance/models.py`
- `fp_i00_governance/git_capture.py`
- `fp_i00_governance/scanner.py`
- `fp_i00_governance/source_verify.py`
- `fp_i00_governance/manifest.py`
- `fp_i00_governance/validator.py`
- `fp_i00_governance/reporting.py`
- `fp_i00_governance/baseline_diff.py`
- `fp_i00_governance/cli.py`

## Handoff constraint

FP-I01 may consume this evidence but may not rewrite it. A changed source, decision, registry, dependency, or ownership contract requires an explicit FP-I00 rebaseline and new phase version.

## Navigation

- [[00_FP_I00_DELIVERY_MOC|FP-I00 Delivery MOC]]
- [[../../phases/FP_I00_GOVERNANCE_BASELINE_FREEZE_AND_SOURCE-CONTROL_HARNESS|Canonical FP-I00 plan]]
- [[../../phases/FP_I01_SHARED-CORE_COMPATIBILITY_HARNESS_AND_ADAPTER_CONTRACTS|FP-I01 handoff]]
