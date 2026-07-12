from strategy_factory_treatment_compiler_v3.golden import compile_golden
from strategy_factory_treatments_v3.enums import TradeSide
def test_deterministic_compile():
 a,_=compile_golden(); b,_=compile_golden(); assert a.treatment_id==b.treatment_id; assert a.action_order==b.action_order
def test_side_is_identity_affecting():
 a,_=compile_golden(TradeSide.LONG); b,_=compile_golden(TradeSide.SHORT); assert a.treatment_id!=b.treatment_id
def test_all_behavior_parameters_are_serialized():
 a,_=compile_golden(); d=a.to_dict(); assert d['selections']; assert all('parameters' in x for x in d['selections'])
