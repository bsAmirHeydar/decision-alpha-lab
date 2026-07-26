# Profile 03 — Paper Live Broker Audit

## Intent

Live paper monitoring with broker position visibility, but still no real trade management.

## Required mode

- Runtime mode: Paper Live.

## Broker position manager

Enable broker position manager only for scanning and audit.

Real close actions remain disabled.

## Real transports

Disabled:

- Real auto-entry.
- Real partial close.
- Real hard close finalizer.
- Paper Live real-action overrides.

## What to verify

The operator should verify:

1. Positions on Symbol1/Symbol2 with the configured magic number are classified as STC-managed.
2. Positions on Symbol1/Symbol2 with other magic numbers are classified as foreign.
3. Foreign positions are never closed.
4. Positions on other symbols are ignored.
5. Broker position rows match actual terminal positions.

## Acceptance criteria

This profile passes when broker classification is correct and no real close/send action occurs.

