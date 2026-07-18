import csv, json

def test_documentation_tree_reports_deny_deletion(survey_root):
    v=json.loads((survey_root/'documentation/exact_duplicate_trees.json').read_text())
    assert v['deletion_authority'] is False
    assert all(g['semantic_equivalence_claimed'] is False for g in v['groups'])

def test_root_hygiene_is_classification_only(survey_root):
    with (survey_root/'root_hygiene/root_artifact_inventory.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
    assert rows and all(r['move_performed']=='false' and r['delete_performed']=='false' for r in rows)

def test_exact_file_duplicates_are_not_merge_authority(survey_root):
    v=json.loads((survey_root/'duplicates/exact_file_duplicate_groups.json').read_text())
    assert v['merge_authority'] is False and v['delete_authority'] is False
