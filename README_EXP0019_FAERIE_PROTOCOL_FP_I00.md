# EXP0019 Faerie Protocol — FP-I00 Governance, Baseline Freeze, and Source-Control Harness

This delivery implements the first phase of the Faerie Protocol implementation program. It freezes the authoritative source/document/decision baseline and provides executable governance tooling before any runtime context, indicator, diagnostic EA, paper execution, or live execution code is introduced.

## Delivered

- Deterministic canonical JSON and SHA-256 utilities.
- Source-control snapshot capture with phase-owned vs unrelated-change separation.
- External source-package verification against the three frozen source hashes.
- Immutable baseline manifest generation.
- Exact shared-core dependency inventory for EXP0017, EXP0018, Strategy Factory Market, Economics, Execution, and Live.
- Previous-context test discovery inventory.
- File ownership and rollback registry.
- Non-bypassable decision checks, including `FP-DEC-012` live-execution closure.
- Runtime-authority and forbidden-file boundary checks.
- Semantic baseline diff utility.
- PowerShell operator scripts.
- 26 Python tests and detailed Obsidian phase documentation.

## Important boundary

No Faerie Protocol MQL5 runtime module is created in FP-I00. This is intentional and tested. The next phase, FP-I01, introduces compatibility adapters and harnesses while preserving the shared cores.
