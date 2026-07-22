def test_hostile(load):
 h=load("reports/hostile_review_report.json")
 assert h["result"]=="PASS" and h["failed_attack_count"]==0 and len(h["attacks"])>=5
