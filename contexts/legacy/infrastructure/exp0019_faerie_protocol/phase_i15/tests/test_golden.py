import json
from pathlib import Path

def test_golden_vectors_complete():
    p=Path(__file__).resolve().parents[1]/'golden/FP_I15_GOLDEN_VECTORS.v1.json'
    d=json.loads(p.read_text())
    assert d['phase_id']=='FP-I15'
    assert len(d['vectors'])==9
    ids={x['id'] for x in d['vectors']}
    assert {'BUY_GEOMETRY','SELL_SPREAD_GEOMETRY','PAPER_POLICY_MATRIX','PAPER_SCENARIO_MATRIX','LIVE_GATE'}<=ids

def test_sell_golden_exact_spread():
    p=Path(__file__).resolve().parents[1]/'golden/FP_I15_GOLDEN_VECTORS.v1.json'
    d=json.loads(p.read_text())
    plan=next(x['plan'] for x in d['vectors'] if x['id']=='SELL_SPREAD_GEOMETRY')
    g=plan['geometry']
    assert abs(g['adjusted_stop']-(g['raw_stop']+g['spread_snapshot']))<1e-12

def test_live_gate_remains_disabled():
    p=Path(__file__).resolve().parents[1]/'golden/FP_I15_GOLDEN_VECTORS.v1.json'
    d=json.loads(p.read_text())
    gate=next(x for x in d['vectors'] if x['id']=='LIVE_GATE')
    assert gate['live_policy']=='UNSET' and gate['live_execution_enabled'] is False
