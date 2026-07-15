from pathlib import Path
import json
import os
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_treatment_dsl.catalog import institutional_capability_profile,institutional_policy,institutional_registry
from saed_v4_treatment_dsl.parser import parse_program
from saed_v4_treatment_dsl.serialization import to_document
from saed_v4_treatment_dsl.service import TreatmentDslService

EX=ROOT/'lab/11_strategy_factory/examples/saed_v4_06';V405=ROOT/'lab/11_strategy_factory/examples/saed_v4_05'
load=lambda p: json.loads(p.read_text(encoding='utf-8'))
sources=tuple(parse_program(load(EX/name)) for name in ('golden_treatment_program_source.json','system_skip_program_source.json','system_abstain_program_source.json'))
package=TreatmentDslService().build_package(graph=load(V405/'golden_semantic_temporal_hypergraph.json'),handoff=load(V405/'v4_05_to_v4_06_handoff.json'),registry=institutional_registry(),policy=institutional_policy(),capability_profile=institutional_capability_profile(),sources=sources)
actual=json.loads(json.dumps(to_document(package),sort_keys=True));expected=load(EX/'golden_treatment_dsl_package.json')
if actual!=expected:
    raise SystemExit('golden package reproduction mismatch')
print(json.dumps({'package_id':package.package_id,'package_hash':package.package_hash,'program_count':len(package.programs),'binding_count':len(package.bindings)},sort_keys=True))
