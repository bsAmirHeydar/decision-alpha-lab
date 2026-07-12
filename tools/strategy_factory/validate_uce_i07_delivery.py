from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();errors=[]
required=[
 'mql5/Include/AlphaLab/StrategyFactory/TrainerSDK/UCEI07_All.mqh',
 'mql5/Experts/StrategyFactoryTests/UCE_I07_TrainerSDKSelfTest.mq5',
 'lab/11_strategy_factory/python/strategy_factory_trainers_v3/orchestrator.py',
 'lab/11_strategy_factory/python/strategy_factory_trainers_v3/conformance.py',
 'lab/11_strategy_factory/schemas/v3/trainer_capability_descriptor.schema.json',
 'lab/11_strategy_factory/schemas/v3/task_orchestration_plan.schema.json',
 'lab/11_strategy_factory/schemas/v3/model_artifact_manifest.schema.json',
 'lab/11_strategy_factory/test_vectors/v3/uce_i07_trainer_conformance_vectors.json',
 'docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i07/00_UCE_I07_DELIVERY_MOC.md',
 'lab/11_strategy_factory/implementation_program/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I07.json',
 'lab/11_strategy_factory/implementation_program/universal_context_exploitation_engine/v3_implementation/artifacts/UCE_I07_ACCEPTANCE_EVIDENCE.json']
for rel in required:
 if not (root/rel).is_file():errors.append('missing '+rel)
for rel in required:
 f=root/rel
 if f.suffix=='.json' and f.exists():
  try:json.loads(f.read_text(encoding='utf-8'))
  except Exception as e:errors.append(f'invalid json {rel}: {e}')
# Validate every I07 schema and vector as JSON.
for folder in [root/'lab/11_strategy_factory/schemas/v3',root/'lab/11_strategy_factory/test_vectors/v3']:
 for f in folder.glob('*i07*.json') if folder.exists() else ():
  try:json.loads(f.read_text(encoding='utf-8'))
  except Exception as e:errors.append(f'invalid json {f.relative_to(root)}: {e}')
docs=root/'docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i07'
if docs.exists() and len(list(docs.rglob('*.md')))<30:errors.append('insufficient detailed Obsidian delivery documentation')
if errors:print('\n'.join(errors));raise SystemExit(1)
print('UCE-I07 delivery validation PASS: canonical SDK, schemas, vectors, phase evidence, and detailed English Obsidian delivery present')
