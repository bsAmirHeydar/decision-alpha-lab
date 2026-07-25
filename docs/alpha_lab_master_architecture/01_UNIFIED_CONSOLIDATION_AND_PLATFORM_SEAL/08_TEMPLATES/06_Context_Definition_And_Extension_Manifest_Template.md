---
id: UCPS-A3A12E121A67
title: "Context Definition and Extension Manifest Template"
type: template
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Context Definition and Extension Manifest Template

## Context definition skeleton

```yaml
identity: {}
doctrine: {}
market: {}
clocks: {}
occurrence: {}
data: {}
features: {}
labels: {}
research: {}
treatments: {}
falsification: {}
runtime: {}
authority: {}
```

## Extension manifest skeleton

```yaml
extension_id: <ID>
version: <semver>
type: <detector|feature|label|treatment|model|adapter|visualizer>
owner: <role>
capabilities: []
inputs: []
outputs: []
dependencies: []
failure_semantics: []
security_scope: []
conformance_suite: <path>
```
