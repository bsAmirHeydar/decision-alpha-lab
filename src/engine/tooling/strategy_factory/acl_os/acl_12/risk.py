from __future__ import annotations
from .canonical import stable_id,with_digest
def build_risk_register(threat_assessment:dict)->dict:
    risks=[]
    for item in threat_assessment['results']:
        state='OPEN' if item['residual_state']=='OPEN_PRODUCTION_EVIDENCE_GAP' else 'CONTROLLED_REFERENCE_ONLY'
        risks.append(with_digest({'schema_version':'1.0.0','risk_id':stable_id('SECRISK',item['threat_id']),'threat_id':item['threat_id'],'inherent_severity':item['inherent_severity'],'residual_state':state,'mapped_controls':item['mapped_controls'],'risk_acceptance_allowed':False,'owner_role':'SECURITY_OWNER','next_action':'COLLECT_PRODUCTION_EVIDENCE' if state=='OPEN' else 'PRESERVE_CONTROL_EVIDENCE'},'risk_digest'))
    return with_digest({'schema_version':'1.0.0','register_id':'ACL12_SECURITY_RISK_REGISTER_V1','risk_count':len(risks),'open_risk_count':sum(1 for r in risks if r['residual_state']=='OPEN'),'risks':risks,'automatic_risk_acceptance_allowed':False},'register_digest')
