import csv, json
from tools.strategy_factory.lcm.lcm_01.verify import verify_survey_package

def test_reference_package_verifies(survey_root):
    r=verify_survey_package(survey_root); assert r['passed']; assert r['artifact_count']>30000

def test_every_baseline_path_appears_once(survey_root):
    with (survey_root/'inventory/artifact_inventory.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
    assert len(rows)==len({r['path'] for r in rows})
    c=json.loads((survey_root/'integrity/baseline_coverage_report.json').read_text())
    assert c['all_baseline_paths_covered_exactly_once'] is True

def test_no_destructive_change_claimed(survey_root):
    s=json.loads((survey_root/'reports/survey_summary.json').read_text())
    assert s['source_file_moved'] is False and s['source_file_deleted'] is False and s['semantic_refactor_performed'] is False
