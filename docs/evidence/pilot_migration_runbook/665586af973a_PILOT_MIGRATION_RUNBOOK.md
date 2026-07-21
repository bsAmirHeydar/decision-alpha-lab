# Pilot Migration Runbook

1. Verify the LCM-08A handoff digest.
2. Verify `lab/03_experiments/EXP0015_intermarket_time_divergence/experiment.py` equals `sha256:99e5e03a4bf30a2ab94949e2ddc6cdc1d067f0441d25dbe0dc8a138026a9bd2f`.
3. Validate the canonical context contracts.
4. Run all golden cases through the immutable legacy module and canonical adapter.
5. Reject any hard-field mismatch; do not use aggregate parity.
6. Scan the adapter for order and drawing APIs.
7. Confirm no consumer import or command path changed.
8. Publish atomically only after clean-overlay verification.
9. On rollback, remove only indexed LCM-08B paths and restore modified roadmap docs.
