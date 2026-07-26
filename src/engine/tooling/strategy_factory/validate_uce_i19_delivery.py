#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
import json

ROOT=find_repository_root(__file__)
errors=[]
def need(rel: str) -> Path:
    path=ROOT/rel
    if not path.exists(): errors.append('missing:'+rel)
    return path
pkg=need('src/engine/packages/strategy_factory_operations_v3')
tests=need('tests/legacy/strategy_factory/v1/phase_uce_i19_production_operations')
docs=need('docs/history/systems/ucee/implementation_program/phase_deliveries/uce_i19')
atoms=need('docs/history/systems/ucee/implementation_program/atomic_concepts/uce_i19')
mql=need('mql5/Include/AlphaLab/StrategyFactory/Operations')
art=need('releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/uce_i19')
status=need('releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I19.json')
counts={
 'python_modules':len(list(pkg.glob('*.py'))) if pkg.exists() else 0,
 'tests':len(list(tests.glob('test_*.py'))) if tests.exists() else 0,
 'schemas':len(list((ROOT/'schemas/legacy/strategy_factory/v3').glob('operations_*.schema.json'))),
 'docs':len(list(docs.glob('*.md'))) if docs.exists() else 0,
 'atoms':len(list(atoms.glob('*.md'))) if atoms.exists() else 0,
 'mql_includes':len(list(mql.glob('*.mqh'))) if mql.exists() else 0,
 'mql_diagnostics':len(list((ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics').glob('EXP_UCE_I19_*.mq5'))),
 'artifacts':len(list(art.glob('*.json'))) if art.exists() else 0,
}
minimums={'python_modules':18,'tests':12,'schemas':28,'docs':55,'atoms':12,'mql_includes':18,'mql_diagnostics':4,'artifacts':10}
for key,minimum in minimums.items():
    if counts[key]<minimum: errors.append(f'{key}_below_{minimum}:{counts[key]}')
for path in (ROOT/'schemas/legacy/strategy_factory/v3').glob('operations_*.schema.json'):
    value=json.loads(path.read_text(encoding='utf-8'))
    if value.get('additionalProperties') is not False: errors.append('open_schema:'+path.name)
for name in ('reference_blocked_operations_bundle.json','reference_blocked_deployment_plan.json','limitations.json','acceptance_matrix.json'):
    path=art/name
    if not path.exists(): errors.append('missing_artifact:'+name); continue
    value=json.loads(path.read_text(encoding='utf-8'))
    if value.get('activation_allowed') is not False: errors.append('unsafe_reference_activation:'+name)
if status.exists() and json.loads(status.read_text(encoding='utf-8')).get('activation_allowed') is not False:
    errors.append('unsafe_phase_status_activation')
print(json.dumps({'phase':'UCE-I19','status':'pass' if not errors else 'fail','counts':counts,'errors':errors},indent=2))
raise SystemExit(1 if errors else 0)
