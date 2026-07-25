from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();errors=[]
required=['mql5/Include/AlphaLab/StrategyFactory/ClassicalAlgorithms/UCEI08_All.mqh','mql5/Tests/Experts/StrategyFactory/UCE_I08_ClassicalAlgorithmsSelfTest.mq5','src/engine/packages/strategy_factory_classical_v3/catalog.py','src/engine/packages/strategy_factory_classical_v3/benchmark.py','schemas/legacy/strategy_factory/v3/algorithm_descriptor.schema.json','schemas/legacy/strategy_factory/v3/classical_comparison_gate.schema.json','tests/fixtures/legacy/strategy_factory/v3/uce_i08_classical_conformance_vectors.json','docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i08/00_UCE_I08_DELIVERY_MOC.md','releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I08.json','releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/UCE_I08_ACCEPTANCE_EVIDENCE.json']
for rel in required:
 if not (root/rel).is_file():errors.append('missing '+rel)
for folder in [root/'schemas/legacy/strategy_factory/v3',root/'tests/fixtures/legacy/strategy_factory/v3']:
 for f in folder.glob('*i08*.json') if folder.exists() else ():
  try:json.loads(f.read_text(encoding='utf-8'))
  except Exception as e:errors.append(f'invalid json {f.relative_to(root)}: {e}')
docs=root/'docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i08'
if docs.exists() and len(list(docs.rglob('*.md')))<20:errors.append('insufficient detailed English Obsidian documentation')
if errors:print('\n'.join(errors));raise SystemExit(1)
print('UCE-I08 delivery validation PASS: algorithm pack, schemas, vectors, phase evidence, and detailed English Obsidian documentation present')
