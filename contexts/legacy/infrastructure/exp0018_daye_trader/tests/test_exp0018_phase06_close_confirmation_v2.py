from __future__ import annotations
from tools.repository_paths import find_repository_root
import csv,json
from pathlib import Path

ROOT=find_repository_root(__file__)
BASE=ROOT/'contexts/legacy/infrastructure/exp0018_daye_trader'

def classify(row):
    if row['missed_close']=='1': return 'MISSED_CLOSE_REPLAY_REQUIRED'
    if row['host_identity_match']!='1' or row['source_available_through_close']!='1': return 'UNAVAILABLE_AT_CLOSE'
    if row['close_pair']=='BOTH': return 'INVALIDATED_DOUBLE_HUNT'
    if row['close_pair']=='NONE': return 'NO_SIGNAL_AT_CLOSE'
    if row['close_pair'] in ('UNAVAILABLE','UNKNOWN'): return 'UNAVAILABLE_AT_CLOSE'
    if row['close_pair']!=row['initial_pair']: return 'INVALIDATED_ROLE_CHANGED'
    return 'CONFIRMED'

def test_contract_authority_boundaries():
    c=json.loads((BASE/'contracts/daye_close_confirmation_contract_v2.json').read_text())
    assert c['execution_authority'] is False
    assert c['drawing_authority'] is False
    assert c['reference_lifecycle_authority'] is False
    assert c['direction_mapping_authority'] is False

def test_golden_outcomes():
    rows=list(csv.DictReader((BASE/'fixtures/daye_close_confirmation_cases_v2.csv').open()))
    assert len(rows)>=12
    for row in rows: assert classify(row)==row['expected_outcome']

def test_double_hunt_never_confirms():
    rows=list(csv.DictReader((BASE/'fixtures/daye_close_confirmation_cases_v2.csv').open()))
    assert all(r['expected_confirmed']=='0' for r in rows if r['close_pair']=='BOTH')

def test_missed_close_requires_replay():
    rows=list(csv.DictReader((BASE/'fixtures/daye_close_confirmation_cases_v2.csv').open()))
    missed=[r for r in rows if r['missed_close']=='1']
    assert missed and all(r['expected_outcome']=='MISSED_CLOSE_REPLAY_REQUIRED' for r in missed)
