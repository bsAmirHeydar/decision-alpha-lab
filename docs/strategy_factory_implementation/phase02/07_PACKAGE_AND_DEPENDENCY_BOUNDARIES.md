# Package and Dependency Boundaries

## MQL5 Packages

- `Contracts` — stable records and codecs.
- `Core` — runtime-neutral enums, config, state and audit envelope.
- `Ports` — interfaces used by the runtime.
- `Runtime` — orchestration through ports.
- `Adapters` — concrete implementations.
- `Testing` — fixtures and assertions.
- `Experts` — composition roots only.

## Rules

Contracts never import Runtime. Core never imports Adapters. Ports never depend on concrete strategies. Runtime never imports strategy-specific folders. Adapters do not call one another directly. Host code is allowed to import Runtime and selected adapters.

The machine-readable rules live in `dependency_rules.json` and are checked by Python tests.
