from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
def test_cli_registered():
 t=(ROOT/'src/engine/packages/pyproject.toml').read_text();assert 'saed-v4-outcome-cube="saed_v4_outcome_cube.cli:main"' in t;assert 'saed_v4_outcome_cube*' in t
