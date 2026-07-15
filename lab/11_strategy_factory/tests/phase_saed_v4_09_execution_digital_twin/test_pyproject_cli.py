from conftest import ROOT

def test_cli_is_registered_and_package_included():
    t=(ROOT/'lab/11_strategy_factory/python/pyproject.toml').read_text();assert 'saed-v4-execution-twin="saed_v4_execution_twin.cli:main"' in t;assert 'saed_v4_execution_twin*' in t
