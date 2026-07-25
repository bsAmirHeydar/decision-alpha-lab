from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT = find_repository_root(__file__)
folders = [
    ROOT / 'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_24',
    ROOT / 'docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_24',
]
files = sorted(path for folder in folders for path in folder.glob('*.md'))
assert len(files) >= 220
for path in files:
    text = path.read_text(encoding='utf-8')
    assert text.startswith('---\n') and 'phase: SAED_V4_24' in text and len(text) > 1200, path
print(f'V4-24 Obsidian validation passed: {len(files)} notes')
