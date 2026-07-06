# Alpha Lab Zone Antifragile Patch

This patch adds a detailed English documentation layer for the Zone-Centric Antifragile Trading Architecture.

## Contents

- `00_ZONE_AF_START_HERE.md` — root entrypoint.
- `docs/zone_af/` — canonical English documents.
- `docs/obsidian_zone/` — Obsidian-ready MOCs, concepts, policies, training notes, templates, and canvases.

## Installation

Copy or expand this patch at the root of the Decision Alpha Lab repository.

PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_zone_af_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_zone_af_patch.zip
```

Then open the repository folder as an Obsidian vault and start from:

```text
00_ZONE_AF_START_HERE.md
```

## Commit Message

```text
docs(zone): add zone-centric antifragile alpha architecture

Add English documentation and Obsidian knowledge layer for the zone-centric antifragile trading model.

Includes:
- zone as risk-contract philosophy
- antifragile loss/profit policy
- mechanical zone source taxonomy for Hook, F1, F2, and F3
- fractal multi-timeframe parent/child zone architecture
- limit-entry, stop-expiration, and profit-growth policy
- zone learning objective, dataset contract, and training targets
- internal bot mind architecture
- Obsidian MOC, concept notes, templates, and canvas diagrams

This commit is documentation-only. It does not change trading logic, execution behavior, MQL5 code, Python research code, registry semantics, or production rules.
```
