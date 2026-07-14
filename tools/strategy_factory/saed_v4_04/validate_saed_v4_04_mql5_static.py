from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];files=list((ROOT/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4MultimodalViews').glob('*.mqh'))+list((ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics').glob('EXP_SAED_V4_04_*.mq5'))
text='\n'.join(p.read_text() for p in files)
for token in ['OrderSend(','CTrade','WebRequest(','SocketCreate(','PositionOpen(']:
 if token in text:raise SystemExit('forbidden MQL5 token: '+token)
if len(files)!=14:raise SystemExit(f'expected 14 files, got {len(files)}')
print('MQL5 static validation passed for 14 files')
