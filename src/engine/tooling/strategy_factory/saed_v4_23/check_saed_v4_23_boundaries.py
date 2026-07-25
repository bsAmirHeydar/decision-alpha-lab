from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);allowed=['src/engine/packages/saed_v4_offline_policy_research','tests/legacy/strategy_factory/v1/phase_saed_v4_23_offline_policy_research','examples/legacy/strategy_factory/saed_v4_23','releases/history/strategy_factory/artifacts/saed_v4_23','schemas/legacy/strategy_factory/saed_v4_23','src/engine/tooling/strategy_factory/saed_v4_23','docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_23','docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_23','mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_23','mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_23']
# Static source boundary: package must not import broker/runtime or mutate UCEE central engine.
for p in (ROOT/'src/engine/packages/saed_v4_offline_policy_research').glob('*.py'):
    t=p.read_text(encoding='utf-8')
    for bad in ['MetaTrader5','OrderSend','broker_adapter','runtime_compiler','portfolio_allocator','live_execution']:assert bad not in t,p
print('V4-23 authority and central-engine boundary passed')
