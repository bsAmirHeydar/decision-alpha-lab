import hashlib
from pathlib import Path

from tools.strategy_factory.lcm.lcm_14a.service import LCM14ADeprecationRedirectService


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def test_clean_rebuild_is_byte_deterministic(repo_root, tmp_path):
    service = LCM14ADeprecationRedirectService(repo_root)
    first = service.build(tmp_path / "first")
    second = service.build(tmp_path / "second")
    assert first.deprecation_id == second.deprecation_id
    assert first.handoff_digest == second.handoff_digest
    assert first.candidate_count == second.candidate_count == 613
    assert first.redirect_count == second.redirect_count == 613
    assert first.documentation_redirect_count == second.documentation_redirect_count == 136
    assert first.active_source_blocked_count == second.active_source_blocked_count == 477
    assert first.observation_candidate_count == second.observation_candidate_count == 136
    assert tree_digest(first.output_root) == tree_digest(second.output_root)
