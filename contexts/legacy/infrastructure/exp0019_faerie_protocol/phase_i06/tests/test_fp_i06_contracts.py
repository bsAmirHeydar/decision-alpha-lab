from dataclasses import replace
import pytest
from fp_i02_kernel.enums import RelationCode,PriceSide,Direction
from fp_i06_relations.golden import golden_store_and_report
from fp_i06_relations.contracts import RelationCompilerConfig,RawDivergenceCandidate
from fp_i06_relations.registry import registry_hash
from fp_i06_relations.errors import FPI06Error

def test_config_rejects_ww_in_i06():
    _,pair,_,snapshot,_,_,_,_=golden_store_and_report(1)
    with pytest.raises(FPI06Error,match='WW'):
        RelationCompilerConfig('FP-CONTEXT-001',pair.pair_id,registry_hash(),snapshot.semantic_hash,enabled_relations=(RelationCode.WW,))
def test_config_rejects_noncanonical_duplicate_relations():
    _,pair,_,snapshot,_,_,_,_=golden_store_and_report(1)
    with pytest.raises(FPI06Error):RelationCompilerConfig('FP-CONTEXT-001',pair.pair_id,registry_hash(),snapshot.semantic_hash,enabled_relations=(RelationCode.AL,RelationCode.AL))
def test_relation_instance_identity_changes_with_offset():
    *_,report,_=golden_store_and_report(2)
    na=[i for i in report.compiled_instances if i.relation is RelationCode.NA]
    assert len(na)==2 and na[0].semantic_hash!=na[1].semantic_hash and na[0].relation_instance_id!=na[1].relation_instance_id
def test_side_plan_has_two_symbol_local_references():
    *_,report,_=golden_store_and_report(1)
    plan=report.side_plans[0]
    assert plan.left_symbol!=plan.right_symbol and plan.left_reference_id!=plan.right_reference_id
    assert len(plan.source_reference_hashes)==2
def test_direction_side_invariant_is_enforced():
    *_,report,_=golden_store_and_report(1);plan=report.side_plans[0]
    with pytest.raises(FPI06Error):RawDivergenceCandidate('x',plan.side_plan_id,plan.relation_instance_id,plan.relation,Direction.BULLISH,PriceSide.HIGH,plan.left_symbol,plan.right_symbol,plan.check_start_utc_ms,'fact',__import__('fp_i06_relations.enums',fromlist=['CandidateState']).CandidateState.RAW_ACTIVE,0,None,'',plan.check_end_utc_ms,'r','reason','a'*64)
def test_projection_metadata_does_not_exist_in_semantic_contracts():
    import fp_i06_relations.contracts as c
    assert not any('color' in name.lower() or 'opacity' in name.lower() for name in vars(c))
