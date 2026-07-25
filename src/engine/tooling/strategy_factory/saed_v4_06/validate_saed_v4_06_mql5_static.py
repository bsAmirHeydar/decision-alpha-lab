from tools.repository_paths import find_repository_root
from pathlib import Path

ROOT=find_repository_root(__file__)
INC=ROOT/'mql5/Include/AlphaLab/StrategyFactory/SAEDV4TreatmentDsl'
EXP=ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics'
files=sorted(INC.glob('*.mqh'))+sorted(EXP.glob('EXP_SAED_V4_06_*.mq5'))
if len(files)<16:
    raise SystemExit(f'insufficient MQL5 mirror: {len(files)} files')
forbidden=('OrderSend(', 'OrderSendAsync(', 'CTrade', 'WebRequest(', 'SocketCreate(', 'FileOpen("http', '#import')
errors=[]
for path in files:
    text=path.read_text(encoding='utf-8')
    for token in forbidden:
        if token in text: errors.append(f'{path.relative_to(ROOT)}:{token}')
    if path.suffix=='.mqh' and '#ifndef' not in text:
        errors.append(f'{path.relative_to(ROOT)}:missing include guard')
if errors:
    raise SystemExit('; '.join(errors))
print(f'validated {len(files)} diagnostic-only MQL5 files')
