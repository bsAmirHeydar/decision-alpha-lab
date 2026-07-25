from __future__ import annotations
from statistics import mean
from .canonical import with_digest
def _q(vals:list[float],p:float)->float:
    if not vals:return 0.0
    s=sorted(vals); idx=min(len(s)-1,max(0,int((len(s)-1)*p))); return s[idx]
def build_baselines(slice_doc:dict,max_trials:int)->dict:
    rows=slice_doc['rows']; n=len(rows); mask=[1 if r['context_present'] else 0 for r in rows]; outcomes=[float(r['forward_delta']) for r in rows]; support=sum(mask)
    conditioned=[outcomes[i] for i,m in enumerate(mask) if m]
    shifts=[]; excluded_identity_equivalent_shifts=[]
    for shift in range(1,min(n,max_trials+1)):
        shifted_mask=[mask[(i-shift)%n] for i in range(n)]
        if shifted_mask==mask:
            excluded_identity_equivalent_shifts.append(shift)
            continue
        vals=[outcomes[i] for i,m in enumerate(shifted_mask) if m]
        shifts.append(mean(vals) if vals else 0.0)
    conditioned_mean=mean(conditioned) if conditioned else 0.0; all_mean=mean(outcomes) if outcomes else 0.0
    random_mean=mean(shifts) if shifts else 0.0; random_p90=_q(shifts,0.90); random_max=max(shifts) if shifts else 0.0
    body={'schema_version':'1.0.0','method':'DETERMINISTIC_CIRCULAR_MASK_SHIFT_EXCLUDING_IDENTITY_EQUIVALENT_MASKS','trial_count':len(shifts),'excluded_identity_equivalent_shift_count':len(excluded_identity_equivalent_shifts),'excluded_identity_equivalent_shifts':excluded_identity_equivalent_shifts,'support_per_trial':support,'conditioned_mean':conditioned_mean,'always_participate_mean':all_mean,'never_participate_mean':0.0,'random_mean':random_mean,'random_p90':random_p90,'random_max':random_max,'conditioned_minus_random_mean':conditioned_mean-random_mean,'conditioned_exceeds_random_p90':conditioned_mean>random_p90,'descriptive_only':True,'statistical_validation_claimed':False,'trial_means':shifts}
    return with_digest(body,'baseline_report_digest')
