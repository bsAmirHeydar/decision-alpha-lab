from fp_i01_compatibility.differential import run_all_fixtures
from fp_i01_compatibility.enums import CompatibilityStatus

def test_all_golden_fixtures_pass():
    results=run_all_fixtures();assert len(results)==8
    assert all(x.status is CompatibilityStatus.PASS for x in results)

def test_golden_evidence_is_stable():
    a=run_all_fixtures();b=run_all_fixtures()
    assert [x.evidence_hash for x in a]==[x.evidence_hash for x in b]

def test_every_fixture_proves_source_unchanged_and_repeatable():
    assert all(x.source_unchanged and x.deterministic for x in run_all_fixtures())
