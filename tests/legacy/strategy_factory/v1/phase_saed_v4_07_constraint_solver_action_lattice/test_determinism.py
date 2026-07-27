import copy,random
from .helpers import inputs
from saed_v4_action_lattice.service import ActionLatticeService
def test_repeated_identity():
 p,h,pol,d,r=inputs();s=ActionLatticeService();a=s.solve(package=p,handoff=h,policy_document=pol,domain_registry=d,request=r);b=s.solve(package=p,handoff=h,policy_document=pol,domain_registry=d,request=r);assert a==b
def test_input_order_independence():
 p,h,pol,d,r=inputs();random.Random(7).shuffle(p['programs']);random.Random(9).shuffle(d['domains']);o=ActionLatticeService().solve(package=p,handoff=h,policy_document=pol,domain_registry=d,request=r);from .helpers import load;assert o['action_lattice']['lattice_hash']==load('golden_action_lattice.json')['lattice_hash']
