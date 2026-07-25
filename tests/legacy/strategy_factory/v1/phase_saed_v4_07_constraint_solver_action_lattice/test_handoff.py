from helpers import load,solve
from saed_v4_action_lattice.handoff import build_v4_08_handoff
from saed_v4_action_lattice.integrity import build_integrity_receipt
from saed_v4_action_lattice.partition import build_partition_manifest
def test_v408_handoff_exact():
 o=solve();p=load('golden_treatment_dsl_package.json',True);h=load('v4_06_to_v4_07_handoff.json',True);pol=load('institutional_action_lattice_policy.json');d=load('golden_parameter_domain_registry.json');q=load('golden_solver_request.json');i=build_integrity_receipt(package=p,handoff=h,policy=pol,registry=d,request=q,result=o['solver_result'],lattice=o['action_lattice']);part=build_partition_manifest(o['action_lattice'],8);assert build_v4_08_handoff(o['solver_result'],o['action_lattice'],i,part)==load('v4_07_to_v4_08_handoff.json')
def test_handoff_authority_bounded():
 x=load('v4_07_to_v4_08_handoff.json');assert x['authority']['build_executable_path_outcome_cube'];assert not any(x['authority'][k] for k in ('select_treatment','train_model','allocate_risk','activate_runtime','send_order'))
