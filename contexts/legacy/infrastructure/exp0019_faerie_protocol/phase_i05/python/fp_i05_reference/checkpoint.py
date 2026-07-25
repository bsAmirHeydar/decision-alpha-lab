from __future__ import annotations
import json
from .canonical import canonical_json,canonical_sha256,stable_id
from .contracts import WindowStoreCheckpoint
from .constants import CHECKPOINT_VERSION
from .enums import CacheDisposition

def make_checkpoint(snapshot,created_utc_ms):
    payload=canonical_json(snapshot)
    material={'version':CHECKPOINT_VERSION,'config':snapshot.config_hash,'revision':snapshot.source_revision_id,'snapshot':snapshot.semantic_hash,'payload_hash':canonical_sha256(payload)}
    return WindowStoreCheckpoint(stable_id('FPCHECKPOINT',material,32),CHECKPOINT_VERSION,snapshot.config_hash,snapshot.source_revision_id,snapshot.semantic_hash,canonical_sha256(payload),created_utc_ms),payload

def validate_checkpoint(checkpoint,payload,config_hash,source_revision_id):
    if checkpoint.checkpoint_version!=CHECKPOINT_VERSION:return CacheDisposition.REBUILD_REQUIRED,'FP_RRC_CHECKPOINT_VERSION_MISMATCH'
    if checkpoint.config_hash!=config_hash:return CacheDisposition.REBUILD_REQUIRED,'FP_RRC_CHECKPOINT_CONFIG_MISMATCH'
    if checkpoint.source_revision_id!=source_revision_id:return CacheDisposition.REBUILD_REQUIRED,'FP_RRC_CHECKPOINT_REVISION_MISMATCH'
    if canonical_sha256(payload)!=checkpoint.payload_hash:return CacheDisposition.REJECTED,'FP_RRC_CHECKPOINT_PAYLOAD_CORRUPT'
    return CacheDisposition.ACCEPTED,'FP_RRC_CHECKPOINT_ACCEPTED'
