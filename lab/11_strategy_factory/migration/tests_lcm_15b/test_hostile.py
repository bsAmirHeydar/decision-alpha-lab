def test_hostile(load):
 r=load("reports/hostile_review_report.json");assert r["report_result"]=="PASS" and r["fail_count"]==0
