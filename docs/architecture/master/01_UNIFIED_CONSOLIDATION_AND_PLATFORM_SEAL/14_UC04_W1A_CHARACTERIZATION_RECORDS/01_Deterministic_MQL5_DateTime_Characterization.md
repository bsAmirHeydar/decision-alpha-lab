---
id: UCPS-8B5C043E1A72
title: "UC04-W1A Deterministic MQL5 DateTime Characterization"
type: execution-record
status: accepted-with-blocker
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-27
updated: 2026-07-27
tags:
  - consolidation
  - uc04
  - w1a
  - mql5
  - characterization
---
# UC04-W1A Deterministic MQL5 DateTime Characterization

## Decision

UC04-W1A is accepted as a **characterization-only** delivery. Production shared-engine materialization and consumer cutover remain blocked until native MetaEditor and runtime evidence is captured on the local Windows/MetaTrader 5 environment.

This boundary follows the accepted W0 registration, which grants characterization authority but explicitly withholds implementation and cutover authority.

## Selected candidate

- Candidate: `ENGCAND_5F87C4D5849C4FD141DDBF29590235D8`
- Proposed engine identity: `ENG_9599AA665C5BC4B13B020EBA4213CB16`
- Capability: deterministic MQL5 `datetime` serialization
- Exact output contract: `YYYY.MM.DD HH:MM:SS`
- Precision: second
- Locale: fixed ASCII digits and separators
- Time acquisition: none
- Timezone conversion: none
- Side effects: none

The historical LCM cluster contains ten exact helper implementations across two Debug experts and eight Execution experts. Their accepted source hashes remain unchanged. The cluster has forty-one active call sites and one exact function body.

## Delivered evidence

1. exact ten-member inventory and source digest freeze;
2. frozen formatting contract;
3. thirteen byte-exact boundary and calendar fixtures;
4. test-only reference implementation under `mql5/Tests/`;
5. native MQL5 self-test producing a CSV receipt in MT5 Common Files;
6. static equivalence and metamorphic verification;
7. isolated MetaEditor capture harness that compiles a mirrored MQL5 workspace rather than tracked sources;
8. bounded cutover and rollback plan;
9. blocked logic-preservation certificate;
10. capability migration ledger row and W1A exit decision.

## Native acceptance boundary

Native compile and runtime execution were not claimed in the repository build environment. The required local evidence is:

- all ten unchanged consumers plus the self-test compile with zero errors and zero warnings;
- the self-test produces thirteen PASS rows and one PASS summary;
- source, log and EX5 hashes are captured in `.alpha/runs/uc04w1/native_acceptance/`;
- an independent review records that no semantic, execution, order or capital authority was introduced.

The capture tool is `tools/consolidation/uc04w1/capture_native_acceptance.ps1`.

## Explicitly untouched

- the ten candidate consumer source files;
- all Entry, Treatment, Execution, Stop, Target and Risk rules;
- Context, feature, label, task, model and Train Engine semantics;
- production MQL5 include topology;
- legacy helper deletion;
- order and capital authority.

## Handoff

The next delivery is `UC04-W1B_NATIVE_QUALIFICATION_AND_BOUNDED_CUTOVER`. It may begin only after native evidence is captured and reviewed. The bounded implementation will add one production include, preserve each existing helper name as a wrapper, cut over the ten registered consumers, prove differential parity and retain immediate rollback.

## Evidence links

- `registry/consolidation/uc04/w1/entry_decision.json`
- `registry/consolidation/uc04/w1/candidate_inventory.json`
- `registry/consolidation/uc04/w1/format_contract.json`
- `registry/consolidation/uc04/w1/fixture_corpus.json`
- `registry/consolidation/uc04/w1/reference_design.json`
- `registry/consolidation/uc04/w1/static_equivalence_record.json`
- `registry/consolidation/uc04/w1/native_acceptance_plan.json`
- `registry/consolidation/uc04/w1/logic_preservation_certificate.json`
- `registry/consolidation/uc04/w1/w1a_exit_decision.json`

## Navigation

- [[01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/14_UC04_W1A_CHARACTERIZATION_RECORDS/00_MOC|W1A records MOC]]
- [[01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/09_STATUS_AND_CONTROL/01_Current_Program_Status|Program status foundation]]
