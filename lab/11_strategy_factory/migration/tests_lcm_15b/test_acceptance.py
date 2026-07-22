def test_acceptance(load):
 r=load("reports/acceptance_report.json");assert r["report_result"]=="PASS" and all(r["gates"].values())
