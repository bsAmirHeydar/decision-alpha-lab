import pytest
from src.engine.tooling.strategy_factory.lcm.lcm_06.move_plan import build as move
from src.engine.tooling.strategy_factory.lcm.lcm_06.redirect_generator import build as redirect
def test_move_preview_only():
    r=move("a/b.mqh","c/d.mqh","sha256:"+"1"*64);assert not r["execute_allowed"] and not r["target_materialization_allowed"]
@pytest.mark.parametrize("kind,legacy,target",[
    ("MQL_INCLUDE_WRAPPER","a/b.mqh","c/d.mqh"),
    ("OBSIDIAN_REDIRECT_STUB","a/b.md","c/d.md"),
    ("PYTHON_IMPORT_SHIM","a/b.py","c/d.py"),
])
def test_redirect_preview_only(kind,legacy,target):
    r=redirect(kind,legacy,target);assert r["preview_only"] and not r["write_performed"] and not r["execution_authority"]
def test_path_traversal_rejected():
    with pytest.raises(Exception): move("a/b","../escape","sha256:"+"1"*64)

def test_move_same_path_rejected():
    with pytest.raises(Exception): move("a/b.mqh","a/b.mqh","sha256:"+"1"*64)

def test_move_invalid_hash_rejected():
    with pytest.raises(Exception): move("a/b.mqh","c/d.mqh","bad")

def test_redirect_extension_mismatch_rejected():
    with pytest.raises(Exception): redirect("MQL_INCLUDE_WRAPPER","a/b.mqh","c/d.py")
