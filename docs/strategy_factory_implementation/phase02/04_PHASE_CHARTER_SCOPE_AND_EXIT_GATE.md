# Phase Charter, Scope and Exit Gate

## Objective

Create a compiling MQL5-first runtime skeleton that can receive a canonical anatomy event, build an immutable feature snapshot, and write both through a result sink without embedding any strategy logic or order authority.

## In Scope

- Thin Host EA.
- Runtime configuration and run modes.
- Lifecycle state machine.
- Typed bounded audit bus.
- Explicit service ports.
- Null and fixture adapters.
- Event-to-snapshot orchestration.
- Dependency rules.
- Python package bootstrap and engineering mirrors.
- Self-test EA and static tests.

## Out of Scope

- Real market cache.
- DST and session logic.
- Candidate, stop, exit and outcome contracts.
- Paper or live order lifecycle.
- Model inference.
- User interface.

## Exit Gate

Phase 02 exits only when the Host is demonstrably thin, the runtime processes a fixture event into a fixture snapshot, illegal state transitions fail, dependency boundaries are machine checked, no live authority tokens exist, and local MetaEditor compilation is the only remaining environment-dependent validation.
