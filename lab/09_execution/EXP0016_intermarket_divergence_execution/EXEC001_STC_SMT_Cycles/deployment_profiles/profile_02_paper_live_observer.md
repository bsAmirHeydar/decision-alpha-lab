# Profile 02 — Paper Live Observer

## Intent

Run the live STC logic without broker interaction.

## Required mode

- Runtime mode: Paper Live.

## Real transports

Disabled:

- Real auto-entry.
- Real partial close.
- Real hard close finalizer.
- Broker close actions.

Broker position manager should normally be off in this profile.

## Alerts

Enable:

- signal alerts;
- paper entry alerts;
- paper outcome alerts;
- partial paper alerts;
- hard close paper alerts;
- ambiguity alerts.

Disable replay-on-init unless debugging.

## Drawing

Drawing should normally be enabled so that the operator can visually compare:

- M/W boundaries;
- W high/low levels;
- check candle state;
- entry/SL/TP;
- partial and hard close markers.

## Acceptance criteria

This profile passes when live alerts match the CSV rows and no real broker action occurs.

