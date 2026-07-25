from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
root=find_repository_root(__file__)
ph=root/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i14'
checks={
 'python_modules':len(list((ph/'python/fp_i14_diagnostic').glob('*.py')))>=18,
 'test_modules':len(list((ph/'tests').glob('test_*.py')))>=15,
 'schemas':len(list((ph/'schemas').glob('*.json')))==18,
 'mql_includes':len(list((root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I14').glob('*.mqh')))>=12,
 'ea_entry':(root/'mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FaerieProtocol_Diagnostic.mq5').exists(),
 'self_test':(root/'mql5/Tests/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I14_DiagnosticSelfTest.mq5').exists(),
}
print(json.dumps(checks,indent=2));raise SystemExit(0 if all(checks.values()) else 1)
