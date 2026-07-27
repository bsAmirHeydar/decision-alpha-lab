---
id: UCPS-41B7C2D65E90
title: "UC04-W1B Installable Release and Rollback Contract"
type: release-contract
status: canonical
domain: unified-consolidation-platform-seal
version: 1.1.0
created: 2026-07-27
updated: 2026-07-27
tags:
  - consolidation
  - uc04
  - w1b
  - release
  - rollback
---
# UC04-W1B Installable Release and Rollback Contract

## Intent

The UC04-W1B-Q delivery must be installable from the accepted W1A repository without relying on an already-extracted working copy. Release safety is part of the change: archive identity, payload membership, hashes, schemas, line endings, Windows path compatibility, Git cleanliness, verification, and rollback are all explicit gates.

## Installation boundary

The ZIP contains only root-relative patch files. It has no repository wrapper directory and no `.git`, virtual environment, cache, secret, generated native evidence, EX5, or Git LFS pointer. The archive is expanded into a unique staging directory outside the repository. Transfer into the repository occurs only after archive-path inspection, ZIP SHA-256 verification, exact index membership, per-file SHA-256 verification, schema checks, secret/LFS scans, and line-ending checks pass.

## Transaction behavior

`releases/unified_consolidation/uc04/w1b/APPLY.ps1`:

1. verifies the accepted W0 and W1A state;
2. refuses uncommitted changes on patch target paths;
3. backs up every pre-existing target file outside the repository;
4. copies each payload file through a hash-verified temporary sibling;
5. executes policy, migration, UC-03, W0, W1A, W1B, targeted pytest, and full collection gates;
6. automatically restores the backup if any transfer or gate fails;
7. writes an operator-local installation state containing the exact rollback path.

The installer never stages, commits, pushes, or grants implementation, runtime, order, consumer-cutover, deletion, or capital authority.

## Line endings and platforms

Patch index paths always use forward slashes. PowerShell files are UTF-8 without BOM and CRLF-terminated. All other governed text files are UTF-8 without BOM and LF-terminated. Archive members are checked for Windows case collisions, reserved names, trailing dots/spaces, drive prefixes, absolute paths, and `..` traversal.

The install surface is Windows PowerShell 5.1 or newer. Python release validation and CI remain compatible with Linux and Windows Python 3.11 or newer.

Installer-owned Python processes MUST run with bytecode writing disabled (`-B` and process-scoped `PYTHONDONTWRITEBYTECODE=1`). Exact staging membership remains fail-closed; `__pycache__`, `.pyc`, and `.pyo` files are never ignored or admitted into the payload.
Installer-owned Pytest gates MUST use `-p no:cacheprovider`; `.pytest_cache` is not an accepted install or verification side effect.

## Rollback

Rollback is state-bound. Files that existed before installation are restored only from hash-verified backups. Files introduced by the patch are deleted only when their current bytes still equal the installed hash. If a file changed after installation, rollback fails closed rather than destroying operator changes.

## Non-goals

This release hardening does not materialize the production formatter include, modify the ten consumers, change any of the forty-one call sites, execute MetaEditor or MetaTrader, create market data, or authorize cutover. Native qualification remains a separate local Windows/MT5 gate.

## Evidence

- `tools/consolidation/uc04w1b/package_validation.py`
- `tests/consolidation/uc04w1b/test_package_validation.py`
- `releases/unified_consolidation/uc04/w1b/APPLY.ps1`
- `releases/unified_consolidation/uc04/w1b/PATCH_MANIFEST.json`
- `releases/unified_consolidation/uc04/w1b/QA_REPORT.json`

## Navigation

- [[01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/15_UC04_W1B_NATIVE_QUALIFICATION/00_MOC|W1B records MOC]]
