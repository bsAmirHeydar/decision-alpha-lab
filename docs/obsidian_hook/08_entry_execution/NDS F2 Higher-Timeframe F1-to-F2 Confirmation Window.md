# NDS F2 Higher-Timeframe F1-to-F2 Confirmation Window

## Contract

```text
Selected HTF count before F1 confirmation
→ no entry

Selected HTF count after F1 confirmation
and before exact direct-child F2 confirmation
→ selected HTF direction may trade

Exact direct-child F2 confirmed
→ no new entry
```

Default input:

```text
InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = true
```

The selected F1 and F2 must belong to the same canonical sequence, direction, scale, and direct parent-child lineage used by the HTF phase-direction classifier. Another count cannot open or close this window.

The filter uses closed HTF bars and the existing cached HTF scan. It does not add a second scan. When pending cancellation is enabled, unfilled orders are removed when the window closes; open positions keep their own exit mode.

## Authority

- [[../../nds_entry_architecture/f2_waist_break_point2_limit/16_higher_timeframe_f1_to_f2_confirmation_window|Full lifecycle-window contract]]
- [[NDS F2 Higher-Timeframe F-Phase Filter]]
- [[NDS F2 Waist-Break Point2 Limit Setup]]
