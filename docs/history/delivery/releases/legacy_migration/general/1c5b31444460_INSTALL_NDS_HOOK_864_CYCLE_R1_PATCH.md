# Install NDS Hook 86.4 Cycle R1 Patch

## Source installation

Place the ZIP in repository root, expand it into root, remove the ZIP, run the bounded QA, then create one atomic commit.

## Repository QA

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\flag_counting\run_nds_hook_864_cycle_r1_tests.ps1
```

## Windows MetaEditor gate

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\flag_counting\compile_nds_hook_864_cycle_r1.ps1 -MetaEditorPath "C:\Path\To\metaeditor64.exe"
```

The compile command writes external evidence under `local_evidence/nds_hook_864_cycle_r1/metaeditor`. It compiles the contract diagnostic, lightweight backtest expert, and central Phoenix expert, and requires a clean zero-error, zero-warning log. External evidence is not included in the source patch.

## Initial operating mode

For paper evaluation:

```text
InpNDSHookTradeEnabled = true
InpNDSHookTradeSendLiveOrders = false
InpNDSHookTradeProfile = HOOK_864_CYCLE_R1
ratio = 0.864
min_x_count = 3
max_x_count = 4
confirmed_terminal = true
level_untouched = true
fixed_reward_r = 1.0
```

Any noncanonical profile value is rejected. Live send must remain disabled until the normal compile, Strategy Tester, demo broker, risk, reconciliation, and approval gates are complete.

## Rollback

Disable decision and send authority, reconcile and preserve any demo broker exposure/evidence, then revert the atomic patch commit. Do not clear the one-attempt registry or delete broker/ledger evidence before reconciliation.
