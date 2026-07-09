feat(gartal-terminal): implement stage 01 compile-safe core skeleton

- implement compile-safe MQL5 indicator lifecycle for gartal terminal
- add runtime state, config loading, validation, diagnostics, and timer-driven orchestration
- add stable event store structs, impact/data/status constants, and alert state memory
- add safe string normalization helpers for MQL5 StringToUpper/StringToLower usage
- add broker GMT detection and base time conversion helpers
- add deterministic sample news pipeline as the default Stage 01 data mode
- add dashboard shell with source status, GMT, event counts, next event, and event rows
- add vertical line renderer and bottom timeline shell for sample events
- add alert threshold skeleton with duplicate alert-key protection
- keep Forex Factory WebRequest/parser paths isolated and non-production for later stages
- add detailed English Obsidian documentation, Stage 01 implementation index, canvas, and core skeleton specification
