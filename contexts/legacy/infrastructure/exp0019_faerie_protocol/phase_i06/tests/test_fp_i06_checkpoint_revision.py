from dataclasses import asdict
from fp_i06_relations.golden import golden_store_and_report
from fp_i06_relations.engine import build_engine_snapshot
from fp_i06_relations.checkpoint import create_checkpoint,validate_checkpoint
from fp_i06_relations.revision import revision_impact

def test_checkpoint_roundtrip():
    *_,config,report,_=golden_store_and_report(1);snapshot=build_engine_snapshot(config,report,(),1);cp=create_checkpoint(config,snapshot,report,2);payload={'config':config.config_hash,'source_revision':snapshot.source_revision_id,'compiler':report.evidence_hash,'snapshot':snapshot.semantic_hash,'created':2}
    assert validate_checkpoint(cp,config,snapshot.source_revision_id,report.evidence_hash,payload)==(True,'FP_HRC_CHECKPOINT_VALID')
def test_checkpoint_rejects_changed_revision():
    *_,config,report,_=golden_store_and_report(1);snapshot=build_engine_snapshot(config,report,(),1);cp=create_checkpoint(config,snapshot,report,2);payload={'config':config.config_hash,'source_revision':snapshot.source_revision_id,'compiler':report.evidence_hash,'snapshot':snapshot.semantic_hash,'created':2}
    assert validate_checkpoint(cp,config,'OTHER',report.evidence_hash,payload)[0] is False
def test_revision_invalidation_is_bounded_to_overlapping_plan():
    *_,report,_=golden_store_and_report(1);target=report.compiled_instances[0];impact=revision_impact(report,'REV2',(target.check_pair_window_id,),())
    assert impact['affected_side_plan_ids']
    instance_index={i.relation_instance_id:i for i in report.compiled_instances}
    plan_index={p.side_plan_id:p for p in report.side_plans}
    assert all(target.check_pair_window_id in (instance_index[plan_index[x].relation_instance_id].check_pair_window_id,instance_index[plan_index[x].relation_instance_id].reference_pair_window_id) for x in impact['affected_side_plan_ids'])
def test_unrelated_revision_has_no_affected_plan():
    *_,report,_=golden_store_and_report(1);impact=revision_impact(report,'REV2',('OTHER',),(0,))
    assert impact['affected_side_plan_ids']==()
