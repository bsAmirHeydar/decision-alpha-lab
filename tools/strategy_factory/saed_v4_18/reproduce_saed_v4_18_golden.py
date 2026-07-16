from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_causal_treatment_policy_value.service import build_reference_bundle
load=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
b=build_reference_bundle(load('lab/11_strategy_factory/artifacts/saed_v4_17/V4_17_TO_V4_18_HANDOFF.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_17/GOLDEN_CHECKPOINT_REGISTRY.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_17/GOLDEN_INTEGRITY_RECEIPT.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_17/GOLDEN_CLAIM_TIER_REPORT.JSON'),load('lab/11_strategy_factory/examples/saed_v4_18/reference_treatment_registry.json'),load('lab/11_strategy_factory/examples/saed_v4_18/reference_outcome_spec.json'),load('lab/11_strategy_factory/examples/saed_v4_18/reference_identification_plan.json'),load('lab/11_strategy_factory/examples/saed_v4_18/reference_estimator_catalog.json'),load('lab/11_strategy_factory/examples/saed_v4_18/reference_policy_catalog.json'),load('lab/11_strategy_factory/examples/saed_v4_18/reference_compute_exposure_budget.json'))
checks={'policy_value_report':'GOLDEN_POLICY_VALUE_REPORT.JSON','tournament':'GOLDEN_POLICY_TOURNAMENT.JSON','checkpoint_registry':'GOLDEN_CHECKPOINT_REGISTRY.JSON','claim_tier_report':'GOLDEN_CLAIM_TIER_REPORT.JSON','handoff':'V4_18_TO_V4_19_HANDOFF.JSON'}
for key,name in checks.items():assert b[key]==load('lab/11_strategy_factory/artifacts/saed_v4_18/'+name),key
print(f'SAED V4-18 golden reproduction passed: {len(checks)} decision-equivalent outputs')
