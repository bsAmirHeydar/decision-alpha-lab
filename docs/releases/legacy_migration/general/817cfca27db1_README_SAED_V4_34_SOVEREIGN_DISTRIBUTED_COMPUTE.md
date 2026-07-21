# SAED V4-34 — Sovereign Distributed Compute

This patch adds the complete V4-34 deterministic reference implementation for sovereign distributed research compute. It is additive and preserves the existing UCEE and MQL5 authority model.

## Included capability

The patch freezes upstream evidence, compute constitution, sovereign domain/node inventories, attestation records, network routes, immutable artifacts, workload DAGs, resource budgets, deterministic partitioning, locality proofs, topological schedules, synthetic execution, checkpoint/recovery, resource/cost/network/exposure accounting, telemetry redaction, distributed provenance, governance reviews, certificate and V4-35 handoff.

## Validation

Run `python tools/strategy_factory/saed_v4_34/run_saed_v4_34_full_qa.py` followed by `python tools/strategy_factory/saed_v4_34/validate_saed_v4_34_delivery.py`.

## Authority

The implementation is research-only. It cannot select treatments, allocate risk, mutate UCEE, submit orders, authorize production or claim real cluster/runtime evidence.
