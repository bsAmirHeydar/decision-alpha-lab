---
id: UCPS-70BD1A9E5C33
title: "UC-03 Part 2 Compatibility Shims and Stable Root Discovery"
type: standard
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-25
updated: 2026-07-25
tags:
  - consolidation
  - uc03
  - compatibility
  - repository-root
---
# UC-03 Part 2 Compatibility Shims and Stable Root Discovery

## Python package compatibility

Historical packages previously exposed by `lab/11_strategy_factory/python` remain importable after relocation through the temporary repository-local bootstrap in `sitecustomize.py`.

Historical `tools.<package>` imports remain available through namespace shims whose `__path__` points to the relocated implementation. Shims contain no business logic and are observable technical debt.

## Stable repository-root discovery

Depth-coupled expressions such as:

```python
ROOT = Path(__file__).resolve().parents[4]
```

are mechanically replaced only when the expression resolved to the repository root in the pre-move location. The replacement is:

```python
ROOT = find_repository_root(__file__)
```

Local parent traversal that targets a package, fixture or adjacent directory is not rewritten.

## Removal

Compatibility paths are temporary. UC-06 must migrate every consumer; UC-07 removes shims and the bootstrap after telemetry reaches zero.
