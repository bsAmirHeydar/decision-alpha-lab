# Level 14 — Paper Live Alerts / No-Order Monitoring Layer

Status: implemented as an audit-only monitoring layer.

Level 14 adds the first operator-facing live monitoring layer for EXEC001 STC SMT Cycles. It does not send broker orders, does not modify broker positions, and does not change any strategy decision. It only observes the already-built paper pipeline and emits alerts when new audit rows appear in the signal, paper entry, paper outcome, partial, or hard-close layers.

## Purpose

The previous levels already build the full paper chain:

1. New York STC time and M/W cycles.
2. Check candle aggregation from M1.
3. W level construction.
4. Previous-W hunt detection.
5. SMT candidate conversion.
6. Closed-check signal registry and consumption.
7. Paper entry planning.
8. Paper outcome simulation.
9. Paper partial simulation.
10. Paper hard-close accounting.
11. Same-day persistence and restart recovery.
12. Audit drawing.

Level 14 turns that pipeline into a practical paper-live monitor. When the EA is attached in `PAPER_LIVE` mode, the operator can receive alerts for meaningful new paper events without enabling real order execution.

## Non-goals

Level 14 intentionally does not:

- open real orders,
- close real positions,
- partially close broker volume,
- retry broker hard closes,
- change stop loss or take profit on the server,
- override the signal registry,
- create late entries,
- replay old same-day signals after restart by default.

## Runtime modes

Alert transport is enabled only when the runtime mode is:

- `PAPER_LIVE`, or
- `AUTO_TRADE`.

In `RESEARCH_BACKTEST`, the pipeline still writes CSV audits, but popup/push/sound alert transport is suppressed. This prevents a historical backfill from spamming the terminal.

## Alert channels

The alert module monitors these already-existing counters:

- Level 07 signal registry rows.
- Level 08 paper entry rows.
- Level 09 paper outcome rows.
- Level 10 partial action rows.
- Level 11 hard-close action rows.

When any monitored counter increases, the module emits a concise no-order alert and writes an audit row.

## Alert types

### `SIGNAL_CONFIRMED`

A new Level 07 signal registry row was produced. This means a closed check candle created a consumed signal or rejection state. The signal registry remains the source of truth.

### `PAPER_ENTRY_PLANNED`

A new Level 08 paper entry row was produced. This means the system planned a no-order paper entry using the next check-candle open and calculated entry, SL, TP, risk, and paper volume.

### `PAPER_OUTCOME_UPDATE`

A new Level 09 outcome row was produced. The operator must inspect `stc_level14_paper_outcomes.csv` to see whether the status is TP, SL, ambiguous, or unresolved.

### `PAPER_PARTIAL_ACTION`

A new Level 10 partial action row was produced. This is an audit-only paper partial. No broker volume is closed in Level 14.

### `PAPER_HARD_CLOSE_ACTION`

A new Level 11 hard-close row was produced. This is an audit-only 15:30 New York paper hard-close accounting event. No broker position is closed in Level 14.

## Initialization baseline

By default, Level 14 does not alert old rows that were reconstructed during EA initialization.

The initialization sequence is:

1. Restore current-day persistence snapshot when allowed.
2. Rebuild all current-day audit layers.
3. Initialize the alert baseline to the current row counts.
4. Start alerting only for new rows after initialization.

This prevents an EA restart from replaying old paper entries or outcomes as fresh operator alerts.

The input `InpAlertReplayOnInit` can override this behavior. The default is `false`.

## Alert audit file

Level 14 writes:

`stc_level14_paper_live_alerts.csv`

Each row includes:

- server time,
- New York time,
- STC day id,
- runtime mode,
- run id,
- symbol pair,
- magic number,
- alert type,
- previous counter,
- current counter,
- delta count,
- transport allowed flag,
- transport used flag,
- popup/push/sound/print configuration,
- check index,
- M cycle,
- W cycle,
- baseline status,
- message,
- rule note.

## Inputs

- `InpEnablePaperLiveAlerts`: master alert switch.
- `InpWriteAlertAudit`: write `stc_level14_paper_live_alerts.csv`.
- `InpAlertPopup`: use terminal popup alerts.
- `InpAlertPush`: use MetaTrader push notifications when configured.
- `InpAlertSound`: play the configured sound file.
- `InpAlertPrint`: print alert messages to the Experts log.
- `InpAlertSoundFile`: sound file name, default `alert.wav`.
- `InpAlertDebounceSeconds`: minimum spacing between alert transports.
- `InpAlertOnSignal`: alert new signal registry rows.
- `InpAlertOnPaperEntry`: alert new paper entry rows.
- `InpAlertOnOutcome`: alert new paper outcome rows.
- `InpAlertOnPartial`: alert new paper partial rows.
- `InpAlertOnHardClose`: alert new paper hard-close rows.
- `InpAlertOnAmbiguous`: include outcome-alert monitoring for ambiguous outcomes.
- `InpAlertOnHardCloseDue`: include hard-close alert monitoring.
- `InpAlertReplayOnInit`: replay already-reconstructed rows on init. Default false.

## Acceptance criteria

Level 14 is accepted when:

1. The EA still compiles with all previous layers.
2. `PAPER_LIVE` mode emits alerts only for rows created after initialization.
3. `RESEARCH_BACKTEST` mode writes audits but does not transport popup/push/sound alerts.
4. No real order function is called.
5. No strategy decision differs from Level 13.
6. `stc_level14_paper_live_alerts.csv` records all alert decisions and suppression reasons.
