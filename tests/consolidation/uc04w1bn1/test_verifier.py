from __future__ import annotations

from tools.consolidation.uc04w1bn1.verify import verify


def test_uc04w1bn1_verifier_passes(repo_root) -> None:
    assert verify(repo_root) == []
