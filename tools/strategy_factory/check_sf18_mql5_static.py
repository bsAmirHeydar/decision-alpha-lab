#!/usr/bin/env python3
from pathlib import Path
import re,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
owned=[root/'mql5/Include/AlphaLab/StrategyFactory/Live',root/'mql5/Experts/StrategyFactory/SF18_MicroLiveHost.mq5',root/'mql5/Experts/StrategyFactory/SF18_LiveSafetyDiagnostic.mq5',root/'mql5/Experts/StrategyFactoryTests/SF18_LiveSafetySelfTest.mq5']
errors=[]
for base in owned:
    files=[base] if base.is_file() else list(base.rglob('*.mqh'))+list(base.rglob('*.mq5'))
    for p in files:
        text=p.read_text(encoding='utf-8',errors='ignore')
        if 'LongToString(' in text: errors.append(f'unsupported LongToString: {p}')
        if re.search(r'=\s*StringTo(?:Upper|Lower)\s*\(',text): errors.append(f'case mutation assignment: {p}')
        stripped=re.sub(r'/\*.*?\*/|//.*','',text,flags=re.S)
        if stripped.count('{')!=stripped.count('}'): errors.append(f'brace mismatch: {p}')
print(f'SF18 MQL5 static preflight: errors={len(errors)}')
for e in errors: print('ERROR:',e)
raise SystemExit(1 if errors else 0)
