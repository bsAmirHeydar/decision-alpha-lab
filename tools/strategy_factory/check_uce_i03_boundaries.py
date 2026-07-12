#!/usr/bin/env python3
from pathlib import Path
import sys
FORBIDDEN=("Order"+"Send(","Order"+"Check(","C"+"Trade","Position"+"Open(")
OWNED=(Path('mql5/Include/AlphaLab/StrategyFactory/TreatmentAtoms'),Path('mql5/Experts/StrategyFactory/UCE_I03_TreatmentAtomsDiagnostic.mq5'),Path('mql5/Experts/StrategyFactoryTests/UCE_I03_TreatmentAtomsSelfTest.mq5'),Path('lab/11_strategy_factory/python/strategy_factory_treatments_v3'))
def main():
 root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); failures=[]
 for rel in OWNED:
  p=root/rel
  files=[p] if p.is_file() else list(p.rglob('*')) if p.exists() else []
  for f in files:
   if not f.is_file() or f.suffix.lower() not in {'.py','.mq5','.mqh'}: continue
   text=f.read_text(encoding='utf-8',errors='ignore')
   for token in FORBIDDEN:
    if token in text: failures.append(f'{f.relative_to(root)}: forbidden live authority token {token}')
 if failures:
  print('\n'.join(failures)); return 1
 print('UCE-I03 boundary check PASS: no broker authority in phase-owned modules'); return 0
if __name__=='__main__': raise SystemExit(main())
