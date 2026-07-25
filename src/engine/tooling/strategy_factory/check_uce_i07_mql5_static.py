from pathlib import Path
import re,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
owned=root/'mql5/Include/AlphaLab/StrategyFactory/TrainerSDK'
targets=list(owned.rglob('*.mqh'))+[
 root/'mql5/Experts/StrategyFactory/UCE_I07_TrainerSDKDiagnostic.mq5',
 root/'mql5/Tests/Experts/StrategyFactory/UCE_I07_TrainerSDKSelfTest.mq5',
 root/'mql5/Tests/Experts/StrategyFactory/UCE_I07_CapabilityParitySelfTest.mq5']
errors=[]
for f in targets:
 if not f.is_file():errors.append(f'missing {f}');continue
 text=f.read_text(encoding='utf-8',errors='ignore')
 if 'LongToString(' in text:errors.append(f'{f}: unsupported LongToString')
 if text.count('{')!=text.count('}'):errors.append(f'{f}: brace imbalance')
 if text.count('(')!=text.count(')'):errors.append(f'{f}: parenthesis imbalance')
 for inc in re.findall(r'#include\s+"([^"]+)"',text):
  if not (f.parent/inc).exists():errors.append(f'{f}: missing local include {inc}')
 if re.search(r'\b(OrderSend|OrderCheck|PositionOpen|WebRequest)\s*\(',text):errors.append(f'{f}: forbidden runtime authority')
if errors:print('\n'.join(errors));raise SystemExit(1)
print(f'UCE-I07 MQL5 static PASS: {len(targets)} files, include resolution, delimiters, compatibility, and no-authority checks')
