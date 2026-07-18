from __future__ import annotations
from typing import Any
from .canonical import digest_object,with_digest
from .policies import GATE_IDS
from .statistics import binomial_upper_tail,wilson_lower,max_drawdown,population_std

def result(gate_id:str,status:str,reason_codes:list[str],metrics:dict[str,Any],evidence:list[str])->dict[str,Any]:
    body={'schema_version':'1.0.0','gate_id':gate_id,'status':status,'reason_codes':sorted(set(reason_codes)),'metrics':metrics,'evidence_digests':sorted(set(evidence))}
    return with_digest(body,'gate_result_digest')

def preliminary(candidate:dict[str,Any],segments:dict[str,dict[str,Any]],policy:dict[str,Any],input_integrity_digest:str)->dict[str,Any]:
    t=policy['thresholds']; out={}
    lane=candidate['lane']; origin=candidate['origin']; support=candidate['support']; signals=candidate['signals']; coverage=candidate['coverage']; accuracy=candidate['accuracy']; effect=None if accuracy is None else accuracy-0.5
    ev=[candidate['candidate_result_digest']]+[segments[x]['segment_result_digest'] for x in sorted(segments)]
    out['INPUT_INTEGRITY']=result('INPUT_INTEGRITY','PASS',['ACL06_BUNDLE_VERIFIED'],{'input_bundle_integrity':True},[input_integrity_digest])
    out['DATA_QUALITY_AND_LEAKAGE']=result('DATA_QUALITY_AND_LEAKAGE','PASS',['UPSTREAM_KNOWN_TIME_AND_SPLIT_EVIDENCE_VERIFIED'],{'known_time_contract':True,'purged_split_present':True},ev)
    if lane=='DIAGNOSTIC':
        out['DIAGNOSTIC_ISOLATION']=result('DIAGNOSTIC_ISOLATION','PASS',['DIAGNOSTIC_LANE_NON_SELECTABLE'],{'lane':lane,'selectable':False},ev)
    else:
        out['DIAGNOSTIC_ISOLATION']=result('DIAGNOSTIC_ISOLATION','PASS',['RESEARCH_LANE_CONFIRMED'],{'lane':lane,'selectable':True},ev)
    support_ok=support>=t['minimum_total_support'] and segments['TEST']['support']>=t['minimum_test_support']
    out['MINIMUM_SUPPORT']=result('MINIMUM_SUPPORT','PASS' if support_ok else 'FAIL',[] if support_ok else ['INSUFFICIENT_TOTAL_OR_TEST_SUPPORT'],{'total_support':support,'test_support':segments['TEST']['support'],'required_total':t['minimum_total_support'],'required_test':t['minimum_test_support']},ev)
    effect_ok=accuracy is not None and accuracy>=t['minimum_accuracy'] and effect>=t['minimum_effect_over_chance'] and candidate['mean_signed_forward_delta'] is not None and candidate['mean_signed_forward_delta']>0
    out['EFFECT_SIZE']=result('EFFECT_SIZE','PASS' if effect_ok else 'FAIL',[] if effect_ok else ['EFFECT_THRESHOLD_NOT_MET'],{'accuracy':accuracy,'effect_over_chance':effect,'mean_signed_forward_delta':candidate['mean_signed_forward_delta'],'minimum_accuracy':t['minimum_accuracy'],'minimum_effect_over_chance':t['minimum_effect_over_chance']},ev)
    p=binomial_upper_tail(candidate['correct'],candidate['signals'])
    wl=wilson_lower(candidate['correct'],candidate['signals'])
    stat_ok=p is not None and p<=t['maximum_fdr_q'] and wl is not None and wl>=t['minimum_wilson_lower']
    out['STATISTICAL_SIGNIFICANCE']=result('STATISTICAL_SIGNIFICANCE','PASS' if stat_ok else ('UNKNOWN' if p is None else 'FAIL'),[] if stat_ok else ['SIGNIFICANCE_OR_CONFIDENCE_BOUND_NOT_MET'],{'p_value_one_sided':p,'wilson_lower_95':wl,'maximum_nominal_p':t['maximum_fdr_q'],'minimum_wilson_lower':t['minimum_wilson_lower']},ev)
    accs=[segments[s]['accuracy'] for s in ('TRAIN','VALIDATION','TEST') if segments[s]['accuracy'] is not None]
    spread=None if not accs else max(accs)-min(accs); train=segments['TRAIN']['accuracy']; test=segments['TEST']['accuracy']; gap=None if train is None or test is None else train-test
    gen_ok=len(accs)==3 and spread<=t['maximum_segment_accuracy_spread'] and gap<=t['maximum_train_test_accuracy_gap'] and test>=t['minimum_accuracy']
    out['TEMPORAL_GENERALIZATION']=result('TEMPORAL_GENERALIZATION','PASS' if gen_ok else ('UNKNOWN' if len(accs)<3 else 'FAIL'),[] if gen_ok else ['SEGMENT_GENERALIZATION_NOT_ESTABLISHED'],{'segment_accuracies':{s:segments[s]['accuracy'] for s in ('TRAIN','VALIDATION','TEST')},'accuracy_spread':spread,'train_test_gap':gap},ev)
    overfit_ok=gen_ok and origin!='DIAGNOSTIC'
    out['OVERFIT_CONTROL']=result('OVERFIT_CONTROL','PASS' if overfit_ok else ('NOT_APPLICABLE' if lane=='DIAGNOSTIC' else 'FAIL'),[] if overfit_ok else ['OVERFIT_CONTROL_BATTERY_NOT_CLEARED'],{'train_test_gap':gap,'segment_spread':spread,'search_exposure_bound_upstream':True},ev)
    obs=[o for s in ('TRAIN','VALIDATION','TEST') for o in segments[s].get('observations',[]) if o.get('decision') not in (None,'NO_ACTION')]
    deltas=[float(o['signed_forward_delta']) for o in obs if o.get('signed_forward_delta') is not None]
    worst=min(deltas) if deltas else None; dd=max_drawdown(deltas); sd=population_std(deltas)
    robust_ok=len(deltas)>=t['minimum_tail_observations'] and worst is not None and worst>=-t['maximum_single_loss'] and (sum(deltas)/len(deltas)>0)
    out['DISTRIBUTIONAL_ROBUSTNESS']=result('DISTRIBUTIONAL_ROBUSTNESS','PASS' if robust_ok else ('UNKNOWN' if len(deltas)<t['minimum_tail_observations'] else 'FAIL'),[] if robust_ok else ['TAIL_EVIDENCE_INSUFFICIENT_OR_ADVERSE'],{'observation_count':len(deltas),'worst_observation':worst,'max_drawdown_proxy':dd,'population_std':sd},ev)
    econ=policy['evidence_availability']['execution_economics']
    out['EXECUTION_ECONOMICS']=result('EXECUTION_ECONOMICS','UNKNOWN' if not econ else 'PASS',['EXECUTION_ECONOMICS_EVIDENCE_MISSING'] if not econ else [],{'evidence_available':econ,'side_aware_cost_model_required':True},ev)
    ood=policy['evidence_availability']['ood_evaluation']
    abstention_ok=coverage is not None and t['minimum_coverage']<=coverage<=t['maximum_coverage']
    out['OOD_AND_ABSTENTION']=result('OOD_AND_ABSTENTION','UNKNOWN' if not ood else ('PASS' if abstention_ok else 'FAIL'),['OOD_EVIDENCE_MISSING'] if not ood else ([] if abstention_ok else ['COVERAGE_OUTSIDE_POLICY']),{'ood_evidence_available':ood,'coverage':coverage,'coverage_bounds':[t['minimum_coverage'],t['maximum_coverage']]},ev)
    prospective=policy['evidence_availability']['prospective_runs']
    out['PROSPECTIVE_EVIDENCE']=result('PROSPECTIVE_EVIDENCE','PASS' if prospective>=t['minimum_prospective_runs'] else 'UNKNOWN',[] if prospective>=t['minimum_prospective_runs'] else ['PROSPECTIVE_EVIDENCE_MISSING'],{'prospective_runs':prospective,'required':t['minimum_prospective_runs']},ev)
    reps=policy['evidence_availability']['independent_replications']
    out['INDEPENDENT_REPLICATION']=result('INDEPENDENT_REPLICATION','PASS' if reps>=t['minimum_independent_replications'] else 'UNKNOWN',[] if reps>=t['minimum_independent_replications'] else ['INDEPENDENT_REPLICATION_MISSING'],{'independent_replications':reps,'required':t['minimum_independent_replications']},ev)
    # populated after family-level calculations
    out['MULTIPLE_TESTING']=result('MULTIPLE_TESTING','UNKNOWN',['FAMILY_Q_VALUE_PENDING'],{'q_value':None},ev)
    out['BASELINE_DOMINANCE']=result('BASELINE_DOMINANCE','UNKNOWN',['BASELINE_COMPARISON_PENDING'],{'advantage':None},ev)
    assert set(out)==set(GATE_IDS)
    return out

