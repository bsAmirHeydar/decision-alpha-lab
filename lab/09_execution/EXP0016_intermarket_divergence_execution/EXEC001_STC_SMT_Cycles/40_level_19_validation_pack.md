# Level 19 — Validation Pack / Self-Test Reports

## Purpose

Level 19 adds an audit-only validation layer to EXEC001 STC SMT Cycles. It does not create signals, paper entries, real entries, partial closes, hard closes, or chart drawings. Its purpose is to give the operator a deterministic report that the locked STC rules still match the implementation before the system is trusted in Paper Live or Auto Trade mode.

The validation pack is deliberately separated from the strategy decision path. A validation failure is reported to CSV and runtime events, but the validator itself does not change SMT candidates, signal registry rows, paper entries, order routing, partial management, or hard-close finalization.

## Why this layer exists

The strategy now has many implementation layers: time conversion, STC trading day classification, check candle aggregation, W level building, legal W reference selection, hunt detection, SMT candidate conversion, signal registry, paper entry, paper outcome, partial simulation, hard close simulation, persistence, drawing, alerts, broker management, auto-entry, real partial, and real hard-close finalization.

A regression in any foundational rule could make later layers look correct while actually operating under the wrong calendar, wrong W matrix, wrong hunt semantics, or wrong safety gate. Level 19 creates compact self-test reports so that those invariants can be inspected after each compile, after each attach, and optionally during live monitoring.

## Scope

Level 19 validates these groups:

1. Configuration invariants.
2. STC time and M/W cycle boundaries.
3. No-entry final check candles.
4. Reference matrix rules.
5. Raw hunt pattern semantics.
6. Real transport safety gates.
7. Output-path readiness.

It does not validate broker execution quality, fill slippage, real market liquidity, or whether the strategy is profitable.

## Inputs

The new inputs are:

- `InpEnableValidationPack`
- `InpWriteValidationReports`
- `InpValidationRunOnInit`
- `InpValidationRunOnPulse`
- `InpValidationRunSeconds`
- `InpValidationStrictMode`

Default behavior is safe and non-invasive:

- Validation is enabled.
- Reports are written.
- Validation runs on init.
- Validation does not run repeatedly on every pulse unless enabled.
- Strict mode is off.

## Output files

Level 19 creates two new Common Files CSVs:

- `stc_level19_validation_summary.csv`
- `stc_level19_validation_matrix.csv`

The summary file contains one row per validation run. The matrix file contains one row per individual check.

## Validation suites

### CONFIG

The config suite checks that the strategy id is stable, the symbols are distinct, check timeframe is one of the approved STC values, reward/risk are positive, magic number is positive, and real transport gates are not accidentally open in unsafe modes.

### TIME_MATRIX

The time matrix suite uses synthetic elapsed minutes from the STC 20:00 New York day start. It checks the locked schedule:

- M1: 20:00 to 02:00
- gap: 02:00 to 03:00
- M2: 03:00 to 09:00
- gap: 09:00 to 09:30
- M3: 09:30 to 15:30
- hard-close zone from 15:30 onward

It also checks the final check candle rule. A check candle that closes exactly at the end of an M is audited, but it cannot create an entry.

### REFERENCE_MATRIX

This suite checks:

- W1 has no legal reference and never signals.
- W2 references only W1.
- W3 references W2 and W1.
- W4 references W3, W2, and W1.
- No W compares with itself.

### HUNT_PATTERN

This suite checks the raw hunt pattern classifier:

- no symbol hunts = `NONE`
- only Symbol1 hunts = `SYMBOL1_ONLY`
- only Symbol2 hunts = `SYMBOL2_ONLY`
- both symbols hunt = `BOTH`

The equality-as-touch price rule is already implemented in the hunt detector. This layer verifies the classifier semantics that later SMT layers consume.

## Strict mode

`InpValidationStrictMode` is intentionally not a broker-action safety switch. The validation pack remains audit-only. In strict mode, failures are marked as `FAIL_STRICT` in the reports and runtime events so that the operator can treat them as a hard manual stop before enabling Auto Trade.

## Acceptance criteria

A clean Level 19 attach should produce:

- `validation_status = PASS` or `PASS_WITH_WARNINGS`
- zero failed checks in the summary row
- matrix rows for CONFIG, TIME_MATRIX, REFERENCE_MATRIX, and HUNT_PATTERN
- no change to signal, paper, or real-order behavior

If the validation pack reports a failure, no later auto-trade testing should be trusted until the failing suite is inspected.
