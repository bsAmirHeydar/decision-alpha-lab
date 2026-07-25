#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
import json
ROOT=find_repository_root(__file__);errors=[];warnings=[]
def need(rel):
 p=ROOT/rel
 if not p.exists():errors.append('missing:'+rel)
 return p
pkg=need('src/engine/packages/strategy_factory_portfolio_v3');tests=need('tests/legacy/strategy_factory/v1/phase_uce_i17_portfolio');docs=need('docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i17');atoms=need('docs/strategy_factory_universal_context_exploitation_engine/implementation_program/atomic_concepts/uce_i17');mql=need('mql5/Include/AlphaLab/StrategyFactory/Portfolio');art=need('releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/uce_i17')
if pkg.exists() and len(list(pkg.glob('*.py')))<18:errors.append('python_module_count_below_18')
schemas=list((ROOT/'schemas/legacy/strategy_factory/v3').glob('portfolio_*.schema.json'))
if len(schemas)!=25:errors.append(f'schema_count:{len(schemas)}')
for p in schemas:
 d=json.loads(p.read_text())
 if d.get('additionalProperties') is not False:errors.append('open_schema:'+p.name)
if docs.exists() and len(list(docs.glob('*.md')))<46:errors.append('documentation_count_below_46')
if atoms.exists() and len(list(atoms.glob('*.md')))<12:errors.append('atomic_concept_count_below_12')
if mql.exists() and len(list(mql.glob('*.mqh')))<13:errors.append('mql_include_count_below_13')
for n in ('golden_opportunity_batch.json','golden_ranked_queue.json','golden_dependence_model.json','golden_capacity_quotes.json','golden_allocation_plan.json','golden_reservation_ledger.json','golden_stress_results.json','golden_validation_report.json','golden_runtime_bundle.json','golden_telemetry.json','uce_i17_evidence_bundle.json','limitations.json'):need('releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/uce_i17/'+n)
lim=art/'limitations.json'
if lim.exists() and json.loads(lim.read_text()).get('activation_allowed') is not False:errors.append('unsafe_activation_claim')
print(json.dumps({'phase':'UCE-I17','status':'pass' if not errors else 'fail','errors':errors,'warnings':warnings},indent=2));raise SystemExit(1 if errors else 0)
