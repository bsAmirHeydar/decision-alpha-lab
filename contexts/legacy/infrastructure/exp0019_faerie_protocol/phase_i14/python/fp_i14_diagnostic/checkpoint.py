from __future__ import annotations
from dataclasses import replace
from .contracts import *
from .canonical import sha256,stable_id
from .constants import CHECKPOINT_VERSION

def create_checkpoint(run:TraceRun,processed_sequence=None):
    seq=processed_sequence or run.inventory.event_count
    events=tuple(e for e in run.events if e.sequence<=seq)
    hashes=tuple((e.computed_event_id,e.semantic_hash) for e in events)
    body={"version":CHECKPOINT_VERSION,"product":run.product.value,"fixture":run.fixture_id,"config":run.manifest.config_hash,"sequence":seq,"chain":run.inventory.chain_hash if seq==run.inventory.event_count else sha256(hashes),"hashes":hashes,"events":[e.semantic_hash for e in events]}
    pid=stable_id("FPDCP",body)
    return TraceCheckpoint(pid,CHECKPOINT_VERSION,run.product,run.fixture_id,run.manifest.config_hash,seq,body["chain"],hashes,events,sha256(body))

def validate_checkpoint(cp,manifest,fixture_id):
    if cp.version!=CHECKPOINT_VERSION:return CheckpointValidation(CheckpointDisposition.REJECT_VERSION,"FP_DIAG_CHECKPOINT_VERSION_MISMATCH",None)
    if cp.config_hash!=manifest.config_hash:return CheckpointValidation(CheckpointDisposition.REJECT_CONFIG,"FP_DIAG_CHECKPOINT_CONFIG_MISMATCH",None)
    if cp.product!=manifest.product:return CheckpointValidation(CheckpointDisposition.REJECT_PRODUCT,"FP_DIAG_CHECKPOINT_PRODUCT_MISMATCH",None)
    if cp.fixture_id!=fixture_id:return CheckpointValidation(CheckpointDisposition.REJECT_HASH,"FP_DIAG_CHECKPOINT_FIXTURE_MISMATCH",None)
    body={"version":cp.version,"product":cp.product.value,"fixture":cp.fixture_id,"config":cp.config_hash,"sequence":cp.processed_sequence,"chain":cp.chain_hash,"hashes":cp.event_hashes,"events":[e.semantic_hash for e in cp.events]}
    if sha256(body)!=cp.payload_hash:return CheckpointValidation(CheckpointDisposition.REJECT_HASH,"FP_DIAG_CHECKPOINT_HASH_MISMATCH",None)
    return CheckpointValidation(CheckpointDisposition.ACCEPTED,"FP_DIAG_CHECKPOINT_ACCEPTED",cp)
