# Install — NDS Pre-Canon Stabilization Patch

## Scope

This root-relative patch stabilizes the existing NDS Hook implementation before final Valid Hook / Zone questionnaire decisions are encoded.

It does not implement Zone logic and does not replace unanswered Canon decisions with assumptions.

## Install from repository root

```powershell
Expand-Archive `
  -LiteralPath ".\NDS_Pre_Canon_Stabilization_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\NDS_Pre_Canon_Stabilization_Patch.zip" `
  -Force
```

## Compile target

Compile in MetaEditor:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Expected source version:

```text
18.21
```

## Repository validation

```powershell
python tools/engineering/validate_alpha_lab_policy.py .
python tools/engineering/check_mql5_compatibility.py .
python tools/engineering/audit_repository_layout.py .
python docs/ai_algorithm_engineering_os/tools/validate_vault.py docs/ai_algorithm_engineering_os
python tools/flag_counting/static_qa.py --root .
python tools/flag_counting/nds_hook_contract_qa.py --root .
```

## Runtime validation

1. Run the EA in `HOOK_ONLY` mode.
2. Keep `InpHookPhase02ShowOnlyValidHooks=true`.
3. Test both values of `InpHookPhase02ValidF3RequireOppositeDirection` and confirm the input changes recognition behavior.
4. Test `FP_HOOK_POST_F3_PRIORITY_EARLIEST_FIRST` and verify the selected sequence owns the earliest origin bar.
5. Export Phase02 CSV and verify the matched F3 terminal and origin-distance fields.
6. Change timeframe and reattach the EA; final visible sets must reconstruct identically.

## Commit

```powershell
git add -- `
  "INSTALL_NDS_PRE_CANON_STABILIZATION_PATCH.md" `
  "NDS_PRE_CANON_STABILIZATION_MANIFEST.json" `
  "NDS_PRE_CANON_AUDIT_REPORT.md" `
  "tools/flag_counting/nds_hook_contract_qa.py" `
  "mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5" `
  "mql5/Include/FlagCountingPhoenix/FP_HookPhase02Types.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_HookPhase02Export.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_HookPhase02Engine.mqh" `
  "docs/nds_hook_architecture/README.md" `
  "docs/nds_hook_architecture/67_phase50_pre_canon_nds_stabilization.md" `
  "docs/obsidian_hook/00_mocs/HOOK_CANON_STEP7_MOC.md" `
  "docs/obsidian_hook/01_concepts/Canonical Bar Index Authority.md" `
  "docs/obsidian_hook/03_architecture/Phase 50 Pre-Canon NDS Stabilization.md" `
  "docs/obsidian_hook/04_debug/NDS Pre-Canon Contract Checklist.md" `
  "docs/obsidian_hook/07_indexes/HOOK_VALIDITY_INDEX.md"

git diff --cached --stat

git commit `
  -m "fix(nds): stabilize post-f3 hook ownership before canon" `
  -m "Move post-F3 ownership to canonical bar indexes, honor recognition inputs and earliest-first priority, preserve matched F3 terminal evidence, and document unresolved Hook/Zone semantics without implementing them."

git push
```
