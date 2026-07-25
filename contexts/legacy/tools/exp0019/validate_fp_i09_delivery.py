from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
ph=root/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i09'
checks={
 'python_modules':len(list((ph/'python/fp_i09_ledger').glob('*.py')))>=15,
 'tests':len(list((ph/'tests').glob('test_*.py')))>=10,
 'schemas':len(list((ph/'schemas').glob('*.json')))==15,
 'mql5_includes':len(list((root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I09').glob('*.mqh')))>=8,
 'entrypoints':(root/'mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I09_LedgerDiagnostic.mq5').exists() and (root/'mql5/Tests/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I09_LedgerSelfTest.mq5').exists(),
 'docs':len(list((root/'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i09').rglob('*.md')))>=40,
}
print(json.dumps(checks,indent=2)); raise SystemExit(0 if all(checks.values()) else 1)
