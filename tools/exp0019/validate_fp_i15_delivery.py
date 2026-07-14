from pathlib import Path
import json,sys
root=Path(__file__).resolve().parents[2]
ph=root/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i15'
checks={
 'python_modules':len(list((ph/'python/fp_i15_paper').glob('*.py'))),
 'tests':len(list((ph/'tests').glob('test_*.py'))),
 'schemas':len(list((ph/'schemas').glob('*.schema.json'))),
 'mql_includes':len(list((root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I15').glob('*.mqh'))),
 'docs':len(list((root/'docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i15').rglob('*.md'))),
}
minimum={'python_modules':20,'tests':15,'schemas':18,'mql_includes':13,'docs':60}
failed=[k for k,v in checks.items() if v<minimum[k]]
print(json.dumps({'phase':'FP-I15','checks':checks,'minimum':minimum,'status':'FAIL' if failed else 'PASS','failed':failed},indent=2))
raise SystemExit(1 if failed else 0)
