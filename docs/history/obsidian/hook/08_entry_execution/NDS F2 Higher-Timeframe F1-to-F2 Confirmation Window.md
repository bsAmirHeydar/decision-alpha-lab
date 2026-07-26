# NDS F2 Higher-Timeframe F1-to-F2 Confirmation Window

## Contract

```text
Each HTF count before F1 confirmation → does not qualify
Each HTF count after F1 confirmation and before exact child F2 confirmation → qualifies
Exact direct-child F2 confirmed → that count closes
```

At least one count may authorize the direction. A newer immature count does not suppress another open window. If bullish and bearish windows are both open, entry is blocked as ambiguous.

Default:

```text
InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = true
```

Stabilization is exact confirmation, not later spawn eligibility:

```text
F1 = confirmed lifecycle + confirm node
F2 = confirmed F2 lifecycle + confirm node + exact parent identity
```

Closed HTF bars and the existing cached scan are used. Pending cancellation affects unfilled orders; open positions retain their own exit authority.

## Authority

- [[../../nds_entry_architecture/f2_waist_break_point2_limit/16_higher_timeframe_f1_to_f2_confirmation_window|Full lifecycle-window contract]]
- [[NDS F2 Higher-Timeframe F-Phase Filter]]
- [[NDS F2 Canonical Frequency Recovery and Multi-Count HTF Gate]]
