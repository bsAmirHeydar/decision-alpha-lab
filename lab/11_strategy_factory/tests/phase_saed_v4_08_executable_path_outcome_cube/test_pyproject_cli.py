from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def test_cli_registered():
 t=(ROOT/'lab/11_strategy_factory/python/pyproject.toml').read_text();assert 'saed-v4-outcome-cube="saed_v4_outcome_cube.cli:main"' in t;assert 'saed_v4_outcome_cube*' in t
