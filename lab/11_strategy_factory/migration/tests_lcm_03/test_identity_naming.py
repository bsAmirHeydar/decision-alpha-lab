import json
from tools.strategy_factory.lcm.lcm_03.naming import propose_identity
from tools.strategy_factory.lcm.lcm_03.io import read_jsonl

def test_fixture_identity(repo_root):
    r=json.loads((repo_root/'lab/11_strategy_factory/migration/fixtures/lcm_03/minimal_identity_fixture.json').read_text());x=propose_identity(r);assert x['identity_id'].startswith('CTX_EXAMPLE_EXAMPLECONTEXT_');assert x['identity_id'].endswith('_V1')
def test_identity_ids_unique(identity_root):
    rows=list(read_jsonl(identity_root/'identities/canonical_identity_candidates.jsonl'));assert len(rows)==len({x['identity_id'] for x in rows})
def test_no_identity_uses_raw_path(identity_root):
    rows=list(read_jsonl(identity_root/'identities/canonical_identity_candidates.jsonl'));assert all('/' not in x['identity_id'] and '\\' not in x['identity_id'] for x in rows)
def test_provisional_not_approved(identity_root):
    rows=list(read_jsonl(identity_root/'identities/canonical_identity_candidates.jsonl'));assert not any(x['human_semantic_approval_claimed'] for x in rows)
def test_no_merge_claim(identity_root):
    rows=list(read_jsonl(identity_root/'identities/canonical_identity_candidates.jsonl'));assert not any(x['merge_claimed'] for x in rows)
