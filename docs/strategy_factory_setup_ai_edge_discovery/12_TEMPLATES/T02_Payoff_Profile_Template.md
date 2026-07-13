---
id: SAED-4EA2F45196
title: "Template — Payoff Profile and Objective"
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
  - payoff-profile
---

# Template — Payoff Profile and Objective

```yaml
profile_id: P<id>
version: 1.0.0
name: <name>
mission: <economic mission>
stop_family: <wide_structural|tight_trigger|...>
exit_family: <fixed|destination|trail|partial_runner>
path_dependence: <low|high>
primary_objectives: []
hard_constraints:
  minimum_net_reward_r: null
  maximum_tail_loss: null
  minimum_clusters: null
  maximum_time_underwater: null
secondary_metrics: []
required_stresses: []
required_models: []
rejection_conditions: []
```
