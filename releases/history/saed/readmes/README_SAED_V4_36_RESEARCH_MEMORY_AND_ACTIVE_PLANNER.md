# SAED V4-36 — Research Memory and Active Planner

This patch adds the complete V4-36 deterministic reference implementation. It freezes append-only research memory, negative knowledge, evidence and lineage, claims and contradictions, deterministic retrieval, evidence gaps, research budgets, risk findings, value-of-information scoring, protected exploration and replication floors, fail-closed proposal selection, prerequisite-aware schedules, human governance, evidence certificate and bounded V4-37 handoff.

Validation commands:

`python tools/strategy_factory/saed_v4_36/run_saed_v4_36_full_qa.py`

`python tools/strategy_factory/saed_v4_36/validate_saed_v4_36_delivery.py`

The implementation is research-only. It cannot launch experiments, mutate UCEE, select treatments, allocate capital, activate runtime, submit orders or authorize production.
