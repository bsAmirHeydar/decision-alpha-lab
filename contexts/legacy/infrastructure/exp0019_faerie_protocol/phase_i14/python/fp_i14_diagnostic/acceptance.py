from .contracts import *
from .canonical import sha256,stable_id

def gate(gate_id,status,reason_codes,evidence_hash): return AcceptanceGate(gate_id,status,tuple(sorted(set(reason_codes))),evidence_hash)
def build_acceptance(gates):
    external={'METAEDITOR_COMPILE','LOCAL_TERMINAL_DIFFERENTIAL_RUNTIME'}
    hard=[g for g in gates if g.gate_id not in external]
    source=all(g.status==GateStatus.PASS for g in hard)
    pending=tuple(g.gate_id for g in gates if g.status==GateStatus.PENDING)
    ready=source and not pending and all(g.status==GateStatus.PASS for g in gates)
    status=GateStatus.FAIL if any(g.status==GateStatus.FAIL for g in hard) else (GateStatus.PASS if ready else (GateStatus.PENDING if source else GateStatus.BLOCKED))
    aid=stable_id('FPDACC',{'gates':[(g.gate_id,g.status.value,g.evidence_hash) for g in gates]})
    return DiagnosticAcceptance(aid,status,tuple(gates),source,ready,pending,sha256({'acceptance_id':aid,'status':status.value,'source':source,'ready':ready,'pending':pending}))
