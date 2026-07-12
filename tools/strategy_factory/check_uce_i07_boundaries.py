from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
owned=[
 root/'mql5/Include/AlphaLab/StrategyFactory/TrainerSDK',
 root/'mql5/Experts/StrategyFactory/UCE_I07_TrainerSDKDiagnostic.mq5',
 root/'mql5/Experts/StrategyFactoryTests/UCE_I07_TrainerSDKSelfTest.mq5',
 root/'mql5/Experts/StrategyFactoryTests/UCE_I07_CapabilityParitySelfTest.mq5',
 root/'lab/11_strategy_factory/python/strategy_factory_trainers_v3']
forbidden=('OrderSend(', 'OrderCheck(', 'CTrade', 'PositionOpen(', 'WebRequest(', 'SocketCreate(', 'requests.', 'urllib.request', 'subprocess.', 'os.system(', 'pickle.', 'joblib.dump(', 'joblib.load(')
hits=[]
for item in owned:
 for f in ([item] if item.is_file() else item.rglob('*')):
  if f.is_file() and f.suffix.lower() in ('.py','.mq5','.mqh'):
   text=f.read_text(encoding='utf-8',errors='ignore')
   for token in forbidden:
    if token in text:hits.append(f'{f.relative_to(root)}: forbidden token {token}')
if hits:
 print('\n'.join(hits));raise SystemExit(1)
print('UCE-I07 boundary guard PASS: offline trainer control plane only; no order, network, subprocess, or opaque-pickle authority')
