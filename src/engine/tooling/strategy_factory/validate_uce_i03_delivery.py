#!/usr/bin/env python3
from pathlib import Path
import json,sys
REQUIRED=[
'mql5/Include/AlphaLab/StrategyFactory/TreatmentAtoms/UCEI03_All.mqh',
'mql5/Tests/Experts/StrategyFactory/UCE_I03_TreatmentAtomsSelfTest.mq5',
'src/engine/packages/strategy_factory_treatments_v3/catalog.py',
'tests/fixtures/legacy/strategy_factory/v3/uce_i03_treatment_atom_vectors.json',
'docs/history/systems/ucee/implementation_program/phase_deliveries/uce_i03/00_UCE_I03_DELIVERY_MOC.md',
'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I03_HANDOFF_TO_UCE_I04.json']
def main():
 root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); failures=[x for x in REQUIRED if not (root/x).exists()]
 docs=root/'docs/history/systems/ucee/implementation_program/phase_deliveries/uce_i03'
 if docs.exists() and len(list(docs.glob('*.md')))<19: failures.append('fewer than 19 phase delivery documents')
 vec=root/'tests/fixtures/legacy/strategy_factory/v3/uce_i03_treatment_atom_vectors.json'
 if vec.exists():
  data=json.loads(vec.read_text());
  if data.get('atom_count')!=50: failures.append('vector atom_count must equal 50')
 if failures:
  print('UCE-I03 delivery validation FAIL'); print('\n'.join(failures)); return 1
 print('UCE-I03 delivery validation PASS'); return 0
if __name__=='__main__': raise SystemExit(main())
