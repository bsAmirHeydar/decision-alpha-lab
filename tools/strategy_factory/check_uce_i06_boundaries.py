from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
owned=[root/'mql5/Include/AlphaLab/StrategyFactory/OutcomeDataset',root/'mql5/Experts/StrategyFactory/UCE_I06_OutcomeDatasetDiagnostic.mq5',root/'mql5/Experts/StrategyFactoryTests/UCE_I06_OutcomeDatasetSelfTest.mq5',root/'mql5/Experts/StrategyFactoryTests/UCE_I06_LongShortCounterfactualSelfTest.mq5',root/'lab/11_strategy_factory/python/strategy_factory_dataset_v3']
forbidden=('OrderSend(', 'OrderCheck(', 'CTrade', 'PositionOpen(', 'WebRequest(', 'SocketCreate(', 'requests.', 'urllib.request')
hits=[]
for p in owned:
 for f in ([p] if p.is_file() else p.rglob('*')):
  if f.is_file() and f.suffix.lower() in ('.py','.mq5','.mqh'):
   text=f.read_text(encoding='utf-8',errors='ignore')
   for token in forbidden:
    if token in text:hits.append(f'{f.relative_to(root)}: {token}')
if hits: print('\n'.join(hits)); raise SystemExit(1)
print('UCE-I06 boundary guard PASS: research data-plane only; no live authority or external network I/O')
