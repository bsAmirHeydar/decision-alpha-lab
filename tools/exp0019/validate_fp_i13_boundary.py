from pathlib import Path
root=Path(__file__).resolve().parents[2]
paths=[
    root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i13/python/fp_i13_release',
    root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I13',
    root/'mql5/Indicators/EXP0019/FaerieProtocolTests/EXP0019_FP_I13_ReleaseSelfTest.mq5',
]
forbidden=('OrderSend(','CTrade','PositionOpen(','PositionClose(','WebRequest(','PERIOD_CURRENT')
find=[]
for p in paths:
    files=[p] if p.is_file() else list(p.rglob('*'))
    for f in files:
        if not f.is_file() or '__pycache__' in f.parts or f.name in ('constants.py','authority.py'):
            continue
        text=f.read_text(encoding='utf-8',errors='ignore')
        for token in forbidden:
            if token in text:
                find.append((str(f.relative_to(root)),token))
print({'status':'PASS' if not find else 'FAIL','findings':find})
raise SystemExit(1 if find else 0)
