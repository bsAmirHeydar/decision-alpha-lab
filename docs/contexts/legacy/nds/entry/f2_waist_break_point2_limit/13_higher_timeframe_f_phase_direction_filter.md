# 13 — Higher-Timeframe F-Phase Direction Filter

## 1. Purpose

The higher-timeframe filter is an entry-authorization layer. It does not redefine the lower-timeframe F2 setup, its prices, its RR calculation, or its exit ownership.

Default configuration:

```text
Higher timeframe = H1
InpF2BTUseHigherTimeframeFPhaseFilter = true
InpF2BTHigherTimeframe = PERIOD_H1
```

## 2. Direction contract

```text
Higher timeframe in bullish F phase
→ Buy setups may continue to the lower-timeframe gates
→ Sell setups are rejected

Higher timeframe in bearish F phase
→ Sell setups may continue to the lower-timeframe gates
→ Buy setups are rejected

Higher timeframe in Hook/ND phase, ambiguous, unavailable, or without a qualifying F count
→ no new setup is authorized
```

Existing positions are not force-closed by this filter. Their stop and selected exit mode remain position-owned.

## 3. Multi-count authority

The classifier does not reduce the entire higher timeframe to the newest event from a single winning sequence. Every visible canonical F1 root is evaluated as its own count.

For each count the engine resolves:

```text
F1 root identity
→ same sequence_id
→ same direction
→ same scale L
→ latest F event in that count
→ Hook/ND ownership for that count only
→ optional F1-to-F2 confirmation-window state
```

A count qualifies when it is in F phase and passes the optional lifecycle window. Authorization then uses all qualifying counts:

```text
one or more qualifying bullish counts, no qualifying bearish count
→ Buy only

one or more qualifying bearish counts, no qualifying bullish count
→ Sell only

qualifying counts in both directions
→ ambiguous, fail closed
```

This implements the requested “one of the higher-timeframe counts” rule. A newer but immature count cannot hide another valid count merely by being newer.

## 4. Count-local Hook/ND veto

Hook veto is local to the count that owns the Hook boundary. An unrelated Hook from another sequence or scale cannot close every higher-timeframe count.

Ownership resolution follows two levels:

1. Exact authority: the Hook resolve/origin node matches the F1 origin node on the same direction and scale.
2. Defensive legacy fallback: on the same direction and scale, the Hook is assigned to the most recent preceding canonical F1 root.

The Hook blocks that root only when its structural endpoint is at or after the latest F event of the same root.

```text
Count A remains valid F
Unrelated Hook belongs to Count B
→ Count A remains eligible
```

## 5. Optional F1-to-F2 confirmation window

The directional filter can be narrowed by:

```text
InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = true
```

The F1-to-F2 confirmation-window is evaluated independently for every count. See [16 — Higher-Timeframe F1-to-F2 Confirmation Window](16_higher_timeframe_f1_to_f2_confirmation_window.md).

## 6. Closed-bar and cache semantics

Only closed H1 bars are used. The live higher-timeframe bar is excluded.

```text
new H1 open bar
→ rebuild canonical H1 events and Hooks once
→ evaluate all count-local phase/window states
→ cache authorization until the next H1 bar
```

No per-tick HTF detector is introduced.

## 7. Pending and position policy

With the default:

```text
InpF2BTCancelPendingWhenHigherTimeframeDisallows = true
```

unfilled managed pending orders are cancelled if the cached HTF gate no longer authorizes their direction. A cancellation releases the active attempt when consume-on-fill policy is enabled, so a still-valid lower-timeframe F2 may re-arm if the required HTF window later opens again and neither its entry nor target has already been touched.

Open positions remain under their own fixed, local-F3, or HTF-F3 exit authority.

## 8. Fail-closed cases

Entry is blocked when:

- HTF history is incomplete;
- no canonical F1 root exists;
- every count is owned by its own active Hook/ND phase;
- all counts are before F1 confirmation or after F2 confirmation while the lifecycle window is enabled;
- qualifying bullish and bearish counts coexist;
- the lower-timeframe setup direction differs from the sole qualifying HTF direction.

## 9. Non-authorities

The filter does not use:

- moving averages;
- slope or candle color;
- a global latest-Hook veto;
- an unrelated scale’s F2 confirmation;
- future/live HTF bars.
