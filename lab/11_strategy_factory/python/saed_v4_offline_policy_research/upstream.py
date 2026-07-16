from __future__ import annotations
from .contracts import UpstreamIntakeContract
from .errors import UpstreamError
from .canonical import content_hash
REQUIRED={'generative_stress_certificate_hash':'GOLDEN_GENERATIVE_STRESS_CERTIFICATE','fidelity_report_hash':'GOLDEN_FIDELITY_REPORT','uncertainty_map_hash':'GOLDEN_UNCERTAINTY_MAP','exploitability_report_hash':'GOLDEN_EXPLOITABILITY_REPORT','budget_ledger_hash':'GOLDEN_BUDGET_SNAPSHOT','handoff_hash':'V4_22_TO_V4_23_HANDOFF'}
def verify(contract_doc,documents):
    c=UpstreamIntakeContract.from_mapping(contract_doc)
    if set(documents)!=set(REQUIRED.values()): raise UpstreamError('upstream document set mismatch')
    for field,name in REQUIRED.items():
        doc=documents[name];expected=getattr(c,field)
        actual=doc.get({'generative_stress_certificate_hash':'certificate_hash','fidelity_report_hash':'fidelity_report_hash','uncertainty_map_hash':'uncertainty_map_hash','exploitability_report_hash':'exploitability_report_hash','budget_ledger_hash':'ledger_hash','handoff_hash':'handoff_hash'}[field])
        if actual!=expected: raise UpstreamError(f'upstream hash mismatch: {name}')
    handoff=documents['V4_22_TO_V4_23_HANDOFF']
    if handoff.get('next_phase')!='SAED_V4_23' or not handoff.get('research_only') or any(handoff.get('authority',{}).values()): raise UpstreamError('unsafe upstream handoff')
    out={'phase':'SAED_V4_23','required_phase':c.required_phase,'verified':True,'document_hashes':{k:content_hash(v) for k,v in documents.items()},'intake_contract_hash':content_hash(contract_doc)}
    out['receipt_hash']=content_hash(out);return out
