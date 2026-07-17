from __future__ import annotations
import json
from saed_v4_sovereign_distributed_compute import run

def test_reference_acceptance(inputs,root):
    r=run(inputs); assert r["certificate"]["status"]=="accepted_reference"; assert r["certificate"]["production_authorization"] is False
    assert r["locality"]["all_locality_satisfied"] and r["usage"]["all_within_budget"] and r["recovery"]["all_recovered"]

def test_golden_exact(inputs,root):
    r=run(inputs); ar=root/"lab/11_strategy_factory/artifacts/saed_v4_34"
    mapping=json.loads((root/"tools/strategy_factory/saed_v4_34/artifact_map.json").read_text())
    for key,name in mapping.items(): assert r[key]==json.loads((ar/name).read_text()),key

def test_zero_authority(inputs):
    a=run(inputs)["authority"]
    for k in ["may_export_raw_data","may_mutate_ucee","may_select_treatment","may_allocate_risk","may_compile_live_runtime","may_send_order","promotion_authority","production_authorization","live_trading_authority"]: assert a[k] is False
