---
title: Install Alpha Lab ACL-OS 05 Patch
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-05, installation]
---

# Install Alpha Lab ACL-OS 05 Patch

Place `ACL_OS_05_IMMUTABLE_BATCH_AND_ARTIFACT_STORE_PATCH.zip` in the repository root. Expand it with overwrite enabled, remove the ZIP, stage only the listed patch paths, commit and push. The ZIP contains root-relative paths and must not be expanded into a nested folder.

## Preconditions

- The repository contains the accepted ACL-04 commit and reference factory fixture.
- The working tree has no unreviewed changes on patch-owned paths.
- Python can import `jsonschema` and `pytest` for local verification.

## Post-install verification

```powershell
python -m compileall -q tools/strategy_factory/acl_os/acl_05
python -m pytest -q lab/11_strategy_factory/acl_os/tests_acl_05
python -m pytest -q lab/11_strategy_factory/acl_os/tests_acl_04
python -m tools.strategy_factory.acl_os.acl_05.run_acl_05_full_qa
```

MetaEditor and MT5 are not invoked by this reference patch.
