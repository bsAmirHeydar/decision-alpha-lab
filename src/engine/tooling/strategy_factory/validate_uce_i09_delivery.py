from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();errors=[]
required=['mql5/Include/AlphaLab/StrategyFactory/AdvancedTasks/UCEI09_All.mqh','mql5/Tests/Experts/StrategyFactory/UCE_I09_AdvancedTasksSelfTest.mq5','src/engine/packages/strategy_factory_advanced_tasks_v3/catalog.py','src/engine/packages/strategy_factory_advanced_tasks_v3/policy.py','schemas/legacy/strategy_factory/v3/advanced_algorithm_descriptor.schema.json','schemas/legacy/strategy_factory/v3/policy_support_audit.schema.json','tests/fixtures/legacy/strategy_factory/v3/uce_i09_advanced_task_conformance_vectors.json','docs/history/systems/ucee/implementation_program/phase_deliveries/uce_i09/00_UCE_I09_DELIVERY_MOC.md','releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I09.json','releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/UCE_I09_ACCEPTANCE_EVIDENCE.json']
for rel in required:
 if not (root/rel).is_file():errors.append('missing '+rel)
for folder in [root/'schemas/legacy/strategy_factory/v3',root/'tests/fixtures/legacy/strategy_factory/v3']:
 for f in folder.glob('*i09*.json') if folder.exists() else ():
  try:json.loads(f.read_text(encoding='utf-8'))
  except Exception as e:errors.append(f'invalid json {f.relative_to(root)}: {e}')
docs=root/'docs/history/systems/ucee/implementation_program/phase_deliveries/uce_i09'
if docs.exists() and len(list(docs.rglob('*.md')))<25:errors.append('insufficient detailed English Obsidian documentation')
if errors:print('\n'.join(errors));raise SystemExit(1)
print('UCE-I09 delivery validation PASS: advanced task pack, schemas, vectors, phase evidence, and detailed English Obsidian documentation present')
