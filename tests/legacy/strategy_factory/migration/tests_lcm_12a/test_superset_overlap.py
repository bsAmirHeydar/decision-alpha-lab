from src.engine.tooling.strategy_factory.lcm.lcm_12a.io import load_jsonl
def test_supersets_record_unique_content(mapping_root):
    rows=load_jsonl(mapping_root/"analysis/documentation_superset_analysis.jsonl")
    assert all(r["superset_unique_line_count"]==len(r["superset_unique_line_digests"]) for r in rows)
def test_semantic_overlap_does_not_claim_equivalence(mapping_root):
    rows=load_jsonl(mapping_root/"analysis/documentation_semantic_overlap_candidates.jsonl")
    assert all(r["proof_ceiling"]=="LEXICAL_TOKEN_OVERLAP_NOT_SEMANTIC_EQUIVALENCE" and not r.get("merge_or_removal_authorized",False) for r in rows)
