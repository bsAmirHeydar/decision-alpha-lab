#!/usr/bin/env python3
from pathlib import Path
import sys,re
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();base=root/'mql5/Include/FaerieProtocol/EXP0019/Compatibility';errors=[]
required={'FP_I01_Enums.mqh','FP_I01_Types.mqh','FP_I01_Fingerprint.mqh','FP_I01_DependencyPins.mqh','FP_I01_CGAdapters.mqh','FP_I01_DAYEAdapters.mqh','FP_I01_Registry.mqh','FP_I01_SelfTest.mqh','FP_I01_All.mqh'}
actual={p.name for p in base.glob('*.mqh')}
if actual!=required:errors.append(f'header set mismatch missing={required-actual} extra={actual-required}')
for p in base.glob('*.mqh'):
 text=p.read_text(encoding='utf-8')
 if text.count('{')!=text.count('}'):errors.append(f'brace mismatch: {p.name}')
 guards=re.findall(r'#ifndef\s+([A-Z0-9_]+)',text)
 if not guards:errors.append(f'missing include guard: {p.name}')
 for line in text.splitlines():
  if '#include "' in line:
   name=line.split('"')[1]
   if not (base/name).exists():errors.append(f'unresolved local include {name} in {p.name}')
registry=(base/'FP_I01_Registry.mqh').read_text()
if 'return 8;' not in registry or registry.count('case ')!=8:errors.append('registry count mismatch')
adapters=(base/'FP_I01_CGAdapters.mqh').read_text()+(base/'FP_I01_DAYEAdapters.mqh').read_text()
if adapters.count('const ')<8:errors.append('source parameters are not const')
for entry in ('mql5/Tests/Experts/FaerieProtocol/EXP0019_FP_I01_CompatibilitySelfTest.mq5','mql5/Experts/FaerieProtocol/EXP0019_FP_I01_CompatibilityDiagnostic.mq5'):
 if not (root/entry).is_file():errors.append('missing '+entry)
if errors:print('\n'.join(errors));raise SystemExit(1)
print('FP-I01 MQL5 static PASS: 9 headers, 8 adapters, 2 entry points, guards/includes/braces valid. MetaEditor compile remains separate.')
