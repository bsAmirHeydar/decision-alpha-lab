# Stage 01 → Stage 02 Handoff

## What Stage 01 gives Stage 02

- clean lifecycle
- sample event loader
- event store
- normalized helper functions
- broker GMT base conversion
- chart object naming discipline
- dashboard shell
- timeline shell
- alert key registry

## What Stage 02 must add

Stage 02 should turn the sample pipeline into a stronger simulation engine:

1. richer event types
2. deterministic sample scenarios
3. multiple currencies per day
4. event status transitions
5. past/upcoming/released simulation
6. stress-test day with 40+ events
7. event ID stability model
8. duplicate detection
9. actual/forecast/previous display contract
10. event-store validation report

## Do not jump directly to Forex Factory

The direct adapter should wait until the product can fully render, filter, and alert against a stable event store. Otherwise parser bugs and UI bugs become mixed.
