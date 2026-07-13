# UCE-I16 — Context Onboarding Factory and Legacy Anatomy Migration

This delivery implements a deterministic context scaffolding generator, typed legacy adapters, three bounded migration waves, a reusable per-context tournament template, and a central-engine invariance gate.

## Safety state

- No trading, broker-write, or network authority is introduced.
- Real MQL5 differential parity remains pending local Windows/MetaEditor execution.
- Behavior-changing migration is disabled until parity evidence closes.
- Context packages are additive and may not modify central engine packages without ADR and compatibility review.

## Primary locations

- Python: `lab/11_strategy_factory/python/strategy_factory_onboarding_v3/`
- Schemas: `lab/11_strategy_factory/schemas/v3/onboarding_*.schema.json`
- Tests: `lab/11_strategy_factory/tests/phase_uce_i16_context_onboarding/`
- MQL5: `mql5/Include/AlphaLab/StrategyFactory/ContextOnboarding/`
- Evidence: `lab/11_strategy_factory/implementation_program/universal_context_exploitation_engine/v3_implementation/artifacts/uce_i16/`
- Obsidian delivery: `docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i16/`
