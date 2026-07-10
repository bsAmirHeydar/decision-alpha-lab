---
title: "Installation and Integration"
type: guide
status: active
version: 1.0.0
created: 2026-07-10
---
# Installation and Integration

## Standalone Obsidian Vault

Open Obsidian, select **Open folder as vault**, and choose `AI_Algorithm_Engineering_OS`.

## Integrate into Quant Lab

Recommended target:

```text
decision-alpha-lab/docs/ai_algorithm_engineering_os/
```

Copy the complete directory. Preserve relative paths because internal links assume the module structure. Run:

```powershell
python .\docsi_algorithm_engineering_os	oolsalidate_vault.py .\docsi_algorithm_engineering_os
```

## Repository Agent Rules

Review this package's `AGENTS.md` against existing repository rules. Merge rather than overwrite. Repository-specific build commands, file restrictions, coding conventions, and domain invariants must remain authoritative.

## Obsidian Settings

Core plugins enabled by the included configuration: backlinks, outgoing links, graph, search, templates, file explorer, and tag pane. Community plugins are not required.

## Validation

Run the validator after moving or renaming notes. A valid vault has unique note IDs, resolvable internal links, frontmatter on normative notes, and no unresolved template placeholders in active documents.
