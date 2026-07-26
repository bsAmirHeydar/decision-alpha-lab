# Phase Charter and Authority Model

## Objective

Create a stable, versioned, deterministic contract layer that lets MQL5 anatomy engines emit events and runtime context while Python consumes exactly the same information for statistics, training, anti-overfit validation, and reporting.

## Authority hierarchy

1. **MQL5 runtime semantics are primary.** The terminal observes bars, ticks, broker state, event lifecycles, and decision-time context.
2. **Machine-readable schemas define the wire agreement.** They are generated and reviewed with the MQL5 contracts in mind.
3. **Python mirrors the contracts.** Python may reject invalid MQL5 artifacts, but it may not reinterpret their meaning.
4. **Documentation explains the contract.** Documentation cannot silently override code or registry versions.

## Why MQL5-first

The final system must decide and execute inside MetaTrader. Any contract that is elegant in Python but expensive, ambiguous, or impossible in MQL5 is the wrong foundation. Therefore the primary types use MQL5-compatible primitives: `string`, `long`, `double`, `bool`, enums, structs, and small classes. Dynamic behavior is limited. Identity generation, timestamp ordering, and validation can run without Python.

## Strict boundary

MQL5 owns runtime event creation, causal timestamps, feature snapshots, pre-trade decisions, risk checks, paper/live execution state, and telemetry. Python owns heavy research, broad candidate search, labeling, statistical tests, walk-forward training, anti-overfit analysis, model selection, and report generation. Models are exported back to MQL5 only through a later versioned model artifact contract.

## Phase gate

Phase 01 is accepted only when the Python suite passes, the MQL5 compatibility scan reports no errors, registry validation passes, cross-language stable IDs match golden vectors, and MetaEditor compilation instructions are present. Actual MetaEditor compilation must be run on a Windows terminal environment because this build environment has no MetaEditor compiler.
