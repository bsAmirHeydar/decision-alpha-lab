---
id: UCPS-862D117118CB
title: "Artifact Disposition and Relocation Record Template"
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
# Artifact Disposition and Relocation Record Template

```yaml
artifact_id: <stable ID>
old_path: <path>
old_digest: <sha256>
artifact_class: <class>
owner: <role>
consumers: []
disposition: <KEEP_CANONICAL|MOVE|MERGE|GENERATE|EXTERNALIZE|DELETE>
target_path: <path>
semantic_change: false
characterization_evidence: []
consumer_rewrite_receipts: []
recovery_location: <reference>
status: <planned|moved|verified|retired>
```

A record with disposition `DELETE` remains non-authoritative until all deletion gates pass.
