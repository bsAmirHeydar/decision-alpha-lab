def test_snapshots(repo_root):
 p=repo_root/"registry/legacy_context_migration/lcm_15a";assert sum(1 for x in (p/"candidate_input_snapshot.jsonl").read_text(encoding="utf-8").splitlines() if x)==2168;assert (p/"reference_match_snapshot.jsonl").is_file()
