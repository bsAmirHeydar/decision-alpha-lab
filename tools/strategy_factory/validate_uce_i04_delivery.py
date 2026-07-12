#!/usr/bin/env python3
from pathlib import Path
import json,sys
REQUIRED=[
'mql5/Include/AlphaLab/StrategyFactory/TreatmentCompiler/UCEI04_All.mqh',
'mql5/Experts/StrategyFactoryTests/UCE_I04_TreatmentCompilerSelfTest.mq5',
'lab/11_strategy_factory/python/strategy_factory_treatment_compiler_v3/compiler.py',
'lab/11_strategy_factory/python/strategy_factory_treatment_compiler_v3/state_machine.py',
'lab/11_strategy_factory/test_vectors/v3/uce_i04_treatment_compiler_vectors.json',
'lab/11_strategy_factory/test_vectors/v3/uce_i04_golden_path_library.json',
'docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i04/00_UCE_I04_DELIVERY_MOC.md',
'lab/11_strategy_factory/implementation_program/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I04_HANDOFF_TO_UCE_I05.json']
def main():
 root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); failures=[x for x in REQUIRED if not (root/x).exists()]
 docs=root/'docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i04'
 if docs.exists() and len(list(docs.glob('*.md')))<25: failures.append('fewer than 25 UCE-I04 phase documents')
 schemas=root/'lab/11_strategy_factory/schemas/v3'
 if len(list(schemas.glob('*treatment*.schema.json')))<4: failures.append('insufficient treatment schemas')
 vec=root/'lab/11_strategy_factory/test_vectors/v3/uce_i04_treatment_compiler_vectors.json'
 if vec.exists():
  data=json.loads(vec.read_text())
  if not data.get('passed'): failures.append('conformance vector is not passed')
  if len(data.get('checks',{}))<6: failures.append('conformance vector lacks required checks')
 neg=root/'lab/11_strategy_factory/test_vectors/v3/uce_i04_negative_vectors.json'
 if neg.exists() and len(json.loads(neg.read_text()).get('cases',[]))<10: failures.append('insufficient negative vectors')
 if failures: print('UCE-I04 delivery validation FAIL');print('\n'.join(failures));return 1
 print('UCE-I04 delivery validation PASS');return 0
if __name__=='__main__': raise SystemExit(main())
