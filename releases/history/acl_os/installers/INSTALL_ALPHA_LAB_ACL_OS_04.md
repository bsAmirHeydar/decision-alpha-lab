# Install ACL-04

## Preconditions

ACL-00 through ACL-03 must already exist in the repository. The ACL-03 reference fixture and its `ACL03_TO_ACL04` handoff are required by the ACL-04 replay and contract tests.

## Installation

Expand `ACL_OS_04_DUAL_SETUP_FACTORY_PATCH.zip` at the repository root. Do not expand it into a nested folder. The archive contains root-relative paths and intentionally updates the canonical ACL-04 architecture notes and implementation-program note.

## Verification

Run:

```powershell
python -m tools.strategy_factory.acl_os.acl_04.run_acl_04_full_qa
python -m tools.strategy_factory.acl_os.acl_04.validate_acl_04_delivery
```

The MQL5 artifacts are static contract mirrors. This patch does not claim MetaEditor compilation or MT5 runtime parity. Those claims require an environment-specific compile and test report.

## Staging discipline

Stage only the paths supplied with the patch delivery command. Do not use `git add .` because the repository may contain unrelated local research artifacts.
