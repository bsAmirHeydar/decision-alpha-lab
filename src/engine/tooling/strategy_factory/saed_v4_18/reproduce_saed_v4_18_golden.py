from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
from saed_v4_causal_treatment_policy_value.service import build_reference_bundle
load=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
b=build_reference_bundle(load('releases/history/strategy_factory/artifacts/saed_v4_17/V4_17_TO_V4_18_HANDOFF.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_CHECKPOINT_REGISTRY.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_INTEGRITY_RECEIPT.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_CLAIM_TIER_REPORT.JSON'),load('examples/legacy/strategy_factory/saed_v4_18/reference_treatment_registry.json'),load('examples/legacy/strategy_factory/saed_v4_18/reference_outcome_spec.json'),load('examples/legacy/strategy_factory/saed_v4_18/reference_identification_plan.json'),load('examples/legacy/strategy_factory/saed_v4_18/reference_estimator_catalog.json'),load('examples/legacy/strategy_factory/saed_v4_18/reference_policy_catalog.json'),load('examples/legacy/strategy_factory/saed_v4_18/reference_compute_exposure_budget.json'))
checks={'policy_value_report':'GOLDEN_POLICY_VALUE_REPORT.JSON','tournament':'GOLDEN_POLICY_TOURNAMENT.JSON','checkpoint_registry':'GOLDEN_CHECKPOINT_REGISTRY.JSON','claim_tier_report':'GOLDEN_CLAIM_TIER_REPORT.JSON','handoff':'V4_18_TO_V4_19_HANDOFF.JSON'}
for key,name in checks.items():assert b[key]==load('releases/history/strategy_factory/artifacts/saed_v4_18/'+name),key
print(f'SAED V4-18 golden reproduction passed: {len(checks)} decision-equivalent outputs')
