from tools.repository_paths import find_repository_root
from pathlib import Path
import json
import re
ROOT = find_repository_root(__file__)
source_files = sorted((ROOT / 'src/engine/packages/saed_v4_conformal_ood_selective_control').glob('*.py'))
artifact_files = sorted((ROOT / 'releases/history/strategy_factory/artifacts/saed_v4_24').glob('*.JSON'))
for path in source_files:
    if path.name == 'security.py':
        continue
    text = path.read_text(encoding='utf-8')
    for pattern in [r'MetaTrader5', r'OrderSend\s*\(', r'WebRequest\s*\(', r'BEGIN PRIVATE KEY']:
        assert not re.search(pattern, text, re.I), f'{path}: {pattern}'
for path in artifact_files:
    value = json.loads(path.read_text(encoding='utf-8'))
    text = json.dumps(value, sort_keys=True)
    for pattern in [r'"promotion_authority"\s*:\s*true', r'"runtime_executable"\s*:\s*true', r'"production_authority"\s*:\s*true', r'"execution_authority"\s*:\s*true']:
        assert not re.search(pattern, text, re.I), f'{path}: {pattern}'
print(f'V4-24 authority boundary passed: {len(source_files) + len(artifact_files)} files')
