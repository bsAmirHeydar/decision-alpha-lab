from src.engine.tooling.strategy_factory.lcm.lcm_03.io import read_json,read_jsonl

def test_locator_cardinality(identity_root):
    ids=list(read_jsonl(identity_root/'identities/canonical_identity_candidates.jsonl'));loc=list(read_jsonl(identity_root/'locators/artifact_locator_records.jsonl'));assert len(ids)==len(loc)
def test_no_physical_canonical_path(identity_root):
    loc=list(read_jsonl(identity_root/'locators/artifact_locator_records.jsonl'));assert all(x['materialized_canonical_path'] is None and not x['canonical_path_materialized'] for x in loc)
def test_no_runtime_authority(identity_root):
    loc=list(read_jsonl(identity_root/'locators/artifact_locator_records.jsonl'));assert not any(x['runtime_authority'] or x['live_order_authority'] or x['capital_authority'] for x in loc)
def test_consumer_census_nonsemantic(identity_root):
    rows=list(read_jsonl(identity_root/'consumers/consumer_census.jsonl'));assert rows and not any(x['semantic_reachability_claimed'] for x in rows)
def test_coverage_complete(identity_root): assert read_json(identity_root/'reports/coverage_report.json')['coverage_complete']
