---
id: SAED-D5F45733BA
title: "Template — Trainer Task Graph"
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
  - trainer
---

# Template — Trainer Task Graph

```yaml
task_graph_id: <id>
upstream_dataset: <manifest-hash>
tasks:
  eligibility:
    target: net_utility_above_hurdle
    trainers: [logistic, boosted_tree]
    calibration: platt
  fill:
    target: fill_before_expiry
    trainers: [logistic, survival]
  outcome_distribution:
    targets: [net_r_q10, net_r_q50, net_r_q90, mae, mfe]
  ranking:
    group_key: opportunity_cluster_id
    candidates_include_skip: true
  novelty:
    action_on_ood: fallback_manual_or_skip
composition:
  use_oof_upstream_predictions: true
  selector: bounded_treatment_selector
```
