from dataclasses import replace
import pytest
from fp_i02_kernel.enums import RelationCode,PriceSide
from fp_i06_relations.golden import golden_store_and_report
from fp_i06_relations.compiler import compile_relations
from fp_i06_relations.errors import FPI06Error

def test_compiler_emits_three_same_day_and_three_offsets_per_historical_relation():
    _,_,_,_,_,_,report,_=golden_store_and_report(3)
    counts={code:sum(i.relation is code for i in report.compiled_instances) for code in RelationCode}
    assert counts[RelationCode.AL]==counts[RelationCode.AN]==counts[RelationCode.LN]==1
    assert counts[RelationCode.NA]==counts[RelationCode.NL]==counts[RelationCode.NN]==3
    assert counts[RelationCode.WW]==0
def test_each_instance_emits_high_and_low_plan():
    *_,report,_=golden_store_and_report(2)
    assert len(report.side_plans)==len(report.compiled_instances)*2
    for instance in report.compiled_instances:
        assert {p.side for p in report.side_plans if p.relation_instance_id==instance.relation_instance_id}=={PriceSide.HIGH,PriceSide.LOW}
def test_same_declaration_compiles_identically():
    _,_,anchor,snapshot,selection,config,first,_=golden_store_and_report(2)
    second=compile_relations(config,snapshot,anchor.isoformat(),selection)
    assert first==second
def test_store_hash_mismatch_fails():
    _,_,anchor,snapshot,selection,config,_,_=golden_store_and_report(1)
    with pytest.raises(FPI06Error):compile_relations(replace(config,reference_store_hash='f'*64),snapshot,anchor.isoformat(),selection)
def test_selection_lineage_mismatch_fails():
    _,_,anchor,snapshot,selection,config,_,_=golden_store_and_report(1)
    with pytest.raises(FPI06Error):compile_relations(config,snapshot,anchor.isoformat(),replace(selection,store_snapshot_hash='f'*64))
def test_historical_offsets_do_not_compress():
    _,_,_,_,selection,_,report,_=golden_store_and_report(3)
    assert tuple(i.offset for i in selection.items)==(1,2,3)
    assert sorted(i.calendar_offset for i in report.compiled_instances if i.relation is RelationCode.NA)==[1,2,3]
