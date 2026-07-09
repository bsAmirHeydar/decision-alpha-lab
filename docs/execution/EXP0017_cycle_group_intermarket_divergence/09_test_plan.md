# 09 — Test Plan

## 1. Purpose

Validate the independent CG Intermarket Divergence EA before live trading.

The test plan covers:

- time conversion;
- cycle construction;
- hunt detection;
- divergence confirmation;
- drawing;
- risk sizing;
- cycle-end exits;
- same-day reset.

## 2. Unit-level tests

### 2.1 Time conversion

Cases:

| Broker time | Broker UTC | NY UTC | Expected NY time |
|---|---:|---:|---|
| 2026-07-09 21:00 | +3 | -4 | 2026-07-09 14:00 |
| 2026-07-10 04:00 | +3 | -4 | 2026-07-09 21:00 |
| 2026-12-10 04:00 | +3 | -5 | 2026-12-09 20:00 |

Expected:

- broker to NY mapping is deterministic;
- trading-day key follows 18:00 NY anchor;
- daylight saving is controlled by input.

### 2.2 Trading-day key

Cases:

| NY time | Expected trading day |
|---|---|
| 17:59 | previous day or outside new day depending exact date |
| 18:00 | current calendar date |
| 23:59 | current calendar date |
| 00:01 | previous calendar date |
| 16:59 | previous calendar date |
| 17:00 | outside active day / end boundary |

### 2.3 Cycle index

For `cg_30m`:

| NY time | Expected cycle |
|---|---:|
| 18:00 | 0 |
| 18:29 | 0 |
| 18:30 | 1 |
| 18:59 | 1 |
| 19:00 | 2 |

For `cg_180m`:

| NY time | Expected cycle |
|---|---:|
| 18:00 | 0 |
| 20:59 | 0 |
| 21:00 | 1 |
| 23:59 | 1 |
| 00:00 | 2 |

### 2.4 Final partial cycles

For `cg_720m`:

| Cycle | Start NY | End NY | Duration |
|---:|---|---|---:|
| 0 | 18:00 | 06:00 | 720m |
| 1 | 06:00 | 17:00 | 660m |

Expected:

- final cycle exists;
- final target is 17:00 NY;
- no cycle extends beyond 17:00.

## 3. Hunt detection tests

### 3.1 Equal high hunt

Reference high:

```text
100.00
```

Current high:

```text
100.00
```

Expected:

```text
high_hunt = true
```

### 3.2 Cross high hunt

Reference high:

```text
100.00
```

Current high:

```text
100.01
```

Expected:

```text
high_hunt = true
```

### 3.3 No high hunt

Reference high:

```text
100.00
```

Current high:

```text
99.99
```

Expected:

```text
high_hunt = false
```

### 3.4 Equal low hunt

Reference low:

```text
100.00
```

Current low:

```text
100.00
```

Expected:

```text
low_hunt = true
```

## 4. Divergence matrix tests

### 4.1 Bearish divergence A hunts

```text
A high hunt = true
B high hunt = false
```

Expected:

```text
side = SELL
hunter = A
clean = B
trade_symbol = B
SL = B reference high
```

### 4.2 Bearish divergence B hunts

```text
A high hunt = false
B high hunt = true
```

Expected:

```text
side = SELL
hunter = B
clean = A
trade_symbol = A
SL = A reference high
```

### 4.3 Bullish divergence A hunts

```text
A low hunt = true
B low hunt = false
```

Expected:

```text
side = BUY
hunter = A
clean = B
trade_symbol = B
SL = B reference low
```

### 4.4 Bullish divergence B hunts

```text
A low hunt = false
B low hunt = true
```

Expected:

```text
side = BUY
hunter = B
clean = A
trade_symbol = A
SL = A reference low
```

### 4.5 Both hunt

Expected:

```text
no divergence
```

### 4.6 Neither hunts

Expected:

```text
no divergence
```

## 5. Candle close tests

The EA must not create signals from open candle shift 0.

Procedure:

1. Watch a candle intrabar touch a reference level on one symbol.
2. Confirm that no trade is sent before candle close.
3. After candle close, confirm that the signal is processed once.

Expected:

```text
no intrabar trade
one post-close signal
```

## 6. Drawing tests

### 6.1 Draw enabled

Given CG draw ON and global drawing ON:

Expected:

- line object created;
- object name contains CG, side, hunter, clean, bar time;
- color matches CG color input;
- no duplicate object on later ticks.

### 6.2 Draw disabled per CG

Given CG draw OFF:

Expected:

- no line object;
- signal can still trade if trade ON.

### 6.3 Wrong chart symbol

If hunter symbol is not the attached chart symbol:

Expected baseline:

- do not draw price line on wrong scale;
- log/draw text only if implemented;
- no crash.

## 7. Trade input tests

### 7.1 Trade enabled

Given global trading ON and CG trade ON:

Expected:

- valid signal produces order attempt;
- order uses clean symbol;
- SL equals clean reference level;
- scheduled exit equals current cycle end.

### 7.2 Trade disabled per CG

Given CG trade OFF:

Expected:

- signal is logged/drawn;
- no order sent.

### 7.3 Global trading disabled

Given global trading OFF:

Expected:

- no order for any CG;
- detection and drawing can continue.

## 8. Risk tests

### 8.1 Valid risk geometry

Buy signal:

```text
entry > SL
```

Expected:

- volume calculated;
- order allowed if lots valid.

Sell signal:

```text
entry < SL
```

Expected:

- volume calculated;
- order allowed if lots valid.

### 8.2 Invalid risk geometry

Buy signal:

```text
entry <= SL
```

Expected:

- skip trade;
- log invalid stop geometry.

Sell signal:

```text
entry >= SL
```

Expected:

- skip trade;
- log invalid stop geometry.

## 9. Cycle-end exit tests

Procedure:

1. Generate signal in `cg_30m` cycle ending 18:30 NY.
2. Confirm entry before 18:30.
3. At or after 18:30, EA closes position.

Expected:

```text
position closed by scheduled cycle-end manager
```

Restart recovery:

1. Open position with scheduled exit 18:30.
2. Turn off EA before 18:30.
3. Restart after 18:35.

Expected:

```text
EA closes expired position immediately after restart/tick
```

## 10. Same-day reset tests

At new 18:00 NY day:

Expected:

- duplicate signal keys from prior day are cleared;
- previous day references are not used;
- cycle index resets to 0;
- first cycle has no reference and cannot produce signal.

## 11. Performance tests

Attach EA on M1 with all 21 CGs enabled.

Expected:

- only process on new closed bars;
- no full-history scan on every tick;
- no chart object duplication;
- no excessive log spam.

## 12. Acceptance criteria

The first code implementation is accepted only if:

1. All CGs exist with independent trade/draw/color inputs.
2. Time conversion uses broker UTC and NY UTC inputs.
3. Cycle groups start from 18:00 NY.
4. Day ends at 17:00 NY.
5. Hunt is inclusive touch-only.
6. Divergence confirms only after candle close.
7. Trade symbol is clean symbol.
8. Stop is clean reference level.
9. Exit is scheduled at current cycle end.
10. Risk is 1% equity.
11. No previous-day reference is used.
12. Drawing line is duplicate-safe.
13. The code is modular, not one giant EA file.

