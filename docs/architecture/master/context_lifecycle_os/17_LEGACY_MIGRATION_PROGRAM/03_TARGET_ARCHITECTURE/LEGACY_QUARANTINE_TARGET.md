---
title: "Legacy Quarantine Target"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Legacy Quarantine Target

Quarantine is outside active `mql5` compile and include paths:

```text
lab/11_strategy_factory/migration/quarantine/<family>/<snapshot_id>/
  original/
  manifest.json
  hashes.sha256
  replacement_mapping.yaml
  parity_report.json
  rollback.md
  delete_eligibility.yaml
```

Quarantine preserves original bytes and provenance while preventing accidental runtime inclusion. It is not a dumping ground: every quarantined artifact has a canonical successor or an explicit archive-only decision.
