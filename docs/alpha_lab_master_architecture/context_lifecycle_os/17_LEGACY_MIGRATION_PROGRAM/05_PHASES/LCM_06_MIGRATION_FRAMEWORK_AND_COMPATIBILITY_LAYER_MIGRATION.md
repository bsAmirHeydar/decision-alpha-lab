---
title: "LCM-06 — Migration Framework and Compatibility Layer"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-06, implementation-phase]
phase_id: LCM-06
claim_ceiling: MIGRATION_FRAMEWORK_REFERENCE_ONLY
framework_run_id: FRAMEWORK_066C5FA5795AA4C283B17271E4478751
---
# LCM-06 — Migration Framework and Compatibility Layer

## Decision

LCM-06 is implemented as a reference-only migration framework bound to topology `TOPOLOGY_F28766C555330F0B89CC662DA8129220`. It supplies deterministic validation and compatibility tools, but performs no migration operation.

## Architecture

```text
LCM05_TO_LCM06
  → upstream integrity gateway
  → phase authority permit
  → closed registries and contracts
  → migration packet validation
  → alias and locator resolution
  → trace normalization and comparison
  → compatibility adapter contracts
  → move-only and redirect previews
  → quarantine and deletion validation
  → event ledger and provenance
  → atomic publication
  → LCM06_TO_LCM07
```

## Reference evidence

- Framework run: `FRAMEWORK_066C5FA5795AA4C283B17271E4478751`
- Five migration packet fixtures
- Three alias resolution cases
- Three trace comparisons: PASS, SOFT_MISMATCH and HARD_MISMATCH
- Four adapter contract classes
- One move-only plan preview
- Three redirect previews
- Two quarantine evaluations
- Two deletion evaluations
- Twenty machine policies
- Twenty-six Draft 2020-12 schemas

## Acceptance

`REFERENCE_FRAMEWORK_ACCEPTED_NO_MIGRATION_EXECUTED`

## Hard boundary

The phase does not move, delete, merge, refactor, materialize, cut over or execute any legacy artifact. LCM-07 may discover shared-engine candidates and build equivalence evidence, but extraction remains unauthorized until its own gates pass.

## Related

- [[MIGRATION_FRAMEWORK_ARCHITECTURE]]
- [[MIGRATION_PACKET_VALIDATION]]
- [[TRACE_NORMALIZATION_AND_COMPARISON]]
- [[LCM06_SECURITY_AND_AUTHORITY_MODEL]]
