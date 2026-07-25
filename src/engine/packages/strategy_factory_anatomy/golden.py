from __future__ import annotations
import json,hashlib
from pathlib import Path
from .contracts import GoldenLedgerManifest

def sha256_file(path:Path)->str:
    h=hashlib.sha256();h.update(path.read_bytes());return 'sha256_'+h.hexdigest()
def load_manifest(path:Path)->GoldenLedgerManifest:
    d=json.loads(path.read_text(encoding='utf-8'))
    m=GoldenLedgerManifest(case_id=d['case_id'],plugin_id=d['plugin_id'],plugin_version=d['plugin_version'],input_fixture_hash=d['input_fixture_hash'],expected_observation_ids=tuple(d['expected_observation_ids']),expected_event_ids=tuple(d['expected_event_ids']),expected_record_count=int(d['expected_record_count']))
    m.validate();return m
def verify_fixture(manifest:GoldenLedgerManifest,fixture:Path)->None:
    actual=sha256_file(fixture)
    if actual!=manifest.input_fixture_hash:raise ValueError(f'fixture hash mismatch: {actual}')
