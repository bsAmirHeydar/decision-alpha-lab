def test_hostile(load):
 h=load("reports/hostile_review_report.json");assert h["report_result"]=="PASS" and h["fail_count"]==0
