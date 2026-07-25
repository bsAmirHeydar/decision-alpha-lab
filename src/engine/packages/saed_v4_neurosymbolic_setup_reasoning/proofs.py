from __future__ import annotations
from .canonical import content_hash,stable_id
from .errors import ProofError

def build(subject_id,decision_time,projection,trace,facts,upstream_hash,ontology_hash,rule_library_hash):
    evidence_facts=sorted([{'fact_id':f['fact_id'],'fact_hash':f.get('fact_hash',content_hash(f))} for f in facts if f['subject_id']==subject_id],key=lambda x:x['fact_id'])
    fired=sorted({x['rule_id'] for x in trace if x['subject_id']==subject_id and x['matched']})
    body={'phase':'SAED_V4_19','subject_id':subject_id,'decision_time':decision_time,'directive':projection['directive'],'treatment_id':projection['treatment_id'],'reason':projection['reason'],'fact_evidence':evidence_facts,'fired_rule_ids':fired,'upstream_hash':upstream_hash,'ontology_hash':ontology_hash,'rule_library_hash':rule_library_hash,'projection_hash':projection['projection_hash'],'research_only':True,'runtime_executable':False,'execution_authority':False}
    if not evidence_facts:raise ProofError('proof has no facts')
    body['proof_id']=stable_id('proof',body);body['proof_hash']=content_hash(body);return body
def verify(proof):
    expected=content_hash({k:v for k,v in proof.items() if k!='proof_hash'});return expected==proof['proof_hash'] and proof['research_only'] and not proof['runtime_executable'] and not proof['execution_authority']
