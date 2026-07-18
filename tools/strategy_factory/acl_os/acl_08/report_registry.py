from __future__ import annotations
from .canonical import with_digest
from .errors import PolicyError
BLOCKS=[
 ('IDENTITY',1),('EXECUTIVE_FINDINGS',2),('DECISION_DISTRIBUTION',3),('CANDIDATE_EVIDENCE',4),('GATE_EVIDENCE',5),('BASELINE_CONTEXT',6),('DIAGNOSTIC_ISOLATION',7),('UNCERTAINTY_AND_UNKNOWN',8),('NEGATIVE_KNOWLEDGE',9),('LIMITATIONS',10),('PROVENANCE',11),('SECURITY_AND_AUTHORITY',12),('NEXT_ALLOWED_ACTIONS',13)
]
def registry_snapshot()->dict:
    return with_digest({'schema_version':'1.0.0','registry_id':'ACL08_REPORT_BLOCK_REGISTRY_V1','closed_world':True,'entries':[{'block_id':x,'order':n,'required':True,'closed_world':True} for x,n in BLOCKS]},'registry_digest')
def validate_registry(doc:dict)->dict:
    expected=registry_snapshot()
    if doc!=expected: raise PolicyError('report block registry is not canonical')
    return doc
def block_order(doc:dict)->list[str]: return [x['block_id'] for x in sorted(doc['entries'],key=lambda r:r['order'])]
