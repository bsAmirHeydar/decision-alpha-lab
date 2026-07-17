from __future__ import annotations
import re
from pathlib import Path
from typing import Any
from .canonical import digest_object
from .types import Finding,Severity

SECRET_PATTERNS=(re.compile(r'AKIA[0-9A-Z]{16}'),re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),re.compile(r'(?i)(?:password|secret|api[_-]?key)\s*[:=]\s*["\'][^"\']{8,}["\']'))
FORBIDDEN_GUARD_TOKENS=('eval(','exec(','__import__','OrderSend(','CTrade','subprocess','socket.','requests.')

def evaluate_security_boundary(context_root:Path,package:dict[str,Any],detector_ir:dict[str,Any],adapters:list[dict[str,Any]])->dict[str,Any]:
    findings=[]
    for p in context_root.rglob('*'):
        if p.is_symlink(): findings.append(Finding('ACL03_SYMLINK_REJECTED',Severity.BLOCKER,str(p.relative_to(context_root)),'symlink detected in Context source','replace it with an immutable regular file').to_dict())
        if p.is_file() and p.stat().st_size<=2_000_000:
            text=p.read_text(encoding='utf-8',errors='ignore')
            for pat in SECRET_PATTERNS:
                if pat.search(text): findings.append(Finding('ACL03_SECRET_MATERIAL_DETECTED',Severity.BLOCKER,str(p.relative_to(context_root)),'possible secret material detected in Context source','remove the secret and rotate it').to_dict())
    for t in detector_ir.get('transitions',[]):
        for token in FORBIDDEN_GUARD_TOKENS:
            if token in t.get('guard_dsl',''): findings.append(Finding('ACL03_DYNAMIC_EXECUTION_DETECTED',Severity.BLOCKER,'detector_ir.transitions.guard_dsl','forbidden executable token appears in guard DSL','rewrite declaratively',{'token':token}).to_dict())
    for a in adapters:
        caps=a['capabilities']
        if caps.get('order_submission') or caps.get('capital_access'): findings.append(Finding('ACL03_ADAPTER_AUTHORITY_ESCALATION',Severity.BLOCKER,a['adapter_id'],'adapter contract requests trading authority','remove order and capital capabilities').to_dict())
    body={'schema_version':'1.0.0','context_id':package['manifest']['context_id'],'passed':not findings,'finding_count':len(findings),'controls':{'source_symlink_reject':True,'secret_scan':True,'dynamic_execution_reject':True,'adapter_least_privilege':True,'network_access_during_compile':False,'source_write_during_compile':False},'findings':findings,'claim_ceiling':'REFERENCE_SECURITY_CONTROLS_ONLY'}
    return {**body,'security_report_digest':digest_object(body)}
