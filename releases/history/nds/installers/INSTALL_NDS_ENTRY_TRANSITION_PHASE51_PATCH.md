# Install — NDS Entry Transition Phase 51 Patch

## Scope

This root-relative patch adds a fail-closed NDS-specific transition from an
annotated valid Hook to a future Zone, Setup, Trade Plan, and broker-neutral
Command Preview.

It does **not** implement unanswered Zone or Entry Canon decisions. It does
**not** size positions and does **not** send orders.

## Install from repository root

```powershell
Expand-Archive `
  -LiteralPath ".\NDS_Entry_Transition_Phase51_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\NDS_Entry_Transition_Phase51_Patch.zip" `
  -Force
```

## Compile target

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Expected source version:

```text
18.30
```

## Default runtime profile

Keep the default values for the first smoke test:

```text
InpNDSEntryEnabled = true
InpNDSEntryContractProfile = PRE_CANON_BLOCKED
InpNDSTradeDirectionPolicy = UNRESOLVED
InpNDSEntryOrderModel = UNRESOLVED
InpNDSEntryStopModel = UNRESOLVED
InpNDSEntryTargetModel = UNRESOLVED
InpNDSEntryZoneCanonLocked = false
InpNDSEntryTradeContractLocked = false
InpNDSEntryCommandPreviewOnly = true
```

The expected fail-closed behavior is:

```text
eligible valid Hook found
→ STRUCTURE_CAPTURED
→ NDS_ZONE_BLOCKED_PRE_CANON_PROFILE
→ no Trade Plan
→ no sendable Command
```

## Runtime outputs

```text
MQL5/Files/FlagCountingPhoenix/nds_entry_structure_snapshot.csv
MQL5/Files/FlagCountingPhoenix/nds_entry_setup_candidate.csv
MQL5/Files/FlagCountingPhoenix/nds_entry_trade_plan.csv
MQL5/Files/FlagCountingPhoenix/nds_entry_command_preview.csv
MQL5/Files/FlagCountingPhoenix/nds_entry_pipeline_summary.csv
```

## Diagnostic-only downstream smoke test

`DIAGNOSTIC_MANUAL_GEOMETRY` may be used to test Setup/Plan/Command contracts.
It is explicitly non-canonical. Supply a valid Zone, entry inside that Zone,
coherent stop/target geometry, explicit direction/order/stop/target policies,
and disable only the trade-contract-lock requirement needed for the diagnostic
run. `CommandPreviewOnly` must remain true.

The output must still satisfy:

```text
volume = 0
send_allowed = false
command_action = PREVIEW_ONLY_NO_SEND
```

## Static validation

```powershell
python tools/flag_counting/nds_hook_contract_qa.py --root .
python tools/flag_counting/nds_entry_contract_qa.py --root .
python tools/flag_counting/static_qa.py --root . --csv reports/flag_counting_static_qa.csv
python tools/engineering/validate_alpha_lab_policy.py .
python tools/engineering/check_mql5_compatibility.py .
python tools/engineering/audit_repository_layout.py .
python docs/ai_algorithm_engineering_os/tools/validate_vault.py docs/ai_algorithm_engineering_os
```

## Suggested Git commit

```powershell
git add -- `
  "INSTALL_NDS_ENTRY_TRANSITION_PHASE51_PATCH.md" `
  "NDS_ENTRY_TRANSITION_PHASE51_MANIFEST.json" `
  "NDS_ENTRY_TRANSITION_PHASE51_AUDIT_REPORT.md" `
  "tools/flag_counting/nds_entry_contract_qa.py" `
  "tools/flag_counting/nds_hook_contract_qa.py" `
  "mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5" `
  "mql5/Include/FlagCountingPhoenix/FP_HookPhase02Engine.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSStructureSnapshot.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSEntryTypes.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSEntryRules.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSEntryExport.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSEntryEngine.mqh" `
  "docs/flag_counting/README.md" `
  "docs/nds_hook_architecture/README.md" `
  "docs/nds_hook_architecture/68_phase51_nds_entry_transition_architecture.md" `
  "docs/nds_entry_architecture" `
  "docs/obsidian_hook/00_mocs/HOOK_CANON_STEP7_MOC.md" `
  "docs/evidence/nds_entry_execution_moc/52823598bbb7_NDS_ENTRY_EXECUTION_MOC.md" `
  "docs/obsidian_hook/03_architecture/Phase 51 NDS Entry Transition Architecture.md" `
  "docs/obsidian_hook/05_templates/NDS Setup Review Template.md" `
  "docs/obsidian_hook/07_indexes/HOOK_VALIDITY_INDEX.md" `
  "docs/obsidian_hook/08_entry_execution"

git diff --cached --stat

git commit `
  -m "feat(nds): add fail-closed entry transition architecture" `
  -m "Bridge annotated valid Hook structure to a canonical Zone adapter seam, Setup, Trade Plan, and zero-volume no-send Command Preview; add CSV traceability, contract QA, Obsidian architecture, and implementation documentation without inventing unresolved Zone or execution doctrine."

git push
```
