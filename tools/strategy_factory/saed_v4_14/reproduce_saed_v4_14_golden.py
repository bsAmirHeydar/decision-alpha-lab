from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_foundation_model_adapters.service import build_reference_bundle
load=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
b=build_reference_bundle(load('lab/11_strategy_factory/artifacts/saed_v4_13/V4_13_TO_V4_14_HANDOFF.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_13/GOLDEN_CHECKPOINT_REGISTRY.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_13/GOLDEN_CANDIDATE_EMBEDDINGS.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_13/GOLDEN_COMPILED_MODEL_GRAPH.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_13/GOLDEN_TOURNAMENT.JSON'),load('lab/11_strategy_factory/examples/saed_v4_14/reference_adapter_config.json'),load('lab/11_strategy_factory/examples/saed_v4_14/reference_model_intake_catalog.json'),load('lab/11_strategy_factory/examples/saed_v4_14/reference_candidate_catalog.json'),load('lab/11_strategy_factory/examples/saed_v4_14/reference_pretraining_disclosures.json'),load('lab/11_strategy_factory/examples/saed_v4_14/reference_domain_shift_policy.json'),load('lab/11_strategy_factory/examples/saed_v4_14/reference_compute_exposure_budget.json'))
checks={'upstream_validation':'GOLDEN_UPSTREAM_VALIDATION.JSON','token_sequence':'GOLDEN_TOKEN_SEQUENCE.JSON','tournament':'GOLDEN_TOURNAMENT.JSON','checkpoint_registry':'GOLDEN_CHECKPOINT_REGISTRY.JSON','handoff':'V4_14_TO_V4_15_HANDOFF.JSON'}
for k,f in checks.items():
 assert b[k]==load('lab/11_strategy_factory/artifacts/saed_v4_14/'+f),k
print('SAED V4-14 deterministic golden reproduction passed')
