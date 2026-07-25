# Install — NDS Hook Limit Entry and F123 Exit Patch

## Patch identity

```text
NDS-HOOK-LIMIT-F123-EXECUTION-P52
Central EA: FlagCountingPhoenixExperiment.mq5
EA version: 18.40
```

## 1. Install from repository root

Place `NDS_Hook_Limit_F123_Execution_Patch.zip` in the repository root and run PowerShell:

```powershell
Expand-Archive `
  -LiteralPath ".\NDS_Hook_Limit_F123_Execution_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\NDS_Hook_Limit_F123_Execution_Patch.zip" `
  -Force
```

## 2. Compile

Compile this root EA in MetaEditor:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Required result:

```text
0 errors, 0 warnings
```

## 3. First-run profile — no broker send

```text
InpNDSHookTradeEnabled = true
InpNDSHookTradeSendLiveOrders = false
InpNDSHookTradeAllowHookAfterHook = true
InpNDSHookTradeAllowHookAfterF3 = true
InpNDSHookTradeRequireClosedHook = true
InpNDSHookTradeOneAttemptPerHook = true
InpNDSHookTradeRequireFullF123AfterEntry = true
```

Review:

```text
MQL5/Files/FlagCountingPhoenix/nds_hook_limit_f123_trade_ledger.csv
```

The expected action is `PAPER_LIMIT`; no broker order is sent.

## 4. Controlled demo profile

After compile, chart, and paper-ledger validation:

```text
InpNDSHookTradeEnabled = true
InpNDSHookTradeSendLiveOrders = true
```

Use a unique `InpNDSHookTradeMagic`, the minimum acceptable test volume, and a demo/non-production account.

## 5. One-attempt registry reset

Only when an intentional retest of already-consumed Hook decisions is required:

```text
InpNDSHookTradeResetUsedSetupsOnInit = true
```

Reinitialize the EA once, then immediately return the input to:

```text
InpNDSHookTradeResetUsedSetupsOnInit = false
```

## 6. Acceptance sequence

1. No HH/F3H: no pending order.
2. Valid positive HH/F3H: one Buy Limit at Hook terminal.
3. Valid negative HH/F3H: one Sell Limit at Hook terminal.
4. A second chart with the same magic: no second pending/order exposure.
5. Pending remains alive while death boundary is not breached.
6. Filled position blocks all new entries.
7. Opposite-direction F123 does not close the position.
8. F123 whose F1/F2 began before the fill does not close in strict mode.
9. Full same-direction F1→F2→F3 after fill closes the position by ticket.
10. Restart on the same Hook does not submit another order.

## 7. Static QA commands

```powershell
python tools/flag_counting/nds_hook_trade_contract_qa.py --root .
python tools/flag_counting/nds_entry_contract_qa.py --root .
python tools/flag_counting/nds_hook_contract_qa.py --root .
python tools/engineering/validate_alpha_lab_policy.py .
python tools/engineering/check_mql5_compatibility.py .
python tools/engineering/audit_repository_layout.py .
python docs/ai_algorithm_engineering_os/tools/validate_vault.py docs/ai_algorithm_engineering_os
```

## 8. Safety warning

This patch contains broker-capable `CTrade` calls. Live authority remains off by default. Do not enable `InpNDSHookTradeSendLiveOrders` before MetaEditor compilation, chart validation, decision-ledger inspection, and demo-account lifecycle testing are complete.
