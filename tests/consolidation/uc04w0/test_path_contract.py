from __future__ import annotations

import json

from tools.repository_paths import RepositoryPaths, find_repository_root, migrated_relative_path, resolve_repository_path


def test_source_archive_repository_discovery(repo_root):
    assert find_repository_root(repo_root / "docs") == repo_root
    assert find_repository_root(repo_root / "src/engine/packages") == repo_root


def test_typed_canonical_roots(repo_root):
    paths = RepositoryPaths.from_root(repo_root)
    assert paths.source_root == repo_root / "src/engine"
    assert paths.package_root == repo_root / "src/engine/packages"
    assert paths.strategy_factory_registry_root == repo_root / "registry/history/strategy_factory"
    assert paths.runtime_run_root == repo_root / ".alpha/runs"


def test_legacy_prefixes_resolve_deterministically(repo_root):
    assert migrated_relative_path(repo_root, "tools/strategy_factory/acl_os/common.py") == "src/engine/tooling/strategy_factory/acl_os/common.py"
    assert migrated_relative_path(repo_root, "registry/strategy_factory/contexts/rthp/v1/context_package_registration.json") == "registry/history/strategy_factory/contexts/rthp/v1/context_package_registration.json"


def test_exact_or_prefix_resolution_targets_existing_file(repo_root):
    target = resolve_repository_path(repo_root, "lab/11_strategy_factory/python/strategy_factory_rthp_train_activation_v1/pipeline.py", require_exists=True)
    assert target == repo_root / "src/engine/packages/strategy_factory_rthp_train_activation_v1/pipeline.py"


def test_machine_path_contract_matches_implementation(repo_root):
    document = json.loads((repo_root / "registry/consolidation/uc04/w0/path_contract.json").read_text(encoding="utf-8"))
    assert document["status"] == "ACTIVE"
    assert document["canonical_roots"]["runtime_runs"] == ".alpha/runs"
    assert document["semantic_change"] is False
