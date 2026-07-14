from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
files=list((ROOT/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4EventModel').glob('*.mqh'))+list((ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics').glob('EXP_SAED_V4_03_*.mq5'))
text="\n".join(p.read_text(errors='ignore') for p in files)
for token in ['OrderSend','CTrade','WebRequest','SocketCreate','PositionOpen']:
 if token in text:raise SystemExit(f'forbidden token: {token}')
for required in ['SAED_EVENT_ORDER_AUTHORITY false','SAED_EVENT_BROKER_AUTHORITY false','SAED_EVENT_NETWORK_AUTHORITY false']:
 if required not in text:raise SystemExit(f'missing boundary: {required}')
print(f'MQL5 static validation passed for {len(files)} files')
