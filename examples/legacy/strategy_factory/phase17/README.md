# Phase 17 Golden Execution Corpus

The corpus drives the same deterministic lifecycle in Python and MQL5: accept a paper-eligible
limit intent, ignore the first non-triggering quote, fill 0.5 lots on each of two triggering quotes,
open and increase one net paper position, then close the complete position at its target. All state
transitions are represented in an append-only hash chain. No broker order API is used.
