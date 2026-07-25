from __future__ import annotations
from dataclasses import replace
from .contracts import *
from .canonical import sha256,stable_id
from .constants import CHECKPOINT_VERSION
from .errors import FPI13Error
from .replay import ReplayReducer

def build_checkpoint(reducer:ReplayReducer)->ReplayCheckpoint:
    inv=reducer.inventory()
    body={'version':CHECKPOINT_VERSION,'fixture_id':reducer.fixture.fixture_id,'config_hash':reducer.fixture.config_hash,'instance_id':reducer.instance.instance_id,'processed_sequence':reducer.last_sequence,'event_chain_hash':reducer.chain_hash,'event_hashes':tuple(sorted(reducer.event_hashes.items())),'semantic_payloads':inv.semantic_payloads,'visual_semantics':tuple(sorted(reducer.visual.items())),'alerts':inv.alert_ids,'suppressed_alerts':inv.suppressed_historical_alert_ids,'exports':inv.export_ids,'health_codes':inv.health_codes}
    return ReplayCheckpoint(stable_id('FPCP',body),payload_hash=sha256(body),**body)

def validate_checkpoint(cp:ReplayCheckpoint,fixture:ReplayFixture,instance:InstanceIdentity)->CheckpointValidation:
    if cp.version!=CHECKPOINT_VERSION:return CheckpointValidation(CheckpointDisposition.REJECT_VERSION,'FP_REL_CHECKPOINT_VERSION_MISMATCH',None)
    if cp.fixture_id!=fixture.fixture_id:return CheckpointValidation(CheckpointDisposition.REJECT_FIXTURE,'FP_REL_CHECKPOINT_FIXTURE_MISMATCH',None)
    if cp.config_hash!=fixture.config_hash:return CheckpointValidation(CheckpointDisposition.REJECT_CONFIG,'FP_REL_CHECKPOINT_CONFIG_MISMATCH',None)
    if cp.instance_id!=instance.instance_id:return CheckpointValidation(CheckpointDisposition.REJECT_INSTANCE,'FP_REL_CHECKPOINT_INSTANCE_MISMATCH',None)
    body={'version':cp.version,'fixture_id':cp.fixture_id,'config_hash':cp.config_hash,'instance_id':cp.instance_id,'processed_sequence':cp.processed_sequence,'event_chain_hash':cp.event_chain_hash,'event_hashes':cp.event_hashes,'semantic_payloads':cp.semantic_payloads,'visual_semantics':cp.visual_semantics,'alerts':cp.alerts,'suppressed_alerts':cp.suppressed_alerts,'exports':cp.exports,'health_codes':cp.health_codes}
    if sha256(body)!=cp.payload_hash:return CheckpointValidation(CheckpointDisposition.REJECT_HASH,'FP_REL_CHECKPOINT_PAYLOAD_MISMATCH',None)
    return CheckpointValidation(CheckpointDisposition.RESTORED,'FP_REL_CHECKPOINT_RESTORED',cp)

def restore_reducer(cp:ReplayCheckpoint,fixture:ReplayFixture,instance:InstanceIdentity)->ReplayReducer:
    v=validate_checkpoint(cp,fixture,instance)
    if v.disposition!=CheckpointDisposition.RESTORED: raise FPI13Error(v.reason_code,'checkpoint rejected')
    r=ReplayReducer(fixture,instance);r.last_sequence=cp.processed_sequence;r.chain_hash=cp.event_chain_hash;r.event_hashes=dict(cp.event_hashes);r.semantic=dict(cp.semantic_payloads)
    r.visual=dict(cp.visual_semantics)
    r.alerts=set(cp.alerts);r.suppressed_alerts=set(cp.suppressed_alerts);r.exports=set(cp.exports);r.health=list(cp.health_codes)
    return r
