# Rollback Engineering Policy CI Recovery V1

Rollback is commit-level and affects only the paths recorded in `ENGINEERING_POLICY_CI_RECOVERY_V1_FILE_INDEX.txt`. No data, schema, market doctrine, MQL5 runtime, redirect stub, or LCM migration receipt requires restoration.

Use the recovery commit SHA and create a normal inverse commit:

```powershell
$recoveryCommit = git log --format='%H' --grep='^fix(ci): restore canonical engineering preflight$' -n 1
if (-not $recoveryCommit) { throw 'Recovery commit not found' }
git revert --no-edit $recoveryCommit
python .\tools\engineering\run_engineering_policy.py .
git push origin main
```

The preflight is expected to fail again after rollback because the old runner target is the generated legacy vault. Use rollback only for an action-runtime or integration incompatibility that outweighs the known failure, and preserve the revert evidence in Git history.
