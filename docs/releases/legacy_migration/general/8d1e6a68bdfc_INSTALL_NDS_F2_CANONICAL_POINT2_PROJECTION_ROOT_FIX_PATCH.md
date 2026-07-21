# Install — NDS F2 Canonical Point-2 Projection Root Fix

## Scope

This is a root-relative cumulative patch over the F2 `2.00 / v11` frequency-recovery build.

```text
Expert version: 2.10
Trade contract: NDS-F2-WAIST-BREAK-12
Schema: nds_f2_waist_break_point2_v12
```

The patch fixes only the F2 Waist-Break Point-2 execution setup. Existing Phoenix Flag Body, Internal Count, F1/F2/F3 lifecycle, and Sequence code is intentionally unchanged.

## Install

Run from the repository root:

```powershell
Expand-Archive `
  -LiteralPath ".\NDS_F2_Canonical_Point2_Projection_Root_Fix_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\NDS_F2_Canonical_Point2_Projection_Root_Fix_Patch.zip" `
  -Force
```

## Compile target

```text
mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5
```

## Locked setup

```text
F2 two-leg flag body:
Origin → Leg1 → Waist → Leg2 / flag end

Then post-flag correction:
1/2 minimum, including the Waist-break branch

Preferred branch:
Point 1 = F2 Waist
Point 2 = strict passage that breaks F2 Waist

Entry = pending limit beyond F2 Waist
Stop = behind direct parent F1 Waist
Fixed TP / RR reference = original F2 flag end

Later re-pass of original F2 flag end = F2 confirmation
```

## Important execution behavior

- The pending order is staged before Point 2, after the source body is causally observable.
- Entry offset is at least `boundary epsilon + one trade tick`.
- Every pending order is bound to one exact F2 body version.
- Leg2 extension, F2 confirmation, invalidation, disappearance, or target consumption cancels only that pending order.
- Dynamic exit orders still use the original F2 flag end for pre-fill validity even though broker TP is initially zero.

## Validation commands

```powershell
python .\tools\engineering\check_mql5_compatibility.py
python .\tools\engineering\validate_alpha_lab_policy.py
python .\tools\engineering\audit_repository_layout.py
python .\tools\flag_counting\static_qa.py
python .\tools\flag_counting\nds_f2_canonical_point2_projection_root_fix_qa.py
python .\tools\flag_counting\nds_f2_canonical_frequency_recovery_contract_qa.py
python .\tools\flag_counting\nds_f2_waist_backtest_contract_qa.py
python .\tools\flag_counting\nds_f2_waist_break_point2_contract_qa.py
python .\tools\flag_counting\nds_f2_dual_exit_contract_qa.py
python .\tools\flag_counting\nds_f2_per_trade_f3_exit_contract_qa.py
python .\tools\flag_counting\nds_f2_higher_timeframe_f3_exit_contract_qa.py
python .\tools\flag_counting\nds_f2_htf_f_phase_filter_contract_qa.py
python .\tools\flag_counting\nds_f2_htf_f1_to_f2_window_contract_qa.py
python .\tools\flag_counting\nds_f2_overlap_wider_rr_reprice_contract_qa.py
python .\tools\flag_counting\nds_f2_rr_parallel_context_contract_qa.py
```

## Tester validation

Use:

```text
Model = Every tick based on real ticks
Account mode = Hedging when parallel contexts or hedge are enabled
```

MetaEditor compilation is not available in the patch-build environment. Compile the Expert locally before committing the test result.
