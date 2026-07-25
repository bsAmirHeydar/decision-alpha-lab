from pathlib import Path
import pytest

from tools.strategy_factory.lcm.lcm_00.canonical import normalize_root_relative, digest_object
from tools.strategy_factory.lcm.lcm_00.errors import ContractViolation
from tools.strategy_factory.lcm.lcm_00.scope import ScopePolicy, classify_path


def test_root_relative_normalization():
    assert normalize_root_relative("a/b c.txt") == "a/b c.txt"

@pytest.mark.parametrize("bad", ["", "/abs", "../x", "a/../b", "./x"])
def test_unsafe_paths_rejected(bad):
    with pytest.raises(ContractViolation):
        normalize_root_relative(bad)


def test_scope_excludes_ephemeral():
    policy = ScopePolicy("P", "1")
    assert classify_path("x/__pycache__/a.pyc", policy)[0] is False
    assert classify_path("x/a.py", policy)[0] is True


def test_digest_is_order_independent_for_objects():
    assert digest_object({"b": 2, "a": 1}) == digest_object({"a": 1, "b": 2})
