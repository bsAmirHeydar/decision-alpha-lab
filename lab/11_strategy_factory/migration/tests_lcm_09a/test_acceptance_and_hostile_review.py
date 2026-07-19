from .conftest import j
def test_acceptance_passes_noncompensatory_gates():
 a=j("reports/acceptance_report.json"); assert a["acceptance_gate_passed"]; assert all(a["gates"].values())
def test_hostile_review_passes_all_cases():
 h=j("reports/hostile_review.json"); assert h["hostile_review_passed"]; assert h["failed_case_count"]==0; assert len(h["cases"])>=8
