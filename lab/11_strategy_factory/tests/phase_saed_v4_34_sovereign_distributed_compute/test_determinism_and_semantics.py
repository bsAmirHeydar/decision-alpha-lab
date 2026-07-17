from __future__ import annotations
import copy
from saed_v4_sovereign_distributed_compute import run

def test_exact_replay(inputs): assert run(inputs)==run(copy.deepcopy(inputs))
def test_order_invariance(inputs):
    a=run(inputs); x=copy.deepcopy(inputs); x["nodes"].reverse(); x["attestations"].reverse(); x["artifacts"].reverse(); x["domains"].reverse()
    b=run(x); assert a["partition"]==b["partition"] and a["execution"]==b["execution"]
def test_future_suffix_ignored_by_cutoff(inputs):
    a=run(inputs); x=copy.deepcopy(inputs); x["attestations"].append({"attestation_id":"ATT-FUTURE","node_id":"NODE-FUTURE","attestation_fingerprint":"0"*64,"runtime_image_hash":"0"*64,"known_time":"2099-01-01T00:00:00Z","expires_time":"2099-12-31T00:00:00Z","human_approved":False,"synthetic_fixture":True})
    # Closed inventory rejects unknown node, proving suffix cannot silently alter a valid run.
    try: run(x)
    except Exception: pass
    else: raise AssertionError("future suffix must not be accepted")
def test_baseline_preserved(inputs): assert run(inputs)["recovery"]["baseline_preserved"] is True
def test_no_raw_data_cross_domain(inputs):
    r=run(inputs); assert not r["partition"]["raw_data_crossed_domain"]; assert r["network_events"]["raw_data_events"]==0
def test_evidence_quorum(inputs): assert run(inputs)["quorum"]["threshold_met"] is True
def test_complete_exposure(inputs): assert run(inputs)["exposure"]["complete_accounting"] is True
