---
title: "MQL5 API Reference"
phase: 07
status: canonical
---
# MQL5 API Reference

Primary APIs are CSF07FeatureRegistry.RegisterNode/Compile, CSF07ContextState.BeginGeneration/Put/Get/MarkDirty, CSF07FeatureVectorSchema.Add/ValidateAgainst, CSF07FixedFeatureVector.Build and CSF07ContextEngine.BuildSnapshot.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
