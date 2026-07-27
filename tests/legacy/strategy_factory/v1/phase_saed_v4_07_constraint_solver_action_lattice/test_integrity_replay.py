import copy
from .helpers import solve,load,inputs
from saed_v4_action_lattice.integrity import verify_integrity_receipt,build_integrity_receipt
from saed_v4_action_lattice.replay import build_replay_receipt
def test_golden_integrity_receipt_verifies():assert verify_integrity_receipt(load('golden_lattice_integrity_receipt.json'))
def test_tamper_fails():
 x=load('golden_lattice_integrity_receipt.json');x['lattice_hash']='0'*64;assert not verify_integrity_receipt(x)
def test_replay_passes():
 o=solve();r=build_replay_receipt({'lattice_hash':o['action_lattice']['lattice_hash'],'solver_result_hash':o['solver_result']['solver_result_hash']},{'lattice_hash':o['action_lattice']['lattice_hash'],'solver_result_hash':o['solver_result']['solver_result_hash']});assert r['status']=='passed'
