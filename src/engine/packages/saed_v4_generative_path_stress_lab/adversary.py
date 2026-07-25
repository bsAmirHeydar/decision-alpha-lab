from __future__ import annotations
from .stress import apply_stress
from .exploitability import _utility
from .canonical import content_hash

def search(base_paths,policy_doc,stress_contract,ledger=None):
    families=list(stress_contract['families']);levels=list(stress_contract['severity_levels']);candidate=policy_doc['candidate'];baseline=policy_doc['baseline'];trials=[]
    for step,(family,sev) in enumerate([(f,s) for f in families for s in levels][:int(stress_contract['adversarial_search_steps'])]):
        losses=[]
        for i,p in enumerate(base_paths[:3]):
            q=apply_stress(p,family,sev,i);losses.append((_utility(q,candidate)-_utility(q,baseline))*-1)
        score=sum(losses)/len(losses) if losses else 0.0;trials.append({'step':step+1,'family':family,'severity':float(sev),'candidate_relative_loss':score})
        if ledger:ledger.consume('adversarial_steps',1)
    worst=max(trials,key=lambda x:(x['candidate_relative_loss'],x['family'],x['severity'])) if trials else {'step':0,'family':'none','severity':0.0,'candidate_relative_loss':0.0}
    out={'trial_count':len(trials),'trials':trials,'worst_case':worst,'failure_found':worst['candidate_relative_loss']>0.0,'research_only':True};out['adversarial_failure_packet_hash']=content_hash(out);return out
