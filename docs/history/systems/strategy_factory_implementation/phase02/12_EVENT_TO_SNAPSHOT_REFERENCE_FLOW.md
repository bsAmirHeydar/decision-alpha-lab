# Event-to-Snapshot Reference Flow

```text
OnTick / OnTimer
→ AnatomyProvider.Process
→ Pop canonical AnatomyEvent
→ Validate event and stable ID
→ ResultSink.WriteEvent
→ FeatureProvider.BuildSnapshot
→ Validate causal feature times and stable ID
→ ResultSink.WriteSnapshot
→ Publish bounded audit records
```

Phase 02 intentionally ends at the snapshot. Candidate creation begins only after the candidate contracts and policy kernel are implemented.
