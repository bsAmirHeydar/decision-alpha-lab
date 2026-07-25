from __future__ import annotations
from .canonical import content_hash,stable_id

def receipt(upstream,dataset,registry,claim_report,ledger):
    out={'phase':'SAED_V4_17','receipt_id':stable_id('v417integrity',{'dataset':dataset['dataset_hash'],'registry':registry['registry_hash']}),'upstream_v4_16_handoff_hash':upstream['v4_16_handoff_hash'],'dataset_hash':dataset['dataset_hash'],'checkpoint_registry_hash':registry['registry_hash'],'claim_report_hash':claim_report['report_hash'],'compute_exposure_ledger_hash':ledger['ledger_hash'],'protected_evidence_exposures':0,'hidden_evaluation_queries':0,'deterministic':True,'synthetic_only':True,'causal_claim_authority':False,'production_eligible':False};out['receipt_hash']=content_hash(out);return out
