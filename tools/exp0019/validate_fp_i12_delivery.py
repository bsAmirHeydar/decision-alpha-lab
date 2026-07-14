from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
ph=root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i12'
checks={
 'python_modules':len(list((ph/'python/fp_i12_operator').glob('*.py')))>=15,
 'tests':len(list((ph/'tests').glob('test_*.py')))>=15,
 'schemas':len(list((ph/'schemas').glob('*.schema.json')))==15,
 'mql5_includes':len(list((root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I12').glob('*.mqh')))>=12,
 'production_indicator':(root/'mql5/Indicators/EXP0019/FaerieProtocol/EXP0019_FaerieProtocol_Context.mq5').exists(),
 'operator_self_test':(root/'mql5/Indicators/EXP0019/FaerieProtocolTests/EXP0019_FP_I12_OperatorUXSelfTest.mq5').exists(),
 'docs':len(list((root/'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i12').rglob('*.md')))>=60,
 'panel':(root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I12/FP_IndicatorPanel.mqh').exists(),
 'alerts':(root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I12/FP_AlertRouter.mqh').exists(),
 'exporter':(root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I12/FP_AuditExporter.mqh').exists(),
}
print(json.dumps(checks,indent=2));raise SystemExit(0 if all(checks.values()) else 1)
