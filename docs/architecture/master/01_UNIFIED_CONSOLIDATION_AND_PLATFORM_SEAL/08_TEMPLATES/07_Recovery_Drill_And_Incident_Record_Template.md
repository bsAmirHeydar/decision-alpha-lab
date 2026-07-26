---
id: UCPS-51CA38E2DF36
title: "Recovery Drill and Incident Record Template"
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
# Recovery Drill and Incident Record Template

## Recovery drill

```yaml
drill_id: <DRILL-ID>
claimed_boundary: <file|package|registry|terminal|remote>
source_snapshot: <digest>
failure_injection: <description>
recovery_steps: []
restored_digests: []
behavior_validation: []
result: <PASS|FAILED|BLOCKED>
```

## Incident

```yaml
incident_id: <INCIDENT-ID>
severity: <P0|P1|P2|P3>
detected_at: <timestamp>
affected_authority: []
containment: []
evidence_preservation: []
root_cause: <finding>
correction: <change>
regression_tests: []
requalification_scope: []
```
