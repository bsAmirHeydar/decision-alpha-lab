# Mandatory broker preflight

## Purpose

This note specifies **mandatory broker preflight** for the MQL5-first Strategy Factory live boundary.

## Canonical rule

Phase 18 is fail-closed. A Phase 16 intent remains only paper-eligible; live elevation is granted by an exact, short-lived Phase 18 release and authorization bound to one account, server, symbol, strategy generation, model release and policy set. No inference score, strategy preference or operator convenience can bypass a hard safety gate.

## Runtime implications

The MQL5 mutation path uses typed structures, bounded arrays and direct calls. The broker port is checked only after identity, lineage, time, account, quote, spread, volume, risk, loss, exposure, order-count, position-count, kill-switch and circuit-breaker gates pass. `OrderCheck` must succeed before the isolated adapter may call `OrderSend`.

## Evidence

Every accepted or rejected transition appends a monotonic live transaction record. Release hash, authorization hash, intent hash, request identity, retcode class, account identity and event timestamp remain available for reconciliation. Python provides only an offline conformance mirror and cannot mutate a broker account.

## Failure posture

Unknown retcodes, malformed inputs, stale snapshots, mismatched lineage, exhausted authorization, capacity exhaustion and permission ambiguity are rejections. Recovery requires explicit evidence and, for micro-live, a new authorization rather than implicit retry.

## Result interpretation

The adapter treats the API boolean and the check result separately. A successful `OrderCheck` basic verification returns `true`, while the canonical successful check result uses retcode `0`. Trade-server send success codes such as placed, done, and done-partial are evaluated only for `OrderSend`. This distinction is encoded in the Phase 18 retcode map and its golden tests.
