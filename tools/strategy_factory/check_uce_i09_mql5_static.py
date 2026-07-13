from pathlib import Path
import re,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();targets=list((root/'mql5/Include/AlphaLab/StrategyFactory/AdvancedTasks').rglob('*.mqh'))+[root/'mql5/Experts/StrategyFactory/UCE_I09_AdvancedTasksDiagnostic.mq5',root/'mql5/Experts/StrategyFactoryTests/UCE_I09_AdvancedTasksSelfTest.mq5',root/'mql5/Experts/StrategyFactoryTests/UCE_I09_ActionSupportSafetySelfTest.mq5'];errors=[]
for f in targets:
 if not f.is_file():errors.append('missing '+str(f));continue
 text=f.read_text(encoding='utf-8',errors='ignore')
 if 'LongToString(' in text:errors.append(f'{f}: unsupported LongToString')
 if text.count('{')!=text.count('}'):errors.append(f'{f}: brace imbalance')
 if text.count('(')!=text.count(')'):errors.append(f'{f}: parenthesis imbalance')
 for inc in re.findall(r'#include\s+"([^"]+)"',text):
  if not (f.parent/inc).exists():errors.append(f'{f}: missing local include {inc}')
 if re.search(r'\b(OrderSend|OrderCheck|PositionOpen|WebRequest)\s*\(',text):errors.append(f'{f}: forbidden runtime authority')
if errors:print('\n'.join(errors));raise SystemExit(1)
print(f'UCE-I09 MQL5 static PASS: {len(targets)} files, local includes, delimiters, compatibility, and no-authority checks')
