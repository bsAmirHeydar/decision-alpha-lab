def test_cli_registered(root):
 text=(root/'src/engine/packages/pyproject.toml').read_text();assert 'saed-v4-baseline-manual="saed_v4_baseline_manual.cli:main"' in text;assert 'saed_v4_baseline_manual*' in text
