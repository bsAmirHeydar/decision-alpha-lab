# Rollback Alpha Lab LCM-09B

## Before commit

```powershell
git restore --staged --pathspec-from-file=LCM_09B_FILE_INDEX.txt
git restore --pathspec-from-file=LCM_09B_FILE_INDEX.txt
```

Remove newly created untracked files only from the exact index after reviewing `git status --short`. Do not use broad clean/reset commands in a working tree containing unrelated work.

## After commit but before shared downstream work

Create a normal revert commit:

```powershell
git revert --no-edit HEAD
git push
```

## Verification after rollback

```powershell
python -m pytest -q lab/11_strategy_factory/acl_os/tests_acl_04
```

Legacy Setup source files require no restoration because LCM-09B performs no source move, delete, semantic rewrite, consumer cutover, or execution activation.
