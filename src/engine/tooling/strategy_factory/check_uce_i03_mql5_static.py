#!/usr/bin/env python3
from pathlib import Path
import re,sys
def main():
 root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); owned=root/'mql5/Include/AlphaLab/StrategyFactory/TreatmentAtoms'; files=list(owned.glob('*.mqh'))+[root/'mql5/Experts/StrategyFactory/UCE_I03_TreatmentAtomsDiagnostic.mq5',root/'mql5/Tests/Experts/StrategyFactory/UCE_I03_TreatmentAtomsSelfTest.mq5']; failures=[]
 required={'UCEI03_All.mqh','UCEI03_Enums.mqh','UCEI03_Contracts.mqh','UCEI03_Catalog.mqh','UCEI03_Conformance.mqh'}
 missing=required-{p.name for p in owned.glob('*.mqh')}
 if missing: failures.append('missing headers: '+','.join(sorted(missing)))
 for p in files:
  if not p.exists(): failures.append(f'missing file: {p}'); continue
  text=p.read_text(encoding='utf-8',errors='ignore')
  if 'Long'+'ToString(' in text: failures.append(f'{p.name}: unsupported long conversion')
  clean=re.sub(r'//.*|/\*.*?\*/|"(?:\\.|[^"\\])*"','',text,flags=re.S)
  if clean.count('{')!=clean.count('}'): failures.append(f'{p.name}: brace mismatch')
  for inc in re.findall(r'#include\s+"([^"]+)"',text):
   target=(p.parent/inc).resolve()
   if not target.exists(): failures.append(f'{p.name}: unresolved local include {inc}')
 if failures:
  print('\n'.join(failures)); return 1
 print(f'UCE-I03 MQL5 static check PASS: {len(files)} files; MetaEditor compile remains local'); return 0
if __name__=='__main__': raise SystemExit(main())
