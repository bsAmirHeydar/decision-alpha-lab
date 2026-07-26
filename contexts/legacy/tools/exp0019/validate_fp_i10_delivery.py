from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
ph=root/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i10'
checks={
'python_modules':len(list((ph/'python/fp_i10_indicator').glob('*.py')))>=18,
'tests':len(list((ph/'tests').glob('test_*.py')))>=14,
'schemas':len(list((ph/'schemas').glob('*.schema.json')))==15,
'mql5_includes':len(list((root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I10').glob('*.mqh')))>=10,
'indicator_entry':(root/'mql5/Indicators/EXP0019/FaerieProtocol/EXP0019_FaerieProtocol_Context.mq5').exists(),
'self_test':(root/'mql5/Tests/Indicators/EXP0019/FaerieProtocol/EXP0019_FP_I10_IndicatorSelfTest.mq5').exists(),
'docs':len(list((root/'docs/operations/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i10').rglob('*.md')))>=45,
}
print(json.dumps(checks,indent=2)); raise SystemExit(0 if all(checks.values()) else 1)
