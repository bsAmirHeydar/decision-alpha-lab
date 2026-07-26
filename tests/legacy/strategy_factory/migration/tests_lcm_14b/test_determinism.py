from src.engine.tooling.strategy_factory.lcm.lcm_14b.canonical import verify_embedded_digest

def test_output_manifest_digest_is_self_consistent(load):
    manifest = load("output_manifest.json")
    assert verify_embedded_digest(manifest, "output_manifest_digest")
    paths = [row["path"] for row in manifest["files"]]
    assert paths == sorted(paths)
    assert len(paths) == len(set(paths))
