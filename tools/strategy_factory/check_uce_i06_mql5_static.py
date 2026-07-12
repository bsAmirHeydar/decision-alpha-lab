from pathlib import Path
import re,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); owned=root/'mql5/Include/AlphaLab/StrategyFactory/OutcomeDataset'; errors=[]
for f in list(owned.rglob('*.mqh'))+[root/'mql5/Experts/StrategyFactory/UCE_I06_OutcomeDatasetDiagnostic.mq5',root/'mql5/Experts/StrategyFactoryTests/UCE_I06_OutcomeDatasetSelfTest.mq5',root/'mql5/Experts/StrategyFactoryTests/UCE_I06_LongShortCounterfactualSelfTest.mq5']:
 text=f.read_text(encoding='utf-8',errors='ignore')
 if 'LongToString(' in text:errors.append(f'{f}: unsupported LongToString')
 if text.count('{')!=text.count('}'):errors.append(f'{f}: brace imbalance')
 for inc in re.findall(r'#include\s+"([^"]+)"',text):
  if not (f.parent/inc).exists():errors.append(f'{f}: missing local include {inc}')
if errors:print('\n'.join(errors));raise SystemExit(1)
print('UCE-I06 MQL5 static PASS: include resolution, braces, and compatibility hazards')
