from .conftest import j
def test_hostile_review_and_acceptance_close_noncompensatory_gates():
 h=j("reports/hostile_review.json");a=j("reports/acceptance_report.json");assert h["hostile_review_passed"] and len(h["attacks"])>=5;assert a["acceptance_gate_passed"] and a["hard_mismatch_count"]==0;assert a["reference_ready_count"]+a["explicitly_blocked_count"]==60
