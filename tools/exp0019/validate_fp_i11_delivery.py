from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
ph=root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i11'
checks={
 'python_modules':len(list((ph/'python/fp_i11_visual').glob('*.py')))>=15,
 'tests':len(list((ph/'tests').glob('test_*.py')))>=15,
 'schemas':len(list((ph/'schemas').glob('*.schema.json')))==15,
 'mql5_includes':len(list((root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I11').glob('*.mqh')))>=10,
 'production_indicator':(root/'mql5/Indicators/EXP0019/FaerieProtocol/EXP0019_FaerieProtocol_Context.mq5').exists(),
 'visual_self_test':(root/'mql5/Indicators/EXP0019/FaerieProtocolTests/EXP0019_FP_I11_VisualSelfTest.mq5').exists(),
 'docs':len(list((root/'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i11').rglob('*.md')))>=60,
 'object_registry':(ph/'artifacts/FP_I11_OBJECT_REGISTRY.v1.json').exists(),
 'style_registry':(ph/'artifacts/FP_I11_STYLE_REGISTRY.v1.json').exists(),
}
print(json.dumps(checks,indent=2));raise SystemExit(0 if all(checks.values()) else 1)
