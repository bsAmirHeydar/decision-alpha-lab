---
type: implementation-phase
phase: 09
product: gartal terminal
status: planned
language: en
---

# Phase 09 — Packaging, Licensing & Distribution

## Objective

Prepare `gartal terminal` for commercial distribution with a clean release package, license hook points, customer documentation, and predictable versioning.

## Commercial Build Structure

```text
gartal_terminal_release_vX.Y.Z/
├── GartalTerminal.ex5
├── docs/
│   ├── Quick_Start.pdf or md
│   ├── WebRequest_Setup.md
│   ├── Inputs_Reference.md
│   └── Troubleshooting.md
├── license/
│   └── license_readme.md
└── changelog.md
```

## Licensing Doctrine

Licensing must be isolated and optional during development. The indicator should support a license layer without mixing license checks into parser, UI, or alert modules.

Recommended split:

| Layer | Responsibility |
|---|---|
| License adapter | validate license state |
| Product runtime | disable/enable premium features based on license result |
| UI | show license status only |
| Packager | include release docs and correct build files |

## Feature Gates

Potential paid feature gates:

- live source adapter
- dashboard full mode
- alert channels beyond popup
- multi-day forward range
- breaking event channel
- cache/failover tools
- premium color themes
- symbol auto-filter presets

## Implementation Tasks

- [ ] Add version constant.
- [ ] Add license status enum.
- [ ] Add license adapter placeholder.
- [ ] Add dashboard license badge.
- [ ] Add release packaging script update.
- [ ] Add customer quick-start docs.
- [ ] Add WebRequest setup guide.
- [ ] Add changelog update process.
- [ ] Add beta build naming convention.
- [ ] Add release checklist.

## Release Versioning

| Version | Meaning |
|---|---|
| `0.1.x` | internal architecture and sample mode |
| `0.2.x` | dashboard/timeline alpha |
| `0.3.x` | live source adapter alpha |
| `0.5.x` | alert/cache beta |
| `1.0.0` | first commercial release |

## Acceptance Criteria

- One PowerShell command creates a clean release directory.
- Development files are excluded from customer release.
- Version appears in dashboard footer or about panel.
- License state can be shown without affecting compile.
- Customer docs explain WebRequest setup and GMT configuration.

## Failure Modes

| Failure | Control |
|---|---|
| License code pollutes core logic | license adapter only returns status |
| Customer receives source files accidentally | packaging whitelist |
| Wrong version in release | single version constant |
| Support burden from WebRequest setup | clear setup guide and dashboard diagnostic |

## Next

- [[10_validation_qa_release_gate|Phase 10 — Validation, QA & Release Gate]]
