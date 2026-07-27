# UC04-W1B-Q Installable Release R4

## Intent

Deliver the already-bounded UC04-W1B-Q native-qualification tooling as a root-relative, hash-bound, schema-validated, transactionally installable patch from the accepted UC04-W1A state.

## R4 isolated-staging correction

R3 correctly fixed the PowerShell parser defect, but Python imported the staged validation module before exact membership verification and wrote `__pycache__/*.pyc` into the isolated staging tree. The validator correctly rejected those extra files. R4 preserves strict membership and instead prevents the mutation at its source by invoking every installer-owned Python process with `-B` and process-scoped `PYTHONDONTWRITEBYTECODE=1`. A subprocess regression test extracts the ZIP, validates it from staging, and proves that no bytecode cache is created. Installer-owned Pytest gates also disable the cache provider, so `.pytest_cache` cannot pollute the repository.

## Current behavior

W1B-Q tooling, native evidence review, conditional candidate generation, governance records, schemas, tests, documentation, and CI exist. The earlier release wrapper assumed that payload files had already been extracted correctly and did not itself enforce staging isolation, exact archive membership, per-file hashes, line endings, LFS/secret absence, automatic rollback, or post-install gates.

## Desired behavior

A user can verify the external ZIP checksum, inspect and expand the archive into an isolated staging directory, validate every staged byte against the patch index and hash ledger, install only the bounded target paths, run all mandatory gates, and restore the exact pre-install state if any step fails.

## Scope

- deterministic root-relative ZIP construction and verification;
- exact index and SHA-256 ledger enforcement;
- JSON Schema validation for the patch manifest and QA report;
- UTF-8/no-BOM, CRLF/LF policy enforcement;
- Windows-safe path, case-collision, ZIP traversal, symlink, secret, cache, and Git LFS pointer rejection;
- transactional PowerShell installation with external backup and automatic rollback;
- CI verification of release controls and deterministic ZIP replay;
- documentation and Obsidian release-contract update.

## Non-goals

- no production shared include;
- no changes to the ten consumers or forty-one call sites;
- no change to Context, Entry, Treatment, Execution, Stop, Target, Risk, model, label, feature, or Train semantics;
- no MetaEditor/MetaTrader evidence claim;
- no implementation, cutover, deletion, runtime, order, or capital authority;
- no Git commit or push performed by the installer.

## Preserved invariants

- candidate: `ENGCAND_5F87C4D5849C4FD141DDBF29590235D8`;
- proposed engine: `ENG_9599AA665C5BC4B13B020EBA4213CB16`;
- output contract: `YYYY.MM.DD HH:MM:SS`;
- ten historical consumer hashes remain frozen;
- forty-one call sites remain unchanged;
- all authority fields remain `false`;
- native qualification remains pending on the local Windows/MT5 host.

## Release controls

- `PATCH_FILE_INDEX.txt`: the only paths permitted in the ZIP and Git staging set;
- `PATCH_FILE_HASHES.sha256`: SHA-256 for every indexed file except the ledger itself;
- `PATCH_MANIFEST.json`: scope, invariants, platform, authority, LFS, line-ending, rollback, and risk contract;
- `QA_REPORT.json`: executed evidence and explicitly unexecuted native/full-suite work;
- `APPLY.ps1`: transactional install/rollback engine; it never stages, commits, or pushes;
- external `<zip>.sha256`: archive checksum sidecar, distributed next to the ZIP.

## Required base

The patch is self-contained relative to the accepted UC04-W1A repository state. W0 and W1A verifiers must pass before any file transfer. It can replace a clean, committed earlier W1B-Q delivery because all pre-existing target bytes are backed up before overwrite.

## Installation and rollback

Follow the R4 `INSTALL.md` exactly. Preserve the printed `INSTALL_STATE.json` path; it is the authority for `ROLLBACK.md`.

## Native follow-up

After installation and commit, the local operator may execute:

```powershell
powershell -ExecutionPolicy Bypass -File tools/consolidation/uc04w1b/Invoke-UC04W1BQualification.ps1
```

That command produces local evidence only. It does not apply the generated cutover candidate.
