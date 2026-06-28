# Level 15 — Broker Position Manager / Magic-Only Safety Layer

## Status

Level 15 is the first layer that looks at the real broker account. It does **not** create entries. It does **not** create market orders for STC signals. It does **not** convert the paper entry model into live trading.

Its purpose is narrower and safer:

1. scan real open broker positions,
2. identify only positions belonging to this STC strategy instance,
3. audit those positions into CSV,
4. detect foreign positions on Symbol1/Symbol2,
5. optionally send hard-close orders only for matching magic-number positions after 15:30 New York.

Auto-entry remains disabled in this level.

## Locked safety contract

The broker manager is allowed to manage only positions where all of the following are true:

- the position symbol is exactly `Symbol1` or `Symbol2`,
- the position magic number equals `InpMagicNumber`,
- the strategy instance lock belongs to this same symbol pair and magic number,
- hard close is due after 15:30 New York,
- real hard close is enabled by input,
- runtime mode permits real close transport.

Foreign manual positions or positions from other strategies must never be closed by this level.

## Inputs

### `InpEnableBrokerPositionManager`

Enables real broker position scanning and safety auditing.

Default: `true`.

When disabled, Level 15 does nothing and writes no broker position scan state.

### `InpWriteBrokerPositionAudit`

Writes broker position scan rows into CSV.

Default: `true`.

### `InpBrokerPositionScanSeconds`

Minimum interval between broker position scans.

Default: `10` seconds.

### `InpEnableRealHardClose`

Allows Level 15 to send real broker close requests for managed magic-number positions after 15:30 New York.

Default: `false`.

This is intentionally false because this level is still not the auto-trade layer.

### `InpAllowRealCloseInPaperLive`

Allows real hard-close transport while runtime mode is `PAPER_LIVE`.

Default: `false`.

When false, real hard close can only be armed in `AUTO_TRADE` mode.

### `InpBrokerCloseDeviationPoints`

Deviation used for real broker position close requests.

Default: `30` points.

### `InpAuditForeignPairPositions`

If true, positions on Symbol1/Symbol2 with a different magic number are audited as foreign pair positions.

Default: `true`.

Foreign pair positions are never managed or closed.

## Runtime behavior

### Normal scan

On each broker scan pulse, the engine iterates through `PositionsTotal()` and reads each selected position. It classifies each position into one of three groups.

### Managed position

A position is managed by this STC strategy instance only when:

- symbol is Symbol1 or Symbol2,
- magic number equals the configured STC magic number.

Managed positions are audited and may become eligible for hard close after 15:30 New York if real hard close is explicitly enabled.

### Foreign pair position

A position is foreign when it is on Symbol1 or Symbol2 but magic number does not match.

Foreign positions are audit-only. The system records them so the operator can see contamination or manual exposure, but it does not close them.

### Ignored non-pair position

A position on another symbol is ignored by the strategy.

It is not audited unless future debug modes explicitly request all-account scans.

## Hard close behavior

The SRS says all open STC trades must be closed at 15:30 New York. Level 15 introduces the real broker safety mechanism for that behavior, but keeps it protected behind inputs.

Real hard close is attempted only when:

- current time snapshot says `hard_close_due=true`,
- `InpEnableBrokerPositionManager=true`,
- `InpEnableRealHardClose=true`,
- runtime is `AUTO_TRADE`, or runtime is `PAPER_LIVE` and `InpAllowRealCloseInPaperLive=true`,
- the open position belongs to Symbol1/Symbol2 and has the configured magic number.

If all conditions pass, the engine sends a `PositionClose(ticket)` request through `CTrade`.

If close fails, the result code, comment, and status are written to the broker action CSV. The timer will retry according to the existing hard-close retry cadence.

## Files

Level 15 adds two broker audit files.

### `stc_level15_broker_positions.csv`

One row per scanned managed or foreign pair position.

Important fields:

- server time,
- New York time,
- STC day id,
- ticket,
- position identifier,
- symbol,
- magic,
- position type,
- volume,
- open price,
- current price,
- SL,
- TP,
- floating profit,
- open time,
- update time,
- whether the symbol belongs to the pair,
- whether the magic matches,
- whether the position is managed by STC,
- whether hard close is due,
- scan status.

### `stc_level15_broker_actions.csv`

One row per broker-side safety action or hard-close attempt.

Important fields:

- action type,
- ticket,
- symbol,
- magic,
- action allowed,
- action attempted,
- action succeeded,
- trade result retcode,
- result comment,
- status,
- rule note.

## Acceptance criteria

Level 15 is accepted when:

1. the EA compiles,
2. the broker position audit CSV is created,
3. managed magic positions are detected correctly,
4. foreign Symbol1/Symbol2 positions are audited but never closed,
5. non-pair positions are ignored,
6. hard close does not send real close requests unless the safety inputs explicitly allow it,
7. no auto-entry order is created,
8. real hard close only targets matching magic-number positions.

## What is still deferred

- real entry orders,
- real SL/TP placement for new STC entries,
- real partial close generated from strategy entries,
- live order retry for entries,
- final production auto-trading mode.

Those belong to later levels.
