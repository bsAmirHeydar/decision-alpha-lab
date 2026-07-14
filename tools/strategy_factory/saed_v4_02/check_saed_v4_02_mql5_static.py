from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
files = list((ROOT/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4ContextTwin').glob('*.mqh'))
files += list((ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics').glob('EXP_SAED_V4_02_*.mq5'))
text = '\n'.join(p.read_text(errors='ignore') for p in files).lower()
for token in ['ordersend','ctrade','webrequest','socketcreate','positionopen']:
    if token in text:
        raise SystemExit(f'forbidden token: {token}')
print(f'static validation passed for {len(files)} files')
