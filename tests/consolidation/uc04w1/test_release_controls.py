from __future__ import annotations

from pathlib import Path

from tools.consolidation.uc04w1.verify import verify


def test_w1a_release_controls(repo_root: Path) -> None:
    assert verify(repo_root, verify_release_controls=True, verify_upstream_w0=False) == []
