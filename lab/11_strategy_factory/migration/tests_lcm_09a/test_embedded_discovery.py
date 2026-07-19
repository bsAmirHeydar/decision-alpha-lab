from .conftest import jl
def test_embedded_candidates_are_not_promoted():
 rows=jl("embedded/embedded_setup_registry.jsonl"); assert len(rows)>0; assert all(x["candidate_status"]=="UNRESOLVED_EMBEDDED_SETUP_CANDIDATE" and not x["promoted_to_setup_identity"] for x in rows)
def test_embedded_scan_is_deterministic_order():
 rows=jl("embedded/embedded_setup_registry.jsonl"); assert [x["source_artifact_path"] for x in rows]==sorted(x["source_artifact_path"] for x in rows)
