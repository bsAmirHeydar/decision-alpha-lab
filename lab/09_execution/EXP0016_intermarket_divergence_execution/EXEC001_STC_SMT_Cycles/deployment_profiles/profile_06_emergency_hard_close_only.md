# Profile 06 — Emergency Hard Close Only

## Intent

Close remaining STC-managed positions after 15:30 New York without allowing new entries.

## Required behavior

Disable:

- STC entry.
- Real auto-entry.
- Real partial close.

Enable:

- Broker position manager.
- Real hard close finalizer.

## Important constraints

The finalizer must only close positions that:

1. are on Symbol1 or Symbol2;
2. match the configured magic number;
3. are still open after the STC hard-close threshold.

Manual or foreign positions must never be closed.

## Use cases

Use this profile when:

- the EA was restarted after 15:30;
- managed positions remain open unexpectedly;
- auto-entry must stay disabled while cleanup is performed;
- the operator wants finalizer-only behavior.

## Acceptance criteria

The profile passes when all matching magic-number positions are closed or clearly reported as requiring manual review after retry cap.

