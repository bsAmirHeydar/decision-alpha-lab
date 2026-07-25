from copy import deepcopy

from fp_i00_governance.canonical import canonical_sha256
from fp_i00_governance.manifest import build_manifest

from conftest import REPO_ROOT, load_policy


def test_manifest_is_deterministic_for_same_repository():
    policy = load_policy()
    first = build_manifest(REPO_ROOT, policy)
    second = build_manifest(REPO_ROOT, policy)
    assert first == second
    material = dict(first)
    supplied = material.pop("manifest_hash")
    assert supplied == canonical_sha256(material)


def test_manifest_freezes_open_decision_and_authority():
    manifest = build_manifest(REPO_ROOT, load_policy())
    assert manifest["open_decision_ids"] == ["FP-DEC-012"]
    assert manifest["authority"] == {
        "execution_authority": False,
        "broker_authority": False,
        "network_authority": False,
        "shared_core_mutation": False,
    }


def test_dependency_hash_change_changes_manifest(tmp_path):
    policy = load_policy()
    original = build_manifest(REPO_ROOT, policy)
    changed = deepcopy(original)
    changed["shared_dependencies"][0]["aggregate_sha256"] = "f" * 64
    changed.pop("manifest_hash")
    assert canonical_sha256(changed) != original["manifest_hash"]
