from __future__ import annotations
from .canonical import content_hash, stable_id

def claim_ledger(checkpoint_admitted:bool)->dict:
    claims=[
      ("closed_contracts",True,"schemas and validators"),
      ("deterministic_reference_pretraining",True,"golden replay"),
      ("learned_reference_representation",checkpoint_admitted,"synthetic reference checkpoint"),
      ("role_safe_corpus",True,"contamination and split audits"),
      ("outcome_supervision",False,"forbidden by phase boundary"),
      ("real_corpus_training",False,"no external corpus evidence"),
      ("distributed_training",False,"reference implementation only"),
      ("real_alpha",False,"not measured or claimed"),
      ("treatment_ranking",False,"forbidden authority"),
      ("treatment_selection",False,"forbidden authority"),
      ("runtime_parity",False,"not a runtime phase"),
      ("production_authorization",False,"requires later qualification"),
      ("live_trading",False,"forbidden authority"),
    ]
    payload={"phase":"SAED_V4_11","claims":[{"claim":a,"supported":b,"basis":c} for a,b,c in claims],"synthetic_reference_only":True}
    payload['ledger_id']=stable_id('claimledger',payload);payload['ledger_hash']=content_hash(payload);return payload
