from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
owned=[root/'mql5/Include/AlphaLab/StrategyFactory/DeepViews',root/'mql5/Experts/StrategyFactory/UCE_I10_DeepViewsDiagnostic.mq5',root/'mql5/Tests/Experts/StrategyFactory/UCE_I10_DeepViewsSelfTest.mq5',root/'mql5/Tests/Experts/StrategyFactory/UCE_I10_CausalitySafetySelfTest.mq5',root/'src/engine/packages/strategy_factory_deep_views_v3']
forbidden=('OrderSend(', 'OrderCheck(', 'CTrade', 'PositionOpen(', 'WebRequest(', 'SocketCreate(', 'requests.', 'urllib.request', 'subprocess.', 'os.system(', 'pickle.', 'joblib.')
hits=[]
for item in owned:
    for f in ([item] if item.is_file() else item.rglob('*')):
        if f.is_file() and f.suffix.lower() in ('.py','.mq5','.mqh'):
            text=f.read_text(encoding='utf-8',errors='ignore')
            for token in forbidden:
                if token in text:hits.append(f'{f.relative_to(root)}: forbidden token {token}')
if hits:
    print('\n'.join(hits));raise SystemExit(1)
print('UCE-I10 boundary guard PASS: offline deep-view research, qualification, and runtime-neutral contracts only; no order, broker, network, subprocess, or opaque-object authority')
