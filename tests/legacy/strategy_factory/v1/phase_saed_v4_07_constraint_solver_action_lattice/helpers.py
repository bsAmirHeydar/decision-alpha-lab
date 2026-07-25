from tools.repository_paths import find_repository_root
from pathlib import Path
import copy,json
from saed_v4_action_lattice.service import ActionLatticeService
ROOT=find_repository_root(__file__)
EX=ROOT/'examples/legacy/strategy_factory/saed_v4_07'
UP=ROOT/'examples/legacy/strategy_factory/saed_v4_06'
def load(name,up=False):return json.loads(((UP if up else EX)/name).read_text())
def inputs():return load('golden_treatment_dsl_package.json',True),load('v4_06_to_v4_07_handoff.json',True),load('institutional_action_lattice_policy.json'),load('golden_parameter_domain_registry.json'),load('golden_solver_request.json')
def solve():
 p,h,pol,d,r=inputs();return ActionLatticeService().solve(package=p,handoff=h,policy_document=pol,domain_registry=d,request=r)
