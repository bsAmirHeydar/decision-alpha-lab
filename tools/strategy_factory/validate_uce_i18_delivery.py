#!/usr/bin/env python3
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
errors=[]
def need(rel):
 p=ROOT/rel
 if not p.exists(): errors.append('missing:'+rel)
 return p
pkg=need('lab/11_strategy_factory/python/strategy_factory_qualification_v3')
tests=need('lab/11_strategy_factory/tests/phase_uce_i18_production_qualification')
docs=need('docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i18')
atoms=need('docs/strategy_factory_universal_context_exploitation_engine/implementation_program/atomic_concepts/uce_i18')
mql=need('mql5/Include/AlphaLab/StrategyFactory/Qualification')
art=need('lab/11_strategy_factory/implementation_program/universal_context_exploitation_engine/v3_implementation/artifacts/uce_i18')
if pkg.exists() and len(list(pkg.glob('*.py')))<15: errors.append('python_module_count_below_15')
schemas=list((ROOT/'lab/11_strategy_factory/schemas/v3').glob('qualification_*.schema.json'))
if len(schemas)<24: errors.append(f'schema_count:{len(schemas)}')
for p in schemas:
 d=json.loads(p.read_text())
 if d.get('additionalProperties') is not False: errors.append('open_schema:'+p.name)
if docs.exists() and len(list(docs.glob('*.md')))<50: errors.append('documentation_count_below_50')
if atoms.exists() and len(list(atoms.glob('*.md')))<12: errors.append('atomic_concept_count_below_12')
if mql.exists() and len(list(mql.glob('*.mqh')))<13: errors.append('mql_include_count_below_13')
for name in ('reference_environment.json','qualification_policy.json','reference_blocked_qualification_report.json','uce_i18_evidence_bundle.json','limitations.json','external_evidence_template.json','acceptance_matrix.json'):
 need('lab/11_strategy_factory/implementation_program/universal_context_exploitation_engine/v3_implementation/artifacts/uce_i18/'+name)
blocked=art/'reference_blocked_qualification_report.json'
if blocked.exists() and json.loads(blocked.read_text()).get('activation_allowed') is not False: errors.append('unsafe_reference_activation_claim')
lim=art/'limitations.json'
if lim.exists() and json.loads(lim.read_text()).get('activation_allowed') is not False: errors.append('unsafe_limitation_activation_claim')
print(json.dumps({'phase':'UCE-I18','status':'pass' if not errors else 'fail','errors':errors,'counts':{'python_modules':len(list(pkg.glob('*.py'))) if pkg.exists() else 0,'schemas':len(schemas),'docs':len(list(docs.glob('*.md'))) if docs.exists() else 0,'atoms':len(list(atoms.glob('*.md'))) if atoms.exists() else 0}},indent=2))
raise SystemExit(1 if errors else 0)
