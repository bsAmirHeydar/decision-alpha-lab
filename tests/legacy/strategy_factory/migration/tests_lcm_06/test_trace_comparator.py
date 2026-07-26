import json
from src.engine.tooling.strategy_factory.lcm.lcm_06.trace_comparator import compare
def load(repo_root,name): return json.loads((repo_root/f"tests/legacy/strategy_factory/migration/fixtures/lcm_06/traces/{name}.json").read_text())
def test_exact_hard_parity(repo_root): assert compare(load(repo_root,"legacy_exact"),load(repo_root,"canonical_exact"))["comparison_status"]=="PASS"
def test_soft_mismatch(repo_root): assert compare(load(repo_root,"legacy_exact"),load(repo_root,"canonical_soft"))["comparison_status"]=="SOFT_MISMATCH"
def test_hard_mismatch(repo_root):
    r=compare(load(repo_root,"legacy_exact"),load(repo_root,"canonical_hard"));assert r["comparison_status"]=="HARD_MISMATCH";assert r["hard_mismatch_count"]>=1;assert not r["hard_mismatch_waived"]
def test_reason_codes_normalized(repo_root):
    a=load(repo_root,"legacy_exact");b=load(repo_root,"canonical_exact");b["events"][0]["reason_codes"]=["B","A","A"];a["events"][0]["reason_codes"]=["A","B"];assert compare(a,b)["comparison_status"]=="PASS"

def test_missing_hard_dimension_is_unknown(repo_root):
    a=load(repo_root,"legacy_exact");b=load(repo_root,"canonical_exact");del a["events"][0]["decision"];del b["events"][0]["decision"]
    r=compare(a,b);assert r["comparison_status"]=="UNKNOWN_EVIDENCE" and r["unknown_evidence_count"]>=1

def test_one_sided_missing_dimension_is_hard_mismatch(repo_root):
    a=load(repo_root,"legacy_exact");b=load(repo_root,"canonical_exact");del b["events"][0]["decision"]
    r=compare(a,b);assert r["comparison_status"]=="HARD_MISMATCH"

def test_naive_timestamp_rejected(repo_root):
    import pytest
    a=load(repo_root,"legacy_exact");b=load(repo_root,"canonical_exact");b["events"][0]["event_time"]="2026-07-19T12:00:00"
    with pytest.raises(Exception): compare(a,b)
