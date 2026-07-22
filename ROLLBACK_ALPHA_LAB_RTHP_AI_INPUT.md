# Rollback — RTHP AI-Engine Input Binding

## Preferred rollback

If the patch was committed as a dedicated commit, revert that commit:

```powershell
git log --oneline -10
git revert <RTHP_AI_INPUT_COMMIT_SHA>
git push
```

This preserves repository history and removes only the additive RTHP AI-input integration.

## Pre-commit rollback

If the patch was expanded and staged but not committed:

```powershell
git restore --staged --pathspec-from-file=RTHP_AI_INPUT_FILE_INDEX.txt
git clean -fd --pathspec-from-file=RTHP_AI_INPUT_FILE_INDEX.txt
```

Review `git status --short` before deleting anything. The patch is designed to contain only new context-owned/generated/registry/test/documentation files and root release artifacts.

## Safety invariant

Rollback must not modify or delete:

```text
lab/11_strategy_factory/contexts/CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1/
lab/11_strategy_factory/python/strategy_factory_contexts_v3/
lab/11_strategy_factory/python/strategy_factory_dataset_v3/
lab/11_strategy_factory/python/strategy_factory_trainers_v3/
tools/strategy_factory/acl_os/
registry/acl_os/
```

The canonical Context and central engine predate this patch and remain authoritative.
