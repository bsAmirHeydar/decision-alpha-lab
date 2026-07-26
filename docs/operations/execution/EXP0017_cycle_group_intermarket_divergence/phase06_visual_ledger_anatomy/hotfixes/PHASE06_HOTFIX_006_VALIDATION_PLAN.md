# EXP0017 Phase 06 Hotfix006 — Minimal Line-Only Visual Mode

## Validation Plan

1. Remove the EA from both charts.
2. Delete all objects with prefix `EXP0017_P06_`.
3. Install this hotfix.
4. Compile `EXP0017_CG_Visual_Ledger_Anatomy.mq5`.
5. Attach the EA to one of the two input-symbol charts.
6. Confirm that the chart contains no white label band.
7. Open Object List and verify there are no `visual_label` objects.
8. Verify that objects named `origin_to_destination_*` exist.
9. Verify that the only visible objects are line objects unless you intentionally select another visual mode.
10. Increase lookback only after confirming readability.

## Expected Object Names

```text
EXP0017_P06_*_origin_to_destination_*
EXP0017_P06_*_origin_to_destination_*_shadow
```

## Objects That Should Not Exist in Minimal Mode

```text
visual_label
origin_marker
destination_marker
origin_vertical
destination_vertical
confirmation_close_vertical
reference_guide
current_extreme_guide
clean_stop_reference_guide
reference_cycle_anchor
```

If these appear while `InpVisualMode=CGV_VISUAL_MODE_MINIMAL_LINES_ONLY`, the old file was not replaced or an older compiled EX5 is still running.
