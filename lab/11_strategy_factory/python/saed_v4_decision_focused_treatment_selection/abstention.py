from __future__ import annotations

def decide_abstention(ranked,selection_set,uncertainty,risk,baseline_id,skip_id,policy,proof_ok=True,support_ok=True):
    reasons=[]
    if policy.abstention_policy in {'margin','combined'} and len(ranked)>1 and ranked[0]['objective_score']-ranked[1]['objective_score']<risk.minimum_margin:reasons.append('insufficient_objective_margin')
    if policy.abstention_policy in {'uncertainty','combined'} and uncertainty['entropy']>risk.maximum_entropy:reasons.append('excessive_selection_entropy')
    if policy.abstention_policy in {'proof','combined'} and not proof_ok:reasons.append('proof_failure')
    if policy.abstention_policy in {'support','combined'} and not support_ok:reasons.append('support_failure')
    baseline=next((r for r in ranked if r['treatment_id']==baseline_id),None)
    if policy.baseline_preservation and baseline and ranked and ranked[0]['lower_confidence_utility']<baseline['lower_confidence_utility']:reasons.append('baseline_not_dominated')
    if reasons:return {'abstain':True,'decision':'abstain','selected_treatments':[skip_id],'fallback':'skip','reasons':sorted(set(reasons))}
    return {'abstain':False,'decision':'set_valued' if len(selection_set)>1 else 'single','selected_treatments':selection_set,'fallback':'none','reasons':[]}
