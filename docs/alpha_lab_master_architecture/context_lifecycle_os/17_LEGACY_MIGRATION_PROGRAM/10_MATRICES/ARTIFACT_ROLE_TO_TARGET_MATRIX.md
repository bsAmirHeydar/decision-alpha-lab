---
title: "Artifact Role to Target Matrix"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Artifact Role to Target Matrix

| Role | Canonical target |
|---|---|
| Context doctrine/contracts | `lab/11_strategy_factory/contexts/<id>` |
| Setup contracts | `lab/11_strategy_factory/setups/<id>` |
| Treatment contracts | `lab/11_strategy_factory/treatments/<id>` |
| Visualization | `lab/11_strategy_factory/visualizers/<id>` and MQL adapter |
| Shared primitive | `lab/11_strategy_factory/shared_engines/<id>` |
| MQL implementation | `mql5/Include/AlphaLab/ContextOS/...` |
| Expert host/test | `mql5/Experts/AlphaLab/ContextOS/...` |
| Legacy source evidence | active path until cutover, then migration quarantine |
| Release metadata | `registry/releases/...` |
| Generated Obsidian projection | generated knowledge namespace |
