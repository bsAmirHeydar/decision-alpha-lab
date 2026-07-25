def test_acceptance(load):
 a=load("reports/acceptance_report.json");assert a["report_result"]=="PASS" and all(a["gates"].values())
