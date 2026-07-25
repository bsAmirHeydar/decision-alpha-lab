from __future__ import annotations
from dataclasses import asdict
from .golden import *
from .graph import compile_graph
from .engine import execute_policy
from .canonical import canonical_sha256

def generate_vectors():
    a=golden_admission();m=golden_manual();o=golden_occurrence();mo=golden_output();f=golden_fallback();au=golden_authority();g=golden_hybrid_graph(a,m,f,au);c=compile_graph(g,a);d=execute_policy(c,o,m,f,au,admission=a,model_output=mo)
    payload={'version':'1.0.0','manual_policy_hash':m.policy_hash,'admission_hash':a.admission_hash,'occurrence_hash':o.occurrence_hash,'model_output_hash':mo.output_hash,'graph_hash':g.graph_hash,'decision_hash':d.decision_hash,'status':d.status.value,'action':d.action.value,'treatment':d.treatment,'risk_tier':d.risk_tier}
    return {**payload,'vector_hash':canonical_sha256(payload)}
def verify_vectors(v):
    body={k:v[k] for k in v if k!='vector_hash'}
    return v.get('version')=='1.0.0' and v.get('vector_hash')==canonical_sha256(body) and v==generate_vectors()
