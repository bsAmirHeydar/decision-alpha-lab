from fp_i11_visual import *

def test_checkpoint_valid(snapshot,cfg,layout):
 e=VisualProjectionEngine(cfg);e.project(snapshot,layout);inv=e.manager.inventory();c=build_checkpoint(cfg.instance_id,cfg.config_hash,snapshot.snapshot_hash,inv,snapshot.generated_at);assert c.valid(cfg.instance_id,cfg.config_hash)
def test_checkpoint_config_mismatch(snapshot,cfg,layout):
 e=VisualProjectionEngine(cfg);e.project(snapshot,layout);c=build_checkpoint(cfg.instance_id,cfg.config_hash,snapshot.snapshot_hash,e.manager.inventory(),snapshot.generated_at);assert not c.valid(cfg.instance_id,canonical_sha256('bad'))
def test_checkpoint_payload_tamper(snapshot,cfg,layout):
 from dataclasses import replace
 e=VisualProjectionEngine(cfg);e.project(snapshot,layout);c=build_checkpoint(cfg.instance_id,cfg.config_hash,snapshot.snapshot_hash,e.manager.inventory(),snapshot.generated_at);assert not replace(c,payload_hash=canonical_sha256('bad')).valid(cfg.instance_id,cfg.config_hash)
