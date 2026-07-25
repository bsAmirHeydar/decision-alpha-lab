# Install — NDS F2 HTF F1-to-F2 Confirmation Window Patch

## Base requirement

Apply this root-relative patch after the cumulative NDS F2 Higher-Timeframe F3 Exit patch, or onto a repository already containing Expert version `1.80`, contract `NDS-F2-WAIST-BREAK-09`, and the cached HTF F-phase filter module.

## Install

Extract the ZIP into the repository root and allow replacement of existing files.

Compile:

```text
mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5
```

## New default input

```text
InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = true
```

With the default HTF filter configuration:

```text
InpF2BTUseHigherTimeframeFPhaseFilter = true
InpF2BTHigherTimeframe = PERIOD_H1
InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = true
InpF2BTCancelPendingWhenHigherTimeframeDisallows = true
```

New entries are allowed only after the selected H1 count's F1 confirms and before its exact direct-child F2 confirms. Direction still comes from the same selected canonical H1 F count.

To retain the broader prior direction-only HTF filter:

```text
InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = false
```

## Verification

Run:

```powershell
python tools/flag_counting/nds_f2_htf_f1_to_f2_window_contract_qa.py
python tools/flag_counting/nds_f2_htf_f_phase_filter_contract_qa.py
python tools/flag_counting/nds_f2_waist_backtest_contract_qa.py
python tools/engineering/validate_alpha_lab_policy.py
python tools/engineering/check_mql5_compatibility.py
python tools/engineering/audit_repository_layout.py
```

Then compile in MetaEditor and run Strategy Tester with closed-bar HTF history available. Validate pre-F1 block, F1→F2 open interval, exact-F2 close boundary, pending cancellation, and open-position continuity.
