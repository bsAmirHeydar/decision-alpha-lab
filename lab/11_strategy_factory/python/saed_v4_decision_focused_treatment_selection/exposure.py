from __future__ import annotations
from .canonical import content_hash

def build_exposure_ledger(budget_snapshot,trial_ids):
    rows=[{'trial_id':x,'exposure_class':'synthetic_reference','protected':False,'hidden_evaluation_queries':0} for x in sorted(set(trial_ids))]
    out={'phase':'SAED_V4_20','complete':True,'rows':rows,'budget_snapshot':budget_snapshot,'protected_evidence_exposure':0,'hidden_evaluation_queries':0,'ledger_hash':''}
    out['ledger_hash']=content_hash({k:v for k,v in out.items() if k!='ledger_hash'})
    return out
