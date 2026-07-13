---
id: AIEOS-TOOLS-README
title: "Vault Tools"
type: guide
status: active
domain: tooling
version: 1.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - tooling
---
# Vault Tools

## Validate the Vault

```powershell
python .\tools\validate_vault.py .
```

The validator checks frontmatter, unique IDs, internal wiki links, empty notes, and probable unresolved placeholders.

## Create a Patch Packet

```powershell
python .\tools\new_patch_packet.py DIV-EXT-001 "Consumed Extreme State" .\work
```

The command creates a bounded work folder containing specification, AI context, patch manifest, test matrix, review, release checklist, engineering log, and execution README.
