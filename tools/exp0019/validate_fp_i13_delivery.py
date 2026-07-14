from pathlib import Path
import json,sys
root=Path(__file__).resolve().parents[2]
phase=root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i13'
required=[phase/'python/fp_i13_release',phase/'tests',phase/'schemas',phase/'artifacts',root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I13',root/'mql5/Indicators/EXP0019/FaerieProtocolTests/EXP0019_FP_I13_ReleaseSelfTest.mq5']
missing=[str(x) for x in required if not x.exists()]
print(json.dumps({'status':'PASS' if not missing else 'FAIL','missing':missing,'python_modules':len(list((phase/'python/fp_i13_release').glob('*.py'))),'tests':len(list((phase/'tests').glob('test_*.py'))),'schemas':len(list((phase/'schemas').glob('*.json'))),'mql5_includes':len(list((root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I13').glob('*.mqh')))},indent=2))
raise SystemExit(1 if missing else 0)
