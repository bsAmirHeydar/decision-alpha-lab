from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
from saed_v4_sequence_state_space.service import build_reference_bundle
load=lambda x:json.loads((ROOT/x).read_text())
b,_=build_reference_bundle(load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_TOKEN_STREAMS.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_ENCODER_CHECKPOINT.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_TOKENIZER_SPEC.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_CHECKPOINT_REGISTRY.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_11/V4_11_TO_V4_12_HANDOFF.JSON'),load('examples/legacy/strategy_factory/saed_v4_12/reference_sequence_spec.json'),load('examples/legacy/strategy_factory/saed_v4_12/reference_candidate_catalog.json'),load('examples/legacy/strategy_factory/saed_v4_12/reference_reset_policy.json'))
checks={'GOLDEN_TOURNAMENT.JSON':b['tournament'],'GOLDEN_CHECKPOINT_REGISTRY.JSON':b['checkpoint_registry'],'GOLDEN_DISTILLATION.JSON':b['distillation'],'V4_12_TO_V4_13_HANDOFF.JSON':b['handoff'],'GOLDEN_INTEGRITY_RECEIPT.JSON':b['integrity_receipt']}
for name,doc in checks.items():assert json.loads((ROOT/'releases/history/strategy_factory/artifacts/saed_v4_12'/name).read_text())==doc,name
print(f'V4-12 golden reproduction passed: {len(checks)} critical artifacts')
