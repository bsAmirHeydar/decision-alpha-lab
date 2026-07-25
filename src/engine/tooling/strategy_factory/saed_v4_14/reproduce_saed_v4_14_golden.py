from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
from saed_v4_foundation_model_adapters.service import build_reference_bundle
load=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
b=build_reference_bundle(load('releases/history/strategy_factory/artifacts/saed_v4_13/V4_13_TO_V4_14_HANDOFF.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_13/GOLDEN_CHECKPOINT_REGISTRY.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_13/GOLDEN_CANDIDATE_EMBEDDINGS.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_13/GOLDEN_COMPILED_MODEL_GRAPH.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_13/GOLDEN_TOURNAMENT.JSON'),load('examples/legacy/strategy_factory/saed_v4_14/reference_adapter_config.json'),load('examples/legacy/strategy_factory/saed_v4_14/reference_model_intake_catalog.json'),load('examples/legacy/strategy_factory/saed_v4_14/reference_candidate_catalog.json'),load('examples/legacy/strategy_factory/saed_v4_14/reference_pretraining_disclosures.json'),load('examples/legacy/strategy_factory/saed_v4_14/reference_domain_shift_policy.json'),load('examples/legacy/strategy_factory/saed_v4_14/reference_compute_exposure_budget.json'))
checks={'upstream_validation':'GOLDEN_UPSTREAM_VALIDATION.JSON','token_sequence':'GOLDEN_TOKEN_SEQUENCE.JSON','tournament':'GOLDEN_TOURNAMENT.JSON','checkpoint_registry':'GOLDEN_CHECKPOINT_REGISTRY.JSON','handoff':'V4_14_TO_V4_15_HANDOFF.JSON'}
for k,f in checks.items():
 assert b[k]==load('releases/history/strategy_factory/artifacts/saed_v4_14/'+f),k
print('SAED V4-14 deterministic golden reproduction passed')
