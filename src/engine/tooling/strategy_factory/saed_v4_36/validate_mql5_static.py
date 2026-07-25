from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);paths=list((ROOT/'mql5/Include/StrategyFactory/SAED/V4_36').glob('*.mqh'))+list((ROOT/'mql5/Experts/StrategyFactory/SAED/V4_36').glob('*.mq5'))
assert len(paths)>=22
for p in paths:
 t=p.read_text(encoding='utf-8');low=t.lower();assert '#ifndef' in t or '#property strict' in t;assert 'ordersend(' not in low;assert 'ctrade' not in low;assert 'production_authorization true' not in low;assert 'automatic_execution true' not in low
print(f'V4-36 MQL5 static validation passed: {len(paths)} files')
