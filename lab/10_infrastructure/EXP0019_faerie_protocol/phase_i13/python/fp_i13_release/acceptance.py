from .contracts import *
from .canonical import sha256,stable_id

def gate(gate_id,status,reason_codes,evidence_hash): return GateResult(gate_id,status,tuple(sorted(set(reason_codes))),evidence_hash)
def build_acceptance(manifest:ReleaseManifest,gates:tuple[GateResult,...])->AcceptanceReport:
    failed=tuple(g.gate_id for g in gates if g.status==GateStatus.FAIL)
    pending=tuple(g.gate_id for g in gates if g.status in (GateStatus.PENDING,GateStatus.NOT_AVAILABLE))
    if failed: status=AcceptanceStatus.REJECTED;ready=False
    elif pending: status=AcceptanceStatus.SOURCE_ACCEPTED_EXTERNAL_COMPILE_PENDING;ready=False
    else: status=AcceptanceStatus.ACCEPTED;ready=True
    body={'manifest':manifest.manifest_id,'gates':tuple((g.gate_id,g.status.value,g.evidence_hash) for g in gates),'status':status.value,'pending':pending}
    return AcceptanceReport(stable_id('FPACCEPT',body),status,gates,manifest.manifest_id,ready,pending,sha256(body))
