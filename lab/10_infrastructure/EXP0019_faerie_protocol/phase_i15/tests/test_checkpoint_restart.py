from dataclasses import replace
from fp_i15_paper import *
def test_checkpoint_accepts(buy_plan,buy_quote):
 p=paper_policy(PaperPolicyProfile.FILLED);r=simulate(buy_plan,p,PaperScenario.IMMEDIATE_FILL,buy_quote,buy_plan.created_utc_ms);cp=create_checkpoint(buy_plan.risk_config_hash,p,r.ledger,(r.quota,),(r.order,),r.fills,(r.position,));assert validate_checkpoint(cp,buy_plan.risk_config_hash,p).disposition==CheckpointDisposition.ACCEPTED
def test_checkpoint_config_rejects(buy_plan,buy_quote):
 p=paper_policy(PaperPolicyProfile.FILLED);r=simulate(buy_plan,p,PaperScenario.IMMEDIATE_FILL,buy_quote,buy_plan.created_utc_ms);cp=create_checkpoint(buy_plan.risk_config_hash,p,r.ledger);assert validate_checkpoint(cp,sha256('other'),p).disposition==CheckpointDisposition.REJECT_CONFIG
def test_checkpoint_hash_rejects(buy_plan,buy_quote):
 p=paper_policy(PaperPolicyProfile.FILLED);r=simulate(buy_plan,p,PaperScenario.IMMEDIATE_FILL,buy_quote,buy_plan.created_utc_ms);cp=create_checkpoint(buy_plan.risk_config_hash,p,r.ledger);cp=replace(cp,payload_hash=sha256('bad'));assert validate_checkpoint(cp,buy_plan.risk_config_hash,p).disposition==CheckpointDisposition.REJECT_HASH
def test_restore_chain(buy_plan,buy_quote):
 p=paper_policy(PaperPolicyProfile.FILLED);r=simulate(buy_plan,p,PaperScenario.IMMEDIATE_FILL,buy_quote,buy_plan.created_utc_ms);cp=create_checkpoint(buy_plan.risk_config_hash,p,r.ledger,(r.quota,),(r.order,),r.fills,(r.position,));v,s=restore_checkpoint(cp,buy_plan.risk_config_hash,p);assert v.disposition==CheckpointDisposition.ACCEPTED and s['ledger'].chain_head==r.ledger[-1].event_hash
