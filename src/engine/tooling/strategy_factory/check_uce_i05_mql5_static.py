from pathlib import Path
import sys,re
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); files=list((root/'mql5/Include/AlphaLab/StrategyFactory/Economics').rglob('*.mqh'))+list((root/'mql5/Experts/StrategyFactory').glob('UCE_I05*.mq5'))+list((root/'mql5/Tests/Experts/StrategyFactory').glob('UCE_I05*.mq5'))
errors=[]
for f in files:
 t=f.read_text(encoding='utf-8',errors='ignore')
 if t.count('{')!=t.count('}'): errors.append(f'{f}: brace mismatch')
 if 'LongToString(' in t: errors.append(f'{f}: forbidden LongToString')
 for inc in re.findall(r'#include\s+[<\"]([^>\"]+)',t):
  if inc.startswith('AlphaLab/'):
   p=root/'mql5/Include'/inc
   if not p.exists(): errors.append(f'{f}: missing include {inc}')
if errors: print('\n'.join(errors)); raise SystemExit(1)
print(f'UCE-I05 MQL5 static PASS: {len(files)} files')
