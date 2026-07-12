#!/usr/bin/env python3
from pathlib import Path
import sys
FORBIDDEN=("Order"+"Send(","Order"+"Check(","C"+"Trade","Position"+"Open(","Web"+"Request(","socket.","requests.","subprocess.Popen")
OWNED=(Path('mql5/Include/AlphaLab/StrategyFactory/TreatmentCompiler'),Path('mql5/Experts/StrategyFactory/UCE_I04_TreatmentCompilerDiagnostic.mq5'),Path('mql5/Experts/StrategyFactoryTests/UCE_I04_TreatmentCompilerSelfTest.mq5'),Path('lab/11_strategy_factory/python/strategy_factory_treatment_compiler_v3'))
def main():
 root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); failures=[]
 for rel in OWNED:
  p=root/rel
  if not p.exists(): failures.append(f'missing owned path: {rel}'); continue
  files=[p] if p.is_file() else p.rglob('*')
  for f in files:
   if not f.is_file() or f.suffix.lower() not in {'.py','.mq5','.mqh'}: continue
   text=f.read_text(encoding='utf-8',errors='ignore')
   for token in FORBIDDEN:
    if token in text: failures.append(f'{f.relative_to(root)}: forbidden authority or side-effect token {token}')
 if failures: print('\n'.join(failures)); return 1
 print('UCE-I04 boundary check PASS: phase-owned code has no broker, network, or process authority'); return 0
if __name__=='__main__': raise SystemExit(main())
