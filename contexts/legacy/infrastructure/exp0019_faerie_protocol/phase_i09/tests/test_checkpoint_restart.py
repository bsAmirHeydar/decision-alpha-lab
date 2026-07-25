from dataclasses import replace
from fp_i09_ledger.engine import LedgerEngine
from fp_i09_ledger.checkpoint import create_checkpoint,validate_checkpoint
from fp_i09_ledger.enums import CheckpointDecision
from fp_i09_ledger.rebuild import assert_snapshot_replay_parity
from conftest import signal,gate,eligible

def build(config,qkey):
    e=LedgerEngine(config); a=signal(0); b=signal(1,hunt=a.first_hunt_minute_utc_ms+60_000)
    for s in (b,a): e.ingest(s,gate(s),eligible(s),qkey,s.confirmation_close_utc_ms+600_000)
    return e,e.snapshot(a.confirmation_close_utc_ms+900_000)
def test_checkpoint_accept(config,qkey):
    _,s=build(config,qkey); cp=create_checkpoint(s,'REV-1',s.created_utc_ms); assert validate_checkpoint(cp,config.config_hash,s.chain_head_hash).decision is CheckpointDecision.ACCEPT
def test_config_mismatch_reject(config,qkey):
    _,s=build(config,qkey); cp=create_checkpoint(s,'REV-1',s.created_utc_ms); assert validate_checkpoint(cp,'f'*64,s.chain_head_hash).decision is CheckpointDecision.REJECT_CONFIG
def test_chain_mismatch_reject(config,qkey):
    _,s=build(config,qkey); cp=create_checkpoint(s,'REV-1',s.created_utc_ms); assert validate_checkpoint(cp,config.config_hash,'e'*64).decision is CheckpointDecision.REJECT_CHAIN_HEAD
def test_payload_tamper_reject(config,qkey):
    _,s=build(config,qkey); cp=create_checkpoint(s,'REV-1',s.created_utc_ms); bad=replace(cp,payload_hash='d'*64); assert validate_checkpoint(bad,config.config_hash,s.chain_head_hash).decision is CheckpointDecision.REJECT_HASH
def test_restart_rebuild_parity(config,qkey):
    _,a=build(config,qkey); _,b=build(config,qkey); assert assert_snapshot_replay_parity(a,b)
