# NDS F2 Higher-Timeframe F1-to-F2 Confirmation Window — Audit Report

## 1. Intent

Add an optional entry-timing filter to the existing canonical higher-timeframe F-phase direction gate.

The selected higher-timeframe count already supplies direction. This patch restricts lower-timeframe entries to one exact lifecycle interval of that same count:

```text
before selected HTF F1 confirmation
→ no new entry

after selected HTF F1 confirmation
and before confirmation of its exact direct-child F2
→ entries may be authorized in the selected HTF direction

at/after confirmation of that exact F2
→ no new entry
```

The filter is enabled by default and can be disabled independently from the broader HTF F-phase direction filter.

## 2. New operator input

```text
InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = true
```

Related existing inputs remain:

```text
InpF2BTUseHigherTimeframeFPhaseFilter = true
InpF2BTHigherTimeframe = PERIOD_H1
InpF2BTCancelPendingWhenHigherTimeframeDisallows = true
```

## 3. Exact lineage contract

The lifecycle window is evaluated only on the same canonical HTF count selected for direction.

Required identity chain:

```text
selected canonical HTF event
→ selected sequence_id
→ exact F1 root in the same sequence/direction/scale
→ exact direct-child F2
```

The F2 must satisfy:

```text
F2.sequence_id       = selected.sequence_id
F2.direction         = selected.direction
F2.scale_L           = selected.scale_L
F2.chain_index       = 2
F2.parent_sequence_id = F1.sequence_id
F2.parent_event_id    = F1.event_id
```

No same-direction F1/F2 from another sequence or scale may open or close the selected window.

## 4. Confirmation authority

### F1 opens the window only when canonical confirmation is complete

```text
level = F1
chain_index = 1
status = CONFIRMED
lifecycle_status = FP_F1_LC_CONFIRMED
has_confirm = true
lifecycle_can_spawn_f2 = true
```

A live body, post-flag candidate, or merely complete F1 body does not open the window.

### F2 closes the window only when its canonical confirmation is complete

```text
level = F2
chain_index = 2
status = CONFIRMED
f2_lifecycle_status = FP_F2_LC_CONFIRMED
has_confirm = true
f2_can_spawn_f3 = true
```

An absent, live, post-flag, size-rejected, or otherwise unconfirmed F2 does not close the window.

## 5. Combined entry gate

A lower-timeframe setup now requires all applicable conditions:

```text
HTF history ready
AND canonical HTF F selected
AND current HTF phase is F rather than Hook/ND
AND no equal-priority direction conflict
AND selected HTF F1 confirmed             [when window input enabled]
AND selected exact direct-child F2 not confirmed
AND lower-timeframe setup direction matches selected HTF direction
```

All missing, ambiguous, pre-F1, post-F2, Hook/ND, and unresolved states fail closed.

## 6. State model added

```text
DISABLED
NOT_EVALUATED
SEQUENCE_MISSING
AMBIGUOUS
BEFORE_F1_CONFIRM
OPEN
CLOSED_AFTER_F2_CONFIRM
```

Only `OPEN` authorizes entries when the new input is enabled.

The HTF snapshot now preserves selected-sequence evidence:

- selected sequence id;
- F1 event id, status, lifecycle status, and confirmation time;
- F2 event id, status, lifecycle status, and confirmation time;
- window evaluated/open flags;
- lifecycle-window state.

## 7. Causal-time behavior

The existing closed-bar HTF contract is preserved.

```text
live HTF bar = excluded
cached HTF snapshot = refreshed once per new HTF bar
```

Consequently, F1/F2 confirmation boundaries become actionable only after the higher-timeframe bar containing the confirmed node is closed and the snapshot refreshes. No future-derived or intrabar HTF state is introduced.

## 8. Pending-order behavior

The existing pending reconciliation policy consumes the final combined gate.

With this input enabled:

```text
InpF2BTCancelPendingWhenHigherTimeframeDisallows = true
```

- no pending order is created before F1 confirmation;
- pending orders can exist inside the F1-confirmed/F2-unconfirmed interval;
- still-unfilled pending orders are cancelled when the exact F2 confirms;
- open positions are not force-closed by this entry filter.

