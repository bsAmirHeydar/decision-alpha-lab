# Rollback

## Before commit

Restore the modified W0 verifier:

```powershell
git restore -- tools/consolidation/uc04w0/verify.py
```

Remove only the newly added paths listed by `git status --short` that also appear in this patch's `PATCH_FILE_INDEX.txt`.

## After commit

Use an atomic Git revert of the patch commit:

```powershell
git revert <PATCH_COMMIT_SHA>
```

Re-run Engineering Policy, UC03, W0, W1A and W1B verifiers after rollback.
