---
id: AIEOS2-5ED060716A19
title: "Integration with Decision Alpha Lab"
type: guide
status: active
domain: navigation
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - navigation
---
# Integration with Decision Alpha Lab

> [!abstract] Purpose
> Install the operating system as Decision Alpha Lab’s repository-wide engineering policy without disturbing its observation-to-production laboratory architecture.

## 1. Canonical Placement

```text
AGENTS.md
docs/engineering/
docs/ai_algorithm_engineering_os/
tools/engineering/
```

The root `AGENTS.md` is the fast enforcement contract. `docs/engineering` contains concise canonical project standards. The full modular vault contains detailed workflows, templates, prompts, examples, and governance.

## 2. Laboratory Mapping

| Quant Lab Path | Engineering Artifacts |
|---|---|
| `lab/01_observation` | observations, source evidence, ambiguity notes |
| `lab/02_hypotheses` | ontology, formal hypothesis, failure conditions |
| `lab/03_experiments` | feature/experiment packet, code, config, test matrix, outputs |
| `lab/04_analysis` | exploratory reports; no production authority |
| `lab/05_validation` | OOS, robustness, stress, benchmark, promotion recommendation |
| `lab/06_production` | approved signal/model/data contracts and versions |
| `lab/07_monitoring` | drift, runtime health, incidents, retirement evidence |
| `lab/08_archive` | rejected, retired, superseded artifacts |
| `lab/09_execution` | MQL5/broker adapters, execution state, logs, fail-safes |
| `lab/10_infrastructure` | CI, tests, configuration, data tooling, reusable utilities |
| `registry` | canonical artifact identity/status index |

## 3. Authority

Quant Lab’s approved domain doctrine wins over generic engineering conventions. Engineering policy controls how doctrine is formalized, coded, tested, delivered, and promoted. AI outputs and historical implementation behavior are lower authority.

## 4. Required Work Packet

Every non-trivial feature/bug/experiment creates or links:

```text
specification / hypothesis
context packet
patch manifest
state/data contracts
test matrix
review evidence
install/rollback
Obsidian links
registry/changelog update
```

## 5. Project Validation

```powershell
python .\tools\engineering\validate_alpha_lab_policy.py .
python .\docs\ai_algorithm_engineering_os\tools\validate_vault.py .\docs\ai_algorithm_engineering_os
python .\tools\engineering\check_mql5_compatibility.py .
```

MetaEditor compile and runtime/replay evidence remain mandatory where relevant.

## 6. Conflict Rule

Do not merge generic OS text over active Quant Lab doctrine. Resolve conflicts through the policy hierarchy and record an ADR. Preserve safe existing behavior until resolved.

## Related Notes

- [[18_ALPHA_LAB_ENGINEERING_STANDARD/_MOC|Alpha Lab Engineering Standard]]
- [[19_LANGUAGE_STANDARDS/_MOC|Language Standards]]
- [[20_QUALITY_AUTOMATION/_MOC|Quality Automation]]
