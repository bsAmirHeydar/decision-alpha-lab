from pathlib import Path
from dataclasses import replace
from fp_i01_compatibility.policy import load_dependency_pins
from fp_i01_compatibility.hash_guard import verify_dependency
from fp_i01_compatibility.enums import CompatibilityStatus
ROOT=Path(__file__).resolve().parents[5]

def test_all_hash_pins_match_i00_baseline():
    _,pins=load_dependency_pins(ROOT);results=[verify_dependency(ROOT,p) for p in pins]
    assert len(results)==19
    assert all(x.status is CompatibilityStatus.PASS for x in results)

def test_wrong_expected_hash_fails():
    _,pins=load_dependency_pins(ROOT);bad=replace(pins[0],expected_aggregate_sha256='0'*64)
    result=verify_dependency(ROOT,bad)
    assert result.status is CompatibilityStatus.FAIL and result.reason_code=='AGGREGATE_HASH_MISMATCH'

def test_wrong_file_count_fails_before_reuse():
    _,pins=load_dependency_pins(ROOT);bad=replace(pins[0],expected_file_count=999)
    result=verify_dependency(ROOT,bad)
    assert result.status is CompatibilityStatus.FAIL and result.reason_code=='FILE_COUNT_MISMATCH'
