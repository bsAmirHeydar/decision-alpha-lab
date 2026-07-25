def test_acceptance(load):
 a=load("reports/acceptance_report.json")
 assert a["passed"] is True and a["non_compensatory_gate_failures"]==[]
 assert all(a["gates"].values())
