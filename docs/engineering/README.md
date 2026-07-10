---
id: AIEOS2-03768317B0AA
title: "Decision Alpha Lab Engineering Policy Index"
type: index
status: active
domain: engineering
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - engineering
---
# Decision Alpha Lab Engineering Policy Index

This directory is the repository-facing control plane for engineering work. The full modular Obsidian operating system is stored at `docs/ai_algorithm_engineering_os/`.

## Canonical Entry Points

1. [[ALPHA_LAB_ENGINEERING_HANDBOOK|Engineering Handbook]] — complete lifecycle and policy.
2. [[ALPHA_LAB_POLICY_HIERARCHY|Policy Hierarchy]] — what wins when documents conflict.
3. [[ALPHA_LAB_REPOSITORY_CONTRACT|Repository Contract]] — ownership and directory boundaries.
4. [[ALPHA_LAB_CODE_STYLE_STANDARD|Code Style Standard]] — cross-language implementation rules.
5. [[ALPHA_LAB_QUALITY_GATE_MATRIX|Quality Gate Matrix]] — phase-entry and phase-exit evidence.
6. [[ALPHA_LAB_PATCH_RELEASE_STANDARD|Patch and Release Standard]] — ZIP, PowerShell, Git, rollback.
7. [[ALPHA_LAB_AI_AGENT_CONTRACT|AI Agent Contract]] — bounded AI roles and acceptance.
8. [[ALPHA_LAB_MQL5_COMPATIBILITY_STANDARD|MQL5 Compatibility Standard]].
9. [[ALPHA_LAB_PYTHON_RESEARCH_STANDARD|Python Research Standard]].
10. [[ALPHA_LAB_DATA_SCHEMA_STANDARD|Data and Schema Standard]].
11. [[ALPHA_LAB_RESEARCH_REPRODUCIBILITY_STANDARD|Research Reproducibility Standard]].
12. [[ALPHA_LAB_EXECUTION_SAFETY_STANDARD|Execution Safety Standard]].
13. [[ALPHA_LAB_OBSIDIAN_KNOWLEDGE_STANDARD|Obsidian Knowledge Standard]].
14. [[ALPHA_LAB_EXCEPTION_WAIVER_STANDARD|Exception and Waiver Standard]].
15. [[AI_ENGINEERING_OS_V2_REVIEW_REPORT|Review and Expansion Report]].

## Normative Language

`MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` are used normatively. A MUST-level deviation requires an approved, expiring waiver.

## Validation

```powershell
python .\tools\engineering\validate_alpha_lab_policy.py .
python .\docs\ai_algorithm_engineering_os\tools\validate_vault.py .\docs\ai_algorithm_engineering_os
python .\tools\engineering\check_mql5_compatibility.py .
```
