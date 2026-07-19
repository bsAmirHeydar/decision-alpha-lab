import pytest
from tools.strategy_factory.lcm.lcm_05.io import read_json
from tools.strategy_factory.lcm.lcm_05.path_policy import validate
from tools.strategy_factory.lcm.lcm_05.errors import PathSafetyError

def test_reference_paths_safe(topology_root):
    r=read_json(topology_root/'paths/target_path_safety_report.json');assert r['windows_safe'];assert r['unsafe_target_count']==0;assert r['max_target_path_length']<=220
def test_reference_collision_free(topology_root):
    r=read_json(topology_root/'collisions/target_path_collision_report.json');assert r['collision_free'];assert r['casefold_collision_count']==0
def test_reject_absolute():
    with pytest.raises(PathSafetyError):validate('/tmp/x')
def test_reject_traversal():
    with pytest.raises(PathSafetyError):validate('a/../b')
def test_reject_reserved():
    with pytest.raises(PathSafetyError):validate('a/CON.txt')
def test_reject_backslash():
    with pytest.raises(PathSafetyError):validate('a\\b')
