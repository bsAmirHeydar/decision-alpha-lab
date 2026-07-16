from __future__ import annotations
from .errors import ActionMaskError
from .treatment_universe import treatment_by_id
from .canonical import content_hash

def compile_action_mask(context,universe,constraints,proofs):
    proof_map={p['treatment_id']:p for p in proofs}
    rows=[]
    for tid in universe['enabled_treatments']:
        t=treatment_by_id(universe,tid);reasons=[]
        if int(context['support'].get(tid,0))<constraints.minimum_support:reasons.append('insufficient_support')
        if float(context['overlap'].get(tid,0.0))<constraints.minimum_overlap:reasons.append('positivity_or_overlap_failure')
        if float(context['estimated_cost'].get(tid,0.0))>constraints.maximum_cost:reasons.append('cost_limit')
        if int(t['complexity'])>constraints.maximum_complexity:reasons.append('complexity_limit')
        if constraints.manual_approval_required and not bool(t['manual_approved']):reasons.append('manual_approval_missing')
        p=proof_map.get(tid)
        if constraints.proof_required and (not p or not p.get('valid') or p.get('proof_hash')!=context['proof_hashes'].get(tid)):reasons.append('proof_missing_or_mismatched')
        allowed=not reasons
        rows.append({'treatment_id':tid,'allowed':allowed,'reasons':reasons})
    if not any(r['allowed'] for r in rows):
        skip=universe['skip_treatment']
        for r in rows:
            if r['treatment_id']==skip:r['allowed']=True;r['reasons']=['fail_closed_skip_override']
    out={'context_id':context['context_id'],'rows':rows,'hard_fail_to_skip':constraints.hard_fail_to_skip,'mask_hash':''}
    out['mask_hash']=content_hash({k:v for k,v in out.items() if k!='mask_hash'})
    return out

def assert_mask_integrity(mask,universe):
    ids=[r['treatment_id'] for r in mask['rows']]
    if ids!=list(universe['enabled_treatments']):raise ActionMaskError('mask universe mismatch')
    if not any(r['allowed'] for r in mask['rows']):raise ActionMaskError('empty action mask')
    return True
