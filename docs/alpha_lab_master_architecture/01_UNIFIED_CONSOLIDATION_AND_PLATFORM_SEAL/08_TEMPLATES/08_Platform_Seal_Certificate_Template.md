---
id: UCPS-C7085F20EC28
title: "Platform Seal Certificate Template"
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
# Platform Seal Certificate Template

```yaml
seal_id: <SEAL-ID>
repository_commit: <commit>
accepted_topology_digest: <sha256>
final_inventory_digest: <sha256>
acceptance_receipt: <reference>
golden_contexts: []
legacy_consumer_count: 0
compatibility_redirect_count: 0
p0_defects: 0
p1_defects: 0
unknown_required_evidence: 0
recovery_receipt: <reference>
security_approval: <reference>
architecture_approval: <reference>
independent_review: <reference>
issued_at: <timestamp>
```

The certificate is not pre-created with `PASS`. It is issued only from verified evidence.
