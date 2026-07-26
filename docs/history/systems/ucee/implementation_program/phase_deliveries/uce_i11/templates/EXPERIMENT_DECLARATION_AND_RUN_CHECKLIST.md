---
title: "UCE-I11 Experiment Declaration and Run Checklist"
tags: [uce-i11, template, experiment]
status: template
---
# UCE-I11 Experiment Declaration and Run Checklist

## Declaration freeze

- [ ] Dataset manifest ID and SHA-256 recorded.
- [ ] Split, transform, target, economics, and known-time policy hashes recorded.
- [ ] UCE-I10 candidate admission evidence imported without reinterpretation.
- [ ] At least one admitted baseline exists when baseline-first is enabled.
- [ ] Rejected candidates are listed as evidence-only.
- [ ] Fold IDs and seed set are unique and frozen.
- [ ] Search adapter exact key/version is frozen.
- [ ] Every search parameter is behavior-changing and identity-bearing.
- [ ] Objective direction, weight, and constraints are frozen.
- [ ] Protected final-test role is absent from requested roles.

## Budget freeze

- [ ] Total and per-candidate trial caps set.
- [ ] Total and per-trial wall-clock caps set.
- [ ] Memory and CPU/GPU slot ceilings set.
- [ ] Retry cap set.
- [ ] Artifact retention limit set.
- [ ] Seed, fold, and candidate caps set.
- [ ] Budget policy hash captured before compilation.

## Compile verification

- [ ] Compile declaration twice.
- [ ] Manifest hashes match.
- [ ] Trial IDs and ordering match.
- [ ] Declared trial count equals emitted trial count.
- [ ] Rejected candidates have no trainer/trial nodes.
- [ ] All edges reference existing nodes.
- [ ] Topological validation passes.
- [ ] Resource claim exists for every trial.

## Execution verification

- [ ] Environment capture recorded.
- [ ] Ready queue uses deterministic `(priority, node_id)` ordering.
- [ ] Worker IDs are attempt-scoped.
- [ ] Retry/cancel/timeout/quarantine behavior tested.
- [ ] Cache hits and refusals are events and ledger entries.
- [ ] Resume snapshot contains only succeeded/cached nodes.
- [ ] Failed descendants are skipped explicitly.

## Completion verification

- [ ] Selection ledger chain verifies.
- [ ] Every report model is selected or ensembled in ledger.
- [ ] Declared and executed trial counts reconcile.
- [ ] Selected trial set reproduces.
- [ ] Event stream hash reproduces.
- [ ] Artifacts match hash or declared tolerance.
- [ ] UCE-I11 QA, manifest, hashes, status, and handoff are attached.
- [ ] MetaEditor status is reported as actual compile or pending; never inferred.
