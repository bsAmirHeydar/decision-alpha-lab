from pathlib import Path

import pytest

from tools.consolidation.uc03p3.verify import verify


def repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def test_part3_repository_closure() -> None:
    repo = repository_root()
    decision = repo / "registry/consolidation/uc03/part3/part3_exit_decision.json"
    if not decision.is_file():
        pytest.skip("UC-03 Part 3 has not been applied")
    assert verify(repo, ci_fast=True) == []
