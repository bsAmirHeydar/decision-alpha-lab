# UC04-W1A — Deterministic MQL5 DateTime Characterization

This release characterizes the first UC-04 shared-engine candidate without changing production MQL5 consumers.

## Accepted scope

- freezes the exact ten-member historical `*_FormatDateTime` cluster;
- records forty-one active call sites and unchanged source hashes;
- defines the byte-exact `YYYY.MM.DD HH:MM:SS` contract;
- freezes thirteen deterministic fixture vectors;
- adds a test-only reference implementation and MQL5 native self-test;
- adds schema-bound governance, a reproducible verifier and CI;
- adds an isolated Windows MetaEditor capture harness;
- prepares a wrapper-based consumer cutover and rollback plan.

## Authority boundary

Production shared-engine materialization and consumer source changes are not authorized in W1A. Native MetaEditor and MT5 runtime evidence are pending. The logic-preservation certificate remains blocked, and deletion, runtime, order and capital authority are false.

## Verification evidence

- Engineering Policy: PASS;
- UC04-W0 logical foundation verification: PASS;
- UC04-W1A verifier: PASS;
- repository collection: 9,745 tests, zero collection errors;
- consolidation W0/W1 scoped suite: 28 passed;
- native MetaEditor compile: pending local Windows;
- native MT5 self-test: pending local Windows.

The next delivery is `UC04-W1B_NATIVE_QUALIFICATION_AND_BOUNDED_CUTOVER` after native evidence is captured and independently reviewed.
