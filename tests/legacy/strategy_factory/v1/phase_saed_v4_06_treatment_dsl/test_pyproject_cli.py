from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
def test_pyproject_exposes_cli():
 text=(ROOT/'src/engine/packages/pyproject.toml').read_text();assert 'saed-v4-treatment-dsl="saed_v4_treatment_dsl.cli:main"' in text;assert 'saed_v4_treatment_dsl*' in text
