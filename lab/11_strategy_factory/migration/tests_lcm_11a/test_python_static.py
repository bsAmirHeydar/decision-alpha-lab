from tools.strategy_factory.lcm.lcm_11a.static_validation import validate_python
def test_python_static(repo_root):
    result=validate_python(repo_root/'tools/strategy_factory/lcm/lcm_11a')
    assert result['result']=='PASS',result
    assert result['file_count']>=15
