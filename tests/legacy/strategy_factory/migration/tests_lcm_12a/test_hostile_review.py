def test_hostile_review(load):
    r=load("reports/hostile_review_report.json")
    assert r["result"]=="PASS"
    assert r["checks"]["INSTALLER_HISTORY_DELETE_COUNT"]==0
    assert r["checks"]["EXTERNAL_LINKS_ASSUMED_ABSENT"] is False
    assert r["checks"]["CONTRADICTION_SILENT_HARMONIZATION_COUNT"]==0
