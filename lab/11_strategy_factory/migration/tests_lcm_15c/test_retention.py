import json
def test_retention(repo_root,package_root):rows=[json.loads(x) for x in (package_root/'records/pre_delete_lock_records.jsonl').read_text().splitlines() if x];assert len(rows)==2168 and all((repo_root/r['candidate_path']).is_file() for r in rows)
