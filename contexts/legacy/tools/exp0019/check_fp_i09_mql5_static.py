from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
inc=root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I09'
files=list(inc.glob('*.mqh'))
checks={'includes_present':len(files)>=8,'all_guarded':all('#ifndef' in p.read_text(encoding='utf-8') for p in files),'unset_consumption':any('CONSUMPTION_POLICY "UNSET"' in p.read_text(encoding='utf-8') for p in files),'no_period_current':all('PERIOD_CURRENT' not in p.read_text(encoding='utf-8') for p in files)}
print(json.dumps(checks,indent=2)); raise SystemExit(0 if all(checks.values()) else 1)
