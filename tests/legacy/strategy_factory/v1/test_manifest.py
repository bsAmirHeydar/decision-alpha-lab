from pathlib import Path

from strategy_factory.manifest import load_manifest


def test_reference_manifest_is_valid():
    path = Path(__file__).resolve().parents[1] / "examples" / "manifests" / "temporal_divergence.json"
    manifest = load_manifest(path)
    assert manifest.strategy_id == "EXP0017_temporal_divergence_reference"
    assert manifest.status == "draft"
    assert manifest.manifest_hash.startswith("manifest_")
