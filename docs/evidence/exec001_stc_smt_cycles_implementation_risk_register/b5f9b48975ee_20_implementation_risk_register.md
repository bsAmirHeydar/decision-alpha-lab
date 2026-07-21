# EXEC001 STC SMT Cycles — Implementation Risk Register

This document lists the main engineering risks and how the implementation plan controls them.

---

## 1. Time Conversion Risk

### Risk

Wrong New York time or DST handling can shift M/W cycles and invalidate all signals.

### Control

Time conversion is isolated in `DAL_STC_Time.mqh` and must be tested before signal logic exists.

### Gate

No SMT logic is allowed before the time gate passes.

---

## 2. Check Candle Anchoring Risk

### Risk

3m and 10m candles may be aligned differently by broker data or chart timeframe.

### Control

All check candles are internally aggregated from M1 and anchored from 20:00 New York.

### Gate

Check candle audit must show exact expected open/close times.

---

## 3. Duplicate Entry Risk

### Risk

The same divergence can be entered twice after restart or repeated check candles.

### Control

Every candidate and signal has deterministic IDs and is persisted in the daily journal.

### Gate

Restart tests must prove no duplicated trades.

---

## 4. Late Entry Risk

### Risk

If the EA was off at the exact entry moment, it could enter later at a worse stop structure.

### Control

Late entry is forbidden. If the EA missed the entry time, the signal is audit-only and no trade is placed.

### Gate

Downtime tests must prove no delayed entry.

---

## 5. Ambiguous Same-Candle Outcome Risk

### Risk

A candle can touch SL and TP in the same interval, making the path unknowable.

### Control

Outcome is recorded as `AMBIGUOUS`, not forced into win or loss.

### Gate

Journals must preserve ambiguous status.

---

## 6. Reference Selection Risk

### Risk

Multiple references can produce different stops.

### Control

The selected reference is the one that creates the largest stop distance on the clean/traded symbol.

### Gate

Reference selector must print all candidate references and selected reference in audit.

---

## 7. Broker Volume Risk

### Risk

The theoretical volume can exceed broker limits.

### Control

The EA calculates theoretical volume, then creates a broker-aware plan. Oversized volume may be split in Auto Trade mode.

### Gate

The trade plan journal must include theoretical volume, broker max, final order count, and adjusted volume.

---

## 8. Hard Close Failure Risk

### Risk

A position may remain open after 15:30 New York due to EA downtime, broker rejection, or platform failure.

### Control

Hard close recovery runs at the first opportunity and retries every configured interval.

### Gate

No EA-owned position may remain open after hard close recovery succeeds.

---

## 9. Manual Position Interference Risk

### Risk

EA could accidentally manage manual trades or other strategy positions.

### Control

The EA manages only its own magic-number positions.

### Gate

Manual positions on Symbol1/Symbol2 must be ignored.

---

## 10. Drawing Logic Contamination Risk

### Risk

Visualization could accidentally influence strategy logic.

### Control

Renderer is audit-only and receives already-finalized state objects.

### Gate

Disabling drawing must not change any journal output.

---

## 11. Monolithic Code Risk

### Risk

A large EA file becomes hard to debug and impossible to validate.

### Control

Implementation is split into small modules and patches.

### Gate

The EA file must remain a lifecycle wrapper, not the strategy logic container.

---

## 12. Data Completeness Risk

### Risk

One symbol can be missing candles while the other appears valid, creating false SMT.

### Control

Both symbols must pass data completeness checks for any decision.

### Gate

Missing data must create a no-trade journal reason.

