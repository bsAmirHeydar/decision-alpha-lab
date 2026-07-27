from __future__ import annotations

from tools.consolidation.uc04w0.verify import verify


def test_uc04_w0_verifier_passes(repo_root):
    assert verify(repo_root, verify_release_controls=True) == []
