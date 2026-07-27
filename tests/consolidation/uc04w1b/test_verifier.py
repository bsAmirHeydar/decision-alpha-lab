from __future__ import annotations

from tools.consolidation.uc04w1b.verify import verify


def test_uc04w1b_verifier_passes(repo_root) -> None:
    assert verify(repo_root) == []
