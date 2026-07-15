from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def test_pyproject_exposes_cli():
 text=(ROOT/'lab/11_strategy_factory/python/pyproject.toml').read_text();assert 'saed-v4-treatment-dsl="saed_v4_treatment_dsl.cli:main"' in text;assert 'saed_v4_treatment_dsl*' in text
