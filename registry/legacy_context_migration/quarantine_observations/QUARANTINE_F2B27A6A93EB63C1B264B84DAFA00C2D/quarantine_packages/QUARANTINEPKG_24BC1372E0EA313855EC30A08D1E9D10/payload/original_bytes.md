# Profile 01 — Research Backtest Full Audit

## Intent

Historical validation with all audit outputs and no broker interaction.

## Required mode

- Runtime mode: Research Backtest.

## Real transports

All real transports must be disabled:

- Real auto-entry: disabled.
- Broker position manager: disabled or harmless if only audit is needed.
- Real partial close: disabled.
- Real hard close finalizer: disabled.
- Paper Live real-action overrides: disabled.

## Recommended audit settings

Enable:

- time audit;
- check candle audit;
- W level audit;
- hunt audit;
- SMT candidate audit;
- signal registry audit;
- paper entry audit;
- paper outcome audit;
- paper partial audit;
- paper hard close audit;
- persistence snapshot;
- validation reports.

Alerts should not fire for historical backfill.

## Expected output

The operator should review:

- validation summary;
- time audit;
- W levels;
- reference hunts;
- SMT candidates;
- signal registry;
- paper entries;
- paper outcomes;
- partial actions;
- hard close actions.

## Acceptance criteria

This profile passes when reports are internally consistent and no real broker action occurs.

