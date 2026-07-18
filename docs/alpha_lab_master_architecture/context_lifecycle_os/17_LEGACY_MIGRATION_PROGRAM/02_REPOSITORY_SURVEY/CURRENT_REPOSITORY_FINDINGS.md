---
title: "Current Repository Findings"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Current Repository Findings

## Survey method

The entire repository was inventoried by file metadata. Every MQL5/MQH source was content-scanned for include edges and risk-bearing API patterns. Authoritative ACL-OS documents and representative domain specifications were read to establish authority and target boundaries. The survey is structural and forensic; pattern hits are triage signals, not proof of execution behavior.

## Repository scale

| Measure | Observed count |
|---|---:|
| Total files | 38,525 |
| Markdown files | 23,737 |
| Python files | 4,421 |
| MQL5/MQH sources | 2,457 |
| `.mq5` files | 288 |
| `.mqh` files | 2,169 |
| Root-level files | 1,069 |
| Exact duplicate MQL source groups | 1 |

## Principal findings

1. The ACL-OS kernel and templates already provide the destination contract under `lab/11_strategy_factory/acl_os` and `lab/11_strategy_factory/contexts/_acl_02_template`.
2. Domain behavior remains distributed across `mql5/Experts`, `mql5/Include`, `docs/execution`, Hook/NDS/Zone documentation and M-series modules.
3. The root contains 1,069 files. Only 7 were classified as canonical root controls by the initial survey. 484 are release-metadata candidates, 54 are installer-script candidates and 9 are commit-record candidates.
4. Three documentation namespace pairs are byte-identical duplicates: `docs/ai_algorithm_engineering_os`, `docs/strategy_factory` and `docs/strategy_factory_v2` each duplicate a corresponding namespace under `docs/alpha_lab_master_architecture`.
5. `docs/strategy_factory_universal_context_exploitation_engine` is a superset of the master-architecture copy and cannot be deleted as a duplicate without reconciliation.
6. The only exact duplicate MQL source pair found is the Astro fractal oscillator under both `mql5/Indicators` and `mql5/Indicators/Research`. Exact duplication is rare; structural and semantic duplication require behavioral proof.
7. FlagCounting/NDS/Hook/Zone is the largest high-risk domain cluster in the initial source survey, with 226 MQL sources and approximately 58,065 source lines.
8. Parallel platform namespaces (`AlphaLab`, `DecisionAlphaLab`, `StrategyFactory`) exist in MQL5. They must be classified as canonical, static mirror, compatibility layer or obsolete before consolidation.

## Survey artifacts

Machine-readable survey files are stored under:

`lab/11_strategy_factory/migration/surveys/reference_2026_07_18/`

They include the full MQL source inventory, include edges, family summary, documentation namespace inventory, root-file classification and exact duplicate report.

## Interpretation boundary

A pattern hit for an order, drawing, timer, file or timeframe API only raises migration risk. It does not prove that the path is active, reachable or authorized. Reachability and runtime behavior are established in LCM-03 and LCM-04.
