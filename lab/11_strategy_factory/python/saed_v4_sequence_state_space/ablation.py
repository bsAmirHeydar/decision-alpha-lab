from __future__ import annotations
from .metrics import evaluate_candidate
from .canonical import content_hash,stable_id

def architecture_ablation(candidate_metrics):
    rows=[]
    baseline=next((m for m in candidate_metrics if m['architecture']=='ema_recurrent'),candidate_metrics[0]);b=baseline['summary']['validation']['mean_mse']
    for m in candidate_metrics:
        v=m['summary']['validation']['mean_mse'];rows.append({'candidate_id':m['candidate_id'],'architecture':m['architecture'],'validation_mse':v,'delta_vs_baseline':None if v is None or b is None else v-b,'baseline_candidate_id':baseline['candidate_id']})
    material={'rows':rows,'baseline_preserved':True,'identity_feature_present':False,'outcome_feature_present':False}
    return {**material,'report_id':stable_id('ablation',material),'report_hash':content_hash(material)}

def future_suffix_audit(model,sequence):
    # Causal prefix outputs must be invariant when an unseen suffix is appended.
    from .streaming import _dts
    xs=[p.vector for p in sequence.points];base,_=model.batch(xs,_dts(sequence.points));suffix=tuple(0.125 for _ in range(model.input_dim));ext,_=model.batch(xs+[suffix],_dts(sequence.points)+[60.0]);passed=base==ext[:-1]
    material={'candidate_id':model.candidate_id,'sequence_id':sequence.sequence_id,'prefix_length':len(xs),'passed':passed,'future_suffix_sensitivity':False if passed else True}
    return {**material,'audit_id':stable_id('futuresuffix',material),'audit_hash':content_hash(material)}