def replace_family_gates(gates:dict[str,dict],candidate:dict,q_value:float|None,best_baseline_test_accuracy:float|None,policy:dict)->None:
    t=policy['thresholds']; ev=[candidate['candidate_result_digest']]
    if candidate['lane']=='DIAGNOSTIC':
        gates['MULTIPLE_TESTING']=result('MULTIPLE_TESTING','NOT_APPLICABLE',['DIAGNOSTIC_LANE_EXCLUDED_FROM_TESTING_FAMILY'],{'q_value':None},ev)
        gates['BASELINE_DOMINANCE']=result('BASELINE_DOMINANCE','NOT_APPLICABLE',['DIAGNOSTIC_LANE_EXCLUDED'],{'advantage':None},ev); return
    qok=q_value is not None and q_value<=t['maximum_fdr_q']
    gates['MULTIPLE_TESTING']=result('MULTIPLE_TESTING','PASS' if qok else ('UNKNOWN' if q_value is None else 'FAIL'),[] if qok else ['FDR_THRESHOLD_NOT_MET'],{'q_value':q_value,'maximum_fdr_q':t['maximum_fdr_q']},ev)
    if candidate['origin']=='BASELINE':
        gates['BASELINE_DOMINANCE']=result('BASELINE_DOMINANCE','NOT_APPLICABLE',['CANDIDATE_IS_BASELINE'],{'advantage':None,'best_baseline_test_accuracy':best_baseline_test_accuracy},ev); return
    test_acc=candidate.get('_test_accuracy'); advantage=None if test_acc is None or best_baseline_test_accuracy is None else test_acc-best_baseline_test_accuracy
    ok=advantage is not None and advantage>=t['minimum_baseline_accuracy_advantage']
    gates['BASELINE_DOMINANCE']=result('BASELINE_DOMINANCE','PASS' if ok else ('UNKNOWN' if advantage is None else 'FAIL'),[] if ok else ['BASELINE_DOMINANCE_NOT_ESTABLISHED'],{'test_accuracy':test_acc,'best_baseline_test_accuracy':best_baseline_test_accuracy,'advantage':advantage,'required_advantage':t['minimum_baseline_accuracy_advantage']},ev)
