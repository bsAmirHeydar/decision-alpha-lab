from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); errors=[]
required=[
 'mql5/Include/AlphaLab/StrategyFactory/OutcomeDataset/UCEI06_All.mqh',
 'src/engine/packages/strategy_factory_dataset_v3/dataset.py',
 'schemas/legacy/strategy_factory/v3/dataset_manifest.schema.json',
 'tests/fixtures/legacy/strategy_factory/v3/uce_i06_golden_dataset_vectors.json',
 'docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i06/00_UCE_I06_DELIVERY_MOC.md',
 'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I06.json']
for rel in required:
 if not (root/rel).is_file():errors.append('missing '+rel)
for p in (root/'schemas/legacy/strategy_factory/v3').glob('*.schema.json'):
 try:json.loads(p.read_text(encoding='utf-8'))
 except Exception as e:errors.append(f'invalid json {p}: {e}')
if errors:print('\n'.join(errors));raise SystemExit(1)
print('UCE-I06 delivery validation PASS: required artifacts and JSON schemas present')
