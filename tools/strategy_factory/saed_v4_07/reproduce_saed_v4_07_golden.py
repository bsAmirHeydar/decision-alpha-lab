from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_action_lattice.service import ActionLatticeService
E=ROOT/'lab/11_strategy_factory/examples/saed_v4_07';U=ROOT/'lab/11_strategy_factory/examples/saed_v4_06'
load=lambda p:json.loads(p.read_text())
o=ActionLatticeService().solve(package=load(U/'golden_treatment_dsl_package.json'),handoff=load(U/'v4_06_to_v4_07_handoff.json'),policy_document=load(E/'institutional_action_lattice_policy.json'),domain_registry=load(E/'golden_parameter_domain_registry.json'),request=load(E/'golden_solver_request.json'))
if o['solver_result']!=load(E/'golden_solver_result.json') or o['action_lattice']!=load(E/'golden_action_lattice.json'):raise SystemExit('golden reproduction mismatch')
print('SAED V4-07 golden reproduction passed')
