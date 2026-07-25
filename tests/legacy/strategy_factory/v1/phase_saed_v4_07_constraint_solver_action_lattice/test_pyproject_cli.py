from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
def test_pyproject_registration():
 t=(ROOT/'src/engine/packages/pyproject.toml').read_text();assert 'version="0.37.0"' in t and 'saed-v4-action-lattice=' in t and 'saed_v4_action_lattice*' in t
