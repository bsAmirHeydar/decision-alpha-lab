---
id: SAED-76A272CC57
title: "Template — Experiment Declaration and Search Budget"
type: template
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - template
  - experiment
---

# Template — Experiment Declaration and Search Budget

```yaml
experiment_id: <id>
hypothesis: <falsifiable statement>
data_roles: <fold-plan-ref>
candidate_universe_hash: <hash>
model_ladder: []
search_spaces: []
budgets:
  max_trials: <n>
  max_seeds: <n>
  max_compute_hours: <n>
  max_feature_revisions: <n>
nulls: []
stresses: []
primary_metrics: []
hard_promotion_gates: []
stopping_rule: <predeclared>
locked_final_test_access: gate_only
```
