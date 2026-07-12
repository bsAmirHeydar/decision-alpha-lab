#!/usr/bin/env python3
from pathlib import Path
import re,sys
REQUIRED={'UCEI04_All.mqh','UCEI04_Enums.mqh','UCEI04_Contracts.mqh','UCEI04_Compatibility.mqh','UCEI04_Compiler.mqh','UCEI04_PathStateMachine.mqh','UCEI04_IntrabarPolicy.mqh','UCEI04_Matrix.mqh','UCEI04_Manual.mqh','UCEI04_GoldenPaths.mqh','UCEI04_Conformance.mqh'}
def strip_code(text): return re.sub(r'//.*|/\*.*?\*/|"(?:\\.|[^"\\])*"','',text,flags=re.S)
def main():
 root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); owned=root/'mql5/Include/AlphaLab/StrategyFactory/TreatmentCompiler'; failures=[]
 files=list(owned.glob('*.mqh'))+[root/'mql5/Experts/StrategyFactory/UCE_I04_TreatmentCompilerDiagnostic.mq5',root/'mql5/Experts/StrategyFactoryTests/UCE_I04_TreatmentCompilerSelfTest.mq5']
 missing=REQUIRED-{p.name for p in owned.glob('*.mqh')}
 if missing: failures.append('missing headers: '+','.join(sorted(missing)))
 for p in files:
  if not p.exists(): failures.append(f'missing file: {p}'); continue
  text=p.read_text(encoding='utf-8',errors='ignore'); clean=strip_code(text)
  if 'Long'+'ToString(' in text: failures.append(f'{p.name}: unsupported LongToString')
  if clean.count('{')!=clean.count('}'): failures.append(f'{p.name}: brace mismatch')
  if clean.count('(')!=clean.count(')'): failures.append(f'{p.name}: parenthesis mismatch')
  for inc in re.findall(r'#include\s+"([^"]+)"',text):
   if not (p.parent/inc).resolve().exists(): failures.append(f'{p.name}: unresolved local include {inc}')
  if '#ifndef' in text and '#endif' not in text: failures.append(f'{p.name}: incomplete include guard')
 if failures: print('\n'.join(failures)); return 1
 print(f'UCE-I04 MQL5 static check PASS: {len(files)} files; MetaEditor compilation remains a local acceptance gate'); return 0
if __name__=='__main__': raise SystemExit(main())
