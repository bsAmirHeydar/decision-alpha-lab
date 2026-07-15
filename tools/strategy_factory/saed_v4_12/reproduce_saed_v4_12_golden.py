from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_sequence_state_space.service import build_reference_bundle
load=lambda x:json.loads((ROOT/x).read_text())
b,_=build_reference_bundle(load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_TOKEN_STREAMS.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_ENCODER_CHECKPOINT.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_TOKENIZER_SPEC.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_CHECKPOINT_REGISTRY.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_11/V4_11_TO_V4_12_HANDOFF.JSON'),load('lab/11_strategy_factory/examples/saed_v4_12/reference_sequence_spec.json'),load('lab/11_strategy_factory/examples/saed_v4_12/reference_candidate_catalog.json'),load('lab/11_strategy_factory/examples/saed_v4_12/reference_reset_policy.json'))
checks={'GOLDEN_TOURNAMENT.JSON':b['tournament'],'GOLDEN_CHECKPOINT_REGISTRY.JSON':b['checkpoint_registry'],'GOLDEN_DISTILLATION.JSON':b['distillation'],'V4_12_TO_V4_13_HANDOFF.JSON':b['handoff'],'GOLDEN_INTEGRITY_RECEIPT.JSON':b['integrity_receipt']}
for name,doc in checks.items():assert json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_12'/name).read_text())==doc,name
print(f'V4-12 golden reproduction passed: {len(checks)} critical artifacts')
