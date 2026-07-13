import pytest
from fp_i02_kernel.enums import PriceSide,RelationCode
from fp_i08_weekly.compiler import compile_ww
from fp_i08_weekly.contracts import WWConfig
from fp_i08_weekly.enums import WWDataState
from fp_i08_weekly.errors import FPI08Error
from helpers import weekly_store

def cfg(s): return WWConfig('FP-CONTEXT-001','PAIR.A.B',s.semantic_hash,'2'*64)
def test_compile_ww_creates_two_side_plans():
 s,p,c=weekly_store();r=compile_ww(cfg(s),s,p.descriptor.week_id,c.descriptor.week_id);assert r.instance is not None and len(r.side_plans)==2 and {x.side for x in r.side_plans}=={PriceSide.HIGH,PriceSide.LOW}
def test_compiled_i06_adapter_has_ww_relation():
 s,p,c=weekly_store();r=compile_ww(cfg(s),s,p.descriptor.week_id,c.descriptor.week_id);assert all(x.to_i06_plan().relation is RelationCode.WW for x in r.side_plans)
def test_missing_previous_week_blocks():
 s,p,c=weekly_store();r=compile_ww(cfg(s),s,'NYWEEK-MISSING',c.descriptor.week_id);assert r.instance is None and 'FP_WRC_PREVIOUS_WEEK_MISSING' in r.blocked_items
def test_previous_incomplete_marks_data_incomplete():
 s,p,c=weekly_store(previous_complete=False);r=compile_ww(cfg(s),s,p.descriptor.week_id,c.descriptor.week_id);assert r.instance.data_state is WWDataState.INCOMPLETE
def test_current_blocked_marks_data_incomplete():
 s,p,c=weekly_store(current_blocked=True);r=compile_ww(cfg(s),s,p.descriptor.week_id,c.descriptor.week_id);assert r.instance.data_state is WWDataState.INCOMPLETE
def test_consumed_reference_blocks_affected_plan():
 s,p,c=weekly_store(consume_high=True);r=compile_ww(cfg(s),s,p.descriptor.week_id,c.descriptor.week_id);high=next(x for x in r.side_plans if x.side is PriceSide.HIGH);assert high.data_state is WWDataState.INCOMPLETE
def test_store_hash_mismatch_fails_closed():
 s,p,c=weekly_store();bad=WWConfig('FP-CONTEXT-001','PAIR.A.B','f'*64,'2'*64)
 with pytest.raises(FPI08Error):compile_ww(bad,s,p.descriptor.week_id,c.descriptor.week_id)
