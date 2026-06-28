# EXEC001 STC SMT Cycles — Patch Build Sequence

This document defines the exact engineering sequence for implementation patches.

The purpose is to keep each patch small enough to compile, inspect, and debug.

---

## Patch 001 — EA Skeleton, Inputs, and Build Sanity

### Goal

Create the EA shell and core types.

### Adds

- EA file
- config structs
- enums
- inputs
- build sanity logs
- output folder creation
- timer loop
- no-op engine

### Must Not Add

- signal detection
- W logic
- order execution
- chart drawing beyond optional build label

### Acceptance

- compiles with zero errors
- can attach to any chart
- prints all inputs
- confirms Symbol1 and Symbol2 exist

---

## Patch 002 — Time and Cycle Engine

### Goal

Correctly classify New York time into STC day, M, W, gap, and hard-close zones.

### Adds

- time conversion
- New York DST handling
- STC day object
- M/W schedule
- gap classifier
- final check candle classifier
- hard close classifier

### Acceptance

- logs current NY time
- logs active STC day
- logs active M/W/gap state
- test timestamps map correctly

---

## Patch 003 — Check Candle Aggregator

### Goal

Build internal check candles from M1 data.

### Adds

- M1 series fetch for both symbols
- synthetic check candle construction
- 1m, 3m, 5m, 10m, 15m, 30m support
- anchor from 20:00 NY
- check candle journal

### Acceptance

- closed check candles are detected once
- 3m and 10m work without broker-native periods
- data missing creates a journaled no-trade reason

---

## Patch 004 — W Level Builder

### Goal

Build W high/low levels for both symbols.

### Adds

- W level builder
- symbol-specific W storage
- cycle audit CSV
- W coverage validation

### Acceptance

- W levels match chart inspection
- W1 is marked non-signal-producing
- W levels are separate per symbol

---

## Patch 005 — Reference Matrix and Hunt Detector

### Goal

Detect high/low touches against valid prior W references.

### Adds

- W reference matrix
- high hunt logic
- low hunt logic
- equality as touch
- no tolerance

### Acceptance

- W2 references only W1
- W3 references W2 and W1
- W4 references W3, W2, and W1
- W1 creates no signal

---

## Patch 006 — SMT Candidate Engine

### Goal

Detect exactly-one-symbol-hunted SMT candidates.

### Adds

- raw SMT candidate creation
- candidate IDs
- hunted/clean symbol selection
- side mapping
- candidate journal

### Acceptance

- high SMT creates sell candidate
- low SMT creates buy candidate
- clean symbol is the trade symbol
- both-symbol hunt creates no valid candidate

---

## Patch 007 — Confirmation and Signal Registry

### Goal

Confirm candidates at check candle close and prevent duplicate entries.

### Adds

- check close confirmation
- still-valid divergence validation
- Entry OFF audit-only behavior
- simultaneous buy/sell rejection
- final check candle blocking
- consumed signal registry

### Acceptance

- no delayed entry
- no duplicate signal entry
- simultaneous buy/sell is forgotten
- rejected signals include reason codes

---

## Patch 008 — Reference Selection and Risk Plan

### Goal

Turn confirmed signals into trade plans.

### Adds

- largest-stop reference selector
- entry price model
- SL/TP calculation
- Final Reward R multiple
- volume calculation
- broker volume constraints
- split order plan

### Acceptance

- SL uses traded symbol's reference W
- largest stop reference is selected
- 10 Final Reward means 10R
- theoretical and broker-adjusted volume are journaled

---

## Patch 009 — Research Simulator and Journals

### Goal

Simulate trades without real orders.

### Adds

- simulated entry
- simulated SL/TP
- ambiguous outcome handling
- partial close simulation
- hard close simulation
- trade journal
- position action journal
- daily summary journal

### Acceptance

- no order is sent
- trade lifecycle is deterministic
- ambiguous SL/TP stays ambiguous
- no simulated position remains after hard close

---

## Patch 010 — Persistence and Restart Recovery

### Goal

Make the engine restart-safe.

### Adds

- daily journal restore
- consumed signal restore
- partial status restore
- magic-number position restore
- delayed partial recovery
- delayed hard close recovery

### Acceptance

- restart does not duplicate trades
- missed partial is executed after restart
- missed hard close is executed after restart

---

## Patch 011 — Visualization

### Goal

Add audit drawings.

### Adds

- M/W boxes
- W high/low lines
- hunt markers
- SMT markers
- entry/SL/TP drawings
- partial and hard close markers
- dashboard

### Acceptance

- every trade/no-trade can be visually audited
- drawing has no effect on logic
- object cleanup is safe

---

## Patch 012 — Paper Live Mode

### Goal

Run the engine live without real orders.

### Adds

- live check close processing
- paper signal generation
- paper trade lifecycle
- live journals
- live drawings

### Acceptance

- no orders are placed
- paper live behavior matches backtest on same data
- signal timing is exact

---

## Patch 013 — Auto Trade Mode

### Goal

Enable real order execution.

### Adds

- market order sending
- SL/TP placement
- split order execution
- partial close execution
- hard close retry execution
- order failure handling

### Acceptance

- real orders only in Auto Trade mode
- order failure consumes signal but does not increment trade counter
- only magic-number positions are managed
- hard close retries until all EA-owned positions are closed

---

## Patch 014 — Validation Pack

### Goal

Add deterministic validation datasets and expected outputs.

### Adds

- synthetic test cases
- expected cycle audit
- expected signals
- expected trade journals
- comparison scripts if needed

### Acceptance

- regression outputs match expected files
- future changes can be checked against known behavior

