---
id: UCPS-B9D37333A95D
title: "Architecture Decision and Waiver Template"
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
# Architecture Decision and Waiver Template

## ADR

```yaml
adr_id: <ADR-ID>
status: <proposed|accepted|superseded>
context: <problem and constraints>
decision: <chosen architecture>
alternatives: []
consequences: []
migration_required: true
security_review: <reference>
```

## Waiver

```yaml
waiver_id: <WAIVER-ID>
scope: <exact paths or controls>
reason: <why compliance is temporarily impossible>
risk: <bounded risk>
owner: <role>
expiry: <date or exit condition>
compensating_controls: []
removal_plan: <action>
```

A waiver cannot authorize unknown consumers, live authority or unpreserved deletion.
