# Strategy Factory UCEE-I18 — Production Qualification and Release

This patch adds the fail-closed UCE-I18 production-qualification reference layer. It evaluates source integrity, MetaEditor compilation, Python/MQL5 and tester differentials, causal ordering, soak budgets, chaos, restart/recovery, reservation and broker reconciliation, security, prospective paper/shadow, bounded micro-live, rollback and human approval.

The repository reference is deliberately blocked. Synthetic evidence can exercise the fully-qualified branch in tests, but it is explicitly non-production and cannot authorize trading. Real authority remains unavailable until supported Windows/MetaTrader, broker, prospective and human-approval evidence is ingested and accepted.

Primary paths:

- `lab/11_strategy_factory/python/strategy_factory_qualification_v3/`
- `lab/11_strategy_factory/tests/phase_uce_i18_production_qualification/`
- `lab/11_strategy_factory/schemas/v3/qualification_*.schema.json`
- `mql5/Include/AlphaLab/StrategyFactory/Qualification/`
- `docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i18/`
- `tools/strategy_factory/run_uce_i18_tests.ps1`
