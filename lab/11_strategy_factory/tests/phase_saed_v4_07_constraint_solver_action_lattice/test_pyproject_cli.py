from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def test_pyproject_registration():
 t=(ROOT/'lab/11_strategy_factory/python/pyproject.toml').read_text();assert 'version="0.37.0"' in t and 'saed-v4-action-lattice=' in t and 'saed_v4_action_lattice*' in t