Position exit remains owned by the selected fixed-F2, exact local-F3, or HTF-F3 exit mode.

## 9. Performance impact

No new detector pass was added.

The same cached HTF `FP_DetectAllScales` event array is reused:

```text
cached HTF F/Hook scan
→ select phase event
→ resolve exact same-sequence F1/F2 lineage
→ evaluate window
```

No per-tick scan, print, renderer, CSV, timer, chart object, or AI runtime was introduced.

## 10. Files changed

### Runtime

- `mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2HigherTimeframePhaseFilter.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeTypes.mqh`

### Documentation

- `docs/flag_counting/README.md`
- `docs/nds_entry_architecture/README.md`
- `docs/nds_entry_architecture/f2_waist_break_point2_limit/README.md`
- `docs/nds_entry_architecture/f2_waist_break_point2_limit/08_operator_guide.md`
- `docs/nds_entry_architecture/f2_waist_break_point2_limit/13_higher_timeframe_f_phase_direction_filter.md`
- `docs/nds_entry_architecture/f2_waist_break_point2_limit/16_higher_timeframe_f1_to_f2_confirmation_window.md`
- `docs/obsidian_hook/00_mocs/NDS_ENTRY_EXECUTION_MOC.md`
- `docs/obsidian_hook/08_entry_execution/NDS F2 Higher-Timeframe F-Phase Filter.md`
- `docs/obsidian_hook/08_entry_execution/NDS F2 Higher-Timeframe F1-to-F2 Confirmation Window.md`

### QA

- new lifecycle-window contract QA;
- existing NDS F2 contract scripts updated to the new Expert/contract/schema version.

## 11. Preserved invariants

This patch does not change:

- F2 Waist-Break Point-2 entry geometry;
- F1-waist stop geometry;
- original F2 endpoint RR authority;
- RR repricing;
- overlap arbitration and wider-context selection;
- same-direction parallel contexts;
- opposite-direction hedge policy;
- fixed F2 exit;
- exact per-trade local F3 exit;
- higher-timeframe F3 exit;
- the HTF F-versus-Hook direction classifier;
- closed-bar HTF semantics;
- open-position exit ownership.

## 12. Validation evidence

Passed in the cumulative reconstructed worktree:

- all `tools/flag_counting/nds_f2_*_qa.py` contract and regression scripts;
- `tools/engineering/validate_alpha_lab_policy.py`;
- `tools/engineering/check_mql5_compatibility.py`;
- `tools/engineering/audit_repository_layout.py`;
- include-resolution inspection;
- brace-balance inspection;
- forbidden runtime Print/PrintFormat/renderer/file-IO checks;
- ZIP integrity and SHA-256 manifest generation.

MetaEditor was not available in the build environment. Final `.mq5` compilation and Strategy Tester replay remain required on the operator machine.

## 13. Required Strategy Tester acceptance cases

1. HTF F1 body complete but unconfirmed: no order.
2. Exact selected HTF F1 confirms: matching-direction lower-timeframe setups become eligible.
3. Exact selected HTF F2 exists but remains unconfirmed: window remains open.
4. Exact selected HTF F2 confirms: new orders blocked and managed pending orders cancelled when policy is enabled.
5. A different sequence F2 confirms: it must not close the selected sequence window.
6. Window input disabled: behavior returns to the broader HTF F-phase direction-only filter.
7. Open position during F2 confirmation: position remains under its own exit mode.

## 14. Residual risks

- Actual MetaEditor compiler acceptance is unverified in this environment.
- The lifecycle boundary is closed-HTF-bar based, not intrabar.
- Ambiguous or duplicated same-sequence F1/F2 lineage fails closed by design.
- If the authoritative HTF selected sequence changes, the new selected sequence owns both direction and lifecycle-window state; the previous sequence does not retain entry authority.

## 15. Rollback

Restore the three runtime files and associated QA/documentation files from the preceding cumulative v9 state, or revert the commit produced for this patch.
