from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
idx=ROOT/'releases/history/saed/indexes/SAED_V4_03_FILE_INDEX.txt'
allowed=(
'src/engine/packages/saed_v4_event_model/',
'tests/legacy/strategy_factory/v1/phase_saed_v4_03_continuous_time_event_model/',
'schemas/legacy/strategy_factory/saed_v4_03/',
'examples/legacy/strategy_factory/saed_v4_03/',
'tests/fixtures/legacy/strategy_factory/saed_v4_03/',
'releases/history/strategy_factory/artifacts/saed_v4_03/',
'releases/history/strategy_factory/artifacts/SAED_V4_03_',
'releases/history/strategy_factory/program/status/SAED_V4_03',
'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_03/',
'docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_03/',
'src/engine/tooling/strategy_factory/saed_v4_03/',
'mql5/Include/AlphaLab/StrategyFactory/SAEDV4EventModel/',
'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics/EXP_SAED_V4_03_',
'README_SAED_V4_03_','INSTALL_SAED_V4_03_','EXPAND_REMOVE_SAED_V4_03_','SAED_V4_03_','COMMIT_MESSAGE.md')
paths=[x.strip() for x in idx.read_text().splitlines() if x.strip()]
bad=[p for p in paths if not p.startswith(allowed)]
if bad:raise SystemExit('boundary violation: '+','.join(bad))
print(f'boundary validation passed for {len(paths)} files')
