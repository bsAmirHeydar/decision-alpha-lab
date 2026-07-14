from dataclasses import replace
from fp_i13_release import *
from fp_i13_release.replay import ReplayReducer
def _cp(fixture,instance):
 r=ReplayReducer(fixture,instance)
 for e in fixture.events[:20]:r.apply(e)
 return build_checkpoint(r)
def test_checkpoint_restores(fixture,instance): assert validate_checkpoint(_cp(fixture,instance),fixture,instance).disposition==CheckpointDisposition.RESTORED
def test_version_mismatch(fixture,instance): assert validate_checkpoint(replace(_cp(fixture,instance),version='9'),fixture,instance).disposition==CheckpointDisposition.REJECT_VERSION
def test_config_mismatch(fixture,instance): assert validate_checkpoint(replace(_cp(fixture,instance),config_hash='1'*64),fixture,instance).disposition==CheckpointDisposition.REJECT_CONFIG
def test_instance_mismatch(fixture,instance,config_hash):
 other=build_instance_identity(2,'/terminal/a','PAIR-ES-NQ','FP-EPOCH-1',config_hash);assert validate_checkpoint(_cp(fixture,instance),fixture,other).disposition==CheckpointDisposition.REJECT_INSTANCE
def test_payload_mismatch(fixture,instance): assert validate_checkpoint(replace(_cp(fixture,instance),payload_hash='1'*64),fixture,instance).disposition==CheckpointDisposition.REJECT_HASH
