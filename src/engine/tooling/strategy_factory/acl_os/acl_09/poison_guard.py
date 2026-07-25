from __future__ import annotations
from .canonical import with_digest
from .errors import PoisoningError
FORBIDDEN_TRUE_FIELDS={'promotion_allowed','live_order_submission_allowed','capital_activation_allowed','doctrine_amendment_allowed','semantic_interpretation_added'}
FORBIDDEN_TEXT=('AUTHORIZE_EXECUTION','ACTIVATE_CAPITAL','PROMOTE_NOW','IGNORE_POLICY','BYPASS_GATE')
def inspect_records(records:list[dict],report_id:str)->dict:
    findings=[]
    for record in records:
        for field in FORBIDDEN_TRUE_FIELDS:
            if record.get(field) is True: findings.append({'experience_id':record['experience_id'],'reason':'FORBIDDEN_TRUE_FIELD','field':field})
        text=str(record)
        for token in FORBIDDEN_TEXT:
            if token in text: findings.append({'experience_id':record['experience_id'],'reason':'FORBIDDEN_CONTROL_TOKEN','token':token})
        if record.get('experience_class')=='DIAGNOSTIC_EXCLUSION' and record.get('knowledge_polarity')!='NON_SELECTABLE_DIAGNOSTIC': findings.append({'experience_id':record['experience_id'],'reason':'DIAGNOSTIC_POLARITY_INVALID'})
    report=with_digest({'schema_version':'1.0.0','report_id':report_id,'record_count':len(records),'finding_count':len(findings),'findings':findings,'structured_fields_only':True,'arbitrary_narrative_execution_denied':True,'passed':not findings},'poisoning_report_digest')
    if findings: raise PoisoningError(str(findings))
    return report
