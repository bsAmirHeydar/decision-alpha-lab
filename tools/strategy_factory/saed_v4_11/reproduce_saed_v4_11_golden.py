from pathlib import Path
import json,sys,tempfile
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_self_supervised_pretraining.service import build_reference_bundle
load=lambda p:json.loads((ROOT/p).read_text())
records=load('lab/11_strategy_factory/examples/saed_v4_11/reference_corpus_records.json');up=load('lab/11_strategy_factory/artifacts/saed_v4_10/GOLDEN_PRETRAINING_CORPUS_MANIFEST.JSON');hand=load('lab/11_strategy_factory/artifacts/saed_v4_10/V4_10_TO_V4_11_HANDOFF.JSON');cfg=load('lab/11_strategy_factory/examples/saed_v4_11/reference_training_config.json');split=load('lab/11_strategy_factory/examples/saed_v4_11/reference_split_policy.json');can=load('lab/11_strategy_factory/examples/saed_v4_11/membership_canaries.json')['tokens']
bundle,streams=build_reference_bundle(records,up,hand,cfg,split,can)
expected=load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_ENCODER_CHECKPOINT.JSON')
assert bundle['checkpoint']['checkpoint_hash']==expected['checkpoint_hash']
assert bundle['training_receipt']['receipt_hash']==load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_TRAINING_RECEIPT.JSON')['receipt_hash']
print(json.dumps({'phase':'SAED_V4_11','passed':True,'checkpoint_hash':expected['checkpoint_hash'],'stream_count':len(streams)},sort_keys=True))
