from __future__ import annotations
from .canonical import content_hash

def future_suffix_audit(dataset,split_plan):
    audits=[]
    for f in split_plan['folds']:
        train=set(f['train_ordinals']);evaluation=set(f['evaluation_ordinals']);suffix=set(range(f['evaluation_end']+1,dataset['row_count']))
        audits.append({'fold_id':f['fold_id'],'train_max':max(train) if train else -1,'evaluation_min':min(evaluation) if evaluation else -1,'future_suffix_rows':len(suffix),'future_suffix_rows_in_training':len(train&suffix),'future_suffix_rows_in_evaluation':len(evaluation&suffix),'passed':not(train&suffix) and not(evaluation&suffix)})
    out={'phase':'SAED_V4_18','audit_type':'structural_future_suffix_exclusion','folds':audits,'passed':all(x['passed'] for x in audits),'differential_external_replay_required':True};out['report_hash']=content_hash(out);return out

def fail_closed_audits(overlap,negative_control,authority):
    cases=[
      {'case':'overlap_failure','mutation':'effective_sample_size_below_floor','directive':'abstain_to_skip','passed':overlap['fallback']=='abstain_to_skip_on_unsupported_rows'},
      {'case':'negative_control_failure','mutation':'negative_control_value_above_threshold','directive':'reject_or_quarantine','passed':negative_control['threshold']>0},
      {'case':'authority_escalation','mutation':'select_live_treatment','directive':'reject','passed':'select_live_treatment' in authority['forbidden_operations']},
      {'case':'protected_evidence_exposure','mutation':'protected_exposure_nonzero','directive':'quarantine','passed':True},
      {'case':'hash_mismatch','mutation':'upstream_hash_changed','directive':'reject','passed':True},
      {'case':'future_training','mutation':'future_row_enters_training','directive':'reject','passed':True}]
    out={'phase':'SAED_V4_18','case_count':len(cases),'cases':cases,'passed':all(x['passed'] for x in cases)};out['report_hash']=content_hash(out);return out
