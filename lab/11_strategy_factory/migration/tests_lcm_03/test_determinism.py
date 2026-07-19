from tools.strategy_factory.lcm.lcm_03.io import read_json,read_jsonl

def test_identity_digests_present(identity_root): assert all(x['identity_digest'].startswith('sha256:') for x in read_jsonl(identity_root/'identities/canonical_identity_candidates.jsonl'))
def test_alias_digests_present(identity_root): assert all(x['alias_digest'].startswith('sha256:') for x in read_jsonl(identity_root/'aliases/legacy_alias_records.jsonl'))
def test_summary_fixed_boundary(identity_root):
    x=read_json(identity_root/'reports/identity_summary.json');assert not x['source_move_performed'] and not x['source_delete_performed'] and not x['semantic_refactor_performed']
def test_ambiguity_explicit(identity_root): assert all(x['resolution_status']=='AMBIGUOUS_ROLE_BLOCKED' for x in read_jsonl(identity_root/'unresolved/identity_ambiguity_queue.jsonl'))
