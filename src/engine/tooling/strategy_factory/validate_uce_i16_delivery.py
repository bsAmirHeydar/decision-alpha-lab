from __future__ import annotations
from tools.repository_paths import find_repository_root
import json,re,sys
from pathlib import Path
ROOT=find_repository_root(__file__)
errors=[];warnings=[]
def need(path):
 p=ROOT/path
 if not p.exists():errors.append(f'missing:{path}')
 return p
pkg=need('src/engine/packages/strategy_factory_onboarding_v3')
tests=need('tests/legacy/strategy_factory/v1/phase_uce_i16_context_onboarding')
docs=need('docs/history/systems/ucee/implementation_program/phase_deliveries/uce_i16')
concepts=need('docs/history/systems/ucee/implementation_program/atomic_concepts/uce_i16')
art=need('releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/uce_i16')
mql=need('mql5/Include/AlphaLab/StrategyFactory/ContextOnboarding')
if pkg.exists() and len(list(pkg.glob('*.py')))<17:errors.append('python_module_count_below_17')
schemas=list((ROOT/'schemas/legacy/strategy_factory/v3').glob('onboarding_*.schema.json'))
if len(schemas)!=25:errors.append(f'schema_count:{len(schemas)}')
for p in schemas:
 d=json.loads(p.read_text());
 if d.get('additionalProperties') is not False:errors.append(f'open_schema:{p.name}')
if docs.exists() and len(list(docs.glob('*.md')))<46:errors.append('documentation_count_below_46')
if concepts.exists() and len(list(concepts.glob('*.md')))<12:errors.append('atomic_concept_count_below_12')
if mql.exists() and len(list(mql.glob('*.mqh')))<13:errors.append('mql_include_count_below_13')
for p in list(mql.glob('*.mqh'))+list((ROOT/'mql5/Experts/StrategyFactory').glob('UCE_I16*.mq5'))+list((ROOT/'mql5/Tests/Experts/StrategyFactory').glob('UCE_I16*.mq5')):
 s=p.read_text(errors='ignore')
 for token in ('OrderSend(','OrderCheck(','CTrade ','WebRequest(','SocketCreate('):
  if token in s:errors.append(f'forbidden_authority:{p}:{token}')
required_artifacts=['golden_scaffold_manifest.json','golden_compiled_tournament_template.json','golden_invariance_report.json','golden_parity_report.json','wave_a_plan.json','wave_b_plan.json','wave_c_plan.json','uce_i16_evidence_bundle.json','limitations.json']
for name in required_artifacts:need(f'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/uce_i16/{name}')
for name in ('wave_a_source_inventory.json','wave_b_source_inventory.json','wave_c_source_inventory.json'):
 p=need(f'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/uce_i16/{name}')
 if p.exists():
  d=json.loads(p.read_text())
  if d.get('activation_policy')!='differential_parity_before_behavior_change':errors.append(f'unsafe_activation_policy:{name}')
index=ROOT/'releases/history/ucee/indexes/UCEE_I16_FILE_INDEX.txt'
if index.exists():
 paths=[x.strip() for x in index.read_text().splitlines() if x.strip()]
 core_prefixes=('src/engine/packages/strategy_factory_contracts_v3/','src/engine/packages/strategy_factory_economics_v3/','src/engine/packages/strategy_factory_experiments_v3/','src/engine/packages/strategy_factory_promotion_v3/','src/engine/packages/strategy_factory_policy_v3/','src/engine/packages/strategy_factory_runtime_v3/')
 bad=[x for x in paths if x.startswith(core_prefixes)]
 if bad:errors.append('central_engine_files_in_patch:'+','.join(bad))
print(json.dumps({'phase':'UCE-I16','errors':errors,'warnings':warnings,'status':'pass' if not errors else 'fail'},indent=2))
raise SystemExit(1 if errors else 0)
