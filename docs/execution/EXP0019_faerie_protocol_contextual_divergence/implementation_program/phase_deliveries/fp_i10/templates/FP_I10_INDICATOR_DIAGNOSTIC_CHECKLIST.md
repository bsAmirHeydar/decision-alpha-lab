# FP-I10 Indicator Diagnostic Checklist

- [ ] Exact FP-I03 through FP-I09 versions are present.
- [ ] Runtime authority is `NONE`.
- [ ] Primary and secondary symbols are valid and distinct.
- [ ] Pair ID and configuration hash are visible.
- [ ] Instance ID, namespace, and checkpoint key are unique.
- [ ] Health, lifecycle, data readiness, WW direction, counts, quota, ledger, revision, and heartbeat buffers are readable.
- [ ] Repeated calculation on the same closed minute performs no duplicate work.
- [ ] History shortage reports DEGRADED rather than fabricating evidence.
- [ ] Data conflict reports BLOCKED.
- [ ] Checkpoint mismatch triggers rebuild.
- [ ] No chart objects, alerts, exports, or orders are created in I10.
- [ ] Local MetaEditor compile evidence is attached.
