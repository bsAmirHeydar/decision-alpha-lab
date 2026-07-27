---
id: UCPS-70F508C6309F
title: "UC04-W0 Test Estate Recovery"
type: verification
status: accepted
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-27
updated: 2026-07-27
tags:
  - consolidation
  - uc04
  - testing
---
# UC04-W0 Test Estate Recovery

## Original failure mode

After UC-03, a repository-wide collection attempted to import many same-named test modules as global modules. This created hundreds of `import file mismatch` and sibling-helper import errors. Stage-specific CI remained green because it did not collect the full test estate.

## Recovery design

The root `pytest.ini` establishes:

- `--import-mode=importlib`;
- root and `src/engine/packages` on the Python path;
- `tests` as the canonical collection root;
- deterministic exclusion of cache and Git metadata.

Test directories that require package identity receive empty `__init__.py` markers. Sibling helper and `conftest` imports are explicit relative imports rather than accidental global imports.

## Verified result

```text
python -m pytest --collect-only -q
9,732 tests collected
0 collection errors
```

The scoped UC-01 through UC-03 and RTHP recovery suite produced:

```text
166 passed
7 skipped
0 failed
0 errors
```

The seven skips are retained historical dynamic-package cases whose original packages are absent after accepted migration. They are reported; they are not converted into passes.

## Meaning of the result

Collection integrity means every test has a stable import identity. It does not guarantee that all historical tests represent current canonical contracts. Full-suite failures, if any, must be classified as current defect, stale historical expectation or formally quarantined debt; they may not be hidden by narrowing CI.

## Full-suite execution limitation

The full `python -m pytest -q` execution was attempted after successful collection. It did not complete within the 900-second execution window and had reached approximately five percent. A separate fail-fast reproduction stopped after 197 passes and seven skips at a historical LCM reference-package test. The required dependency CSV is declared as 61,208,723 bytes, while the supplied source ZIP contains the unchanged 133-byte Git LFS pointer. Four historical LFS payloads are absent from the supplied archive.

Therefore W0 records full-suite execution as `INCOMPLETE_AT_FIRST_HISTORICAL_LFS_BLOCKER`. Tests beyond that blocker remain unqualified; W0 does not reclassify them as passing.
