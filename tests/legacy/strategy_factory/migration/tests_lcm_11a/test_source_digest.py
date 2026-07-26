from src.engine.tooling.strategy_factory.lcm.lcm_11a.canonical import file_digest
def test_inventory_source_digests_match(repo_root,inventory):
    for item in inventory['objects'][:25]:
        assert file_digest(repo_root/item['source_path'])==item['source_digest']
