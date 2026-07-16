from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[3]
files = sorted(list((ROOT / 'mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_24').glob('*.mqh')) + list((ROOT / 'mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_24').glob('*.mq5')))
assert len(files) >= 20
for path in files:
    text = path.read_text(encoding='utf-8')
    assert '#ifndef' in text or '#property strict' in text
    for pattern in [r'OrderSend\s*\(', r'WebRequest\s*\(', r'FileOpen\s*\(', r'password', r'private key', r'DLL']:
        assert not re.search(pattern, text, re.I), path
print(f'V4-24 MQL5 static validation passed: {len(files)} files; MetaEditor pending_local_windows')
