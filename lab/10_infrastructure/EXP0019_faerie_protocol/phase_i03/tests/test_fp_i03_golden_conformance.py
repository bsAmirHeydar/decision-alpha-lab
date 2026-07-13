from fp_i03_time.conformance import run_conformance
from fp_i03_time.golden import golden_vector_material


def test_conformance_report_passes_with_expected_check_count():
    report=run_conformance()
    assert report["passed"]
    assert report["check_count"]==20
    assert len(report["report_hash"])==64


def test_golden_vector_is_deterministic():
    assert golden_vector_material()==golden_vector_material()
    assert len(golden_vector_material()["vector_hash"])==64
