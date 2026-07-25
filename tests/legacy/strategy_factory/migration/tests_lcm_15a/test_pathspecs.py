def test_pathspecs(proof_root,load):
 r=load("deletion_candidate_ledger.json");approved=[x for x in (proof_root/"approved_relocation_pathspec.txt").read_text(encoding="utf-8").splitlines() if x];assert len(approved)==r["approved_relocation_count"];assert (proof_root/"approved_future_deletion_pathspec.txt").read_text(encoding="utf-8")==""
