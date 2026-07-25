from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
from saed_v4_action_lattice.service import ActionLatticeService
E=ROOT/'examples/legacy/strategy_factory/saed_v4_07';U=ROOT/'examples/legacy/strategy_factory/saed_v4_06'
load=lambda p:json.loads(p.read_text())
o=ActionLatticeService().solve(package=load(U/'golden_treatment_dsl_package.json'),handoff=load(U/'v4_06_to_v4_07_handoff.json'),policy_document=load(E/'institutional_action_lattice_policy.json'),domain_registry=load(E/'golden_parameter_domain_registry.json'),request=load(E/'golden_solver_request.json'))
if o['solver_result']!=load(E/'golden_solver_result.json') or o['action_lattice']!=load(E/'golden_action_lattice.json'):raise SystemExit('golden reproduction mismatch')
print('SAED V4-07 golden reproduction passed')
