from dataclasses import replace
from fp_i10_indicator import *
from fp_i10_indicator.checkpoint import *

def test_checkpoint_roundtrip(engine):
 c=create_checkpoint(instance=engine.instance,composition=engine.composition,snapshot=engine.snapshot,last_processed_m1=engine.cursor.last_processed_m1,lifecycle_sequence=len(engine.event_chain.events),source_revision_id=engine.snapshot.source_revision_id); v=validate_checkpoint(c,instance=engine.instance,composition=engine.composition); assert v.accepted
def test_config_mismatch(engine,config):
 c=create_checkpoint(instance=engine.instance,composition=engine.composition,snapshot=engine.snapshot,last_processed_m1=engine.cursor.last_processed_m1,lifecycle_sequence=1,source_revision_id='REV'); other=build_instance_identity(build_config(context_epoch='OTHER',primary_symbol='ES',secondary_symbol='NQ'),101,'TERM-A'); assert validate_checkpoint(c,instance=other,composition=engine.composition).accepted is False
def test_payload_tamper(engine):
 c=create_checkpoint(instance=engine.instance,composition=engine.composition,snapshot=engine.snapshot,last_processed_m1=engine.cursor.last_processed_m1,lifecycle_sequence=1,source_revision_id='REV'); bad=replace(c,payload_hash='0'*64); assert validate_checkpoint(bad,instance=engine.instance,composition=engine.composition).accepted is False
def test_restart_restores_cursor(config,modules,engine):
 c=create_checkpoint(instance=engine.instance,composition=engine.composition,snapshot=engine.snapshot,last_processed_m1=engine.cursor.last_processed_m1,lifecycle_sequence=len(engine.event_chain.events),source_revision_id=engine.snapshot.source_revision_id); e=IndicatorEngine(); e.initialize(config=config,chart_id=101,terminal_instance_id='TERM-A',modules=modules,now_m1=engine.snapshot.generated_utc_ms,checkpoint=c); assert e.checkpoint_disposition is CheckpointDisposition.RESTORED
