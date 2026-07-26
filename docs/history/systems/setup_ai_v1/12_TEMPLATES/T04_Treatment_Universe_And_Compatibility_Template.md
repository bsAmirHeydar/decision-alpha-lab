---
id: SAED-5429146C69
title: "Template — Treatment Universe and Compatibility Graph"
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
  - treatment
---

# Template — Treatment Universe and Compatibility Graph

```yaml
universe_id: <id>
context_package_hash: <hash>
registries:
  payoff: <hash>
  entry: <hash>
  stop: <hash>
  exit: <hash>
  management: <hash>
rules:
  - when: {archetype: pullback_continuation, profile: P5}
    allow: {entry: [E3], stop: [tight_trigger], exit: [fixed]}
  - when: {profile: P3}
    require: {path_replay: true, trail_runtime: true}
pruning:
  semantic: true
  geometry: true
  broker: true
  cost: true
  duplicate: true
skip_candidate: required
manual_baseline: required
```
