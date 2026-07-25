from __future__ import annotations
from typing import Any
from .canonical import digest_object
from .types import Finding,Severity

ALLOWED_KINDS={'DOMAIN_LINTER','DATA_ADAPTER','CALENDAR_ADAPTER','FEATURE_VIEW_ADAPTER','GOLDEN_CASE_PROVIDER'}
FORBIDDEN_CAPABILITIES={'ORDER_SUBMISSION','CAPITAL_ACCESS','UNBOUNDED_NETWORK','UNBOUNDED_FILESYSTEM','DYNAMIC_CODE_EXECUTION','AUTHORITY_ESCALATION'}

def resolve_extensions(package:dict[str,Any])->dict[str,Any]:
    findings=[];resolved=[];seen=set()
    for ext in package['manifest'].get('extensions',[]):
        if not isinstance(ext,dict):
            findings.append(Finding('ACL03_EXTENSION_MANIFEST_INVALID',Severity.BLOCKER,'manifest.extensions','extension entry must be a mapping','use a registered extension manifest').to_dict());continue
        eid=ext.get('extension_id');kind=ext.get('extension_kind');caps=set(ext.get('capabilities',[]))
        if not eid or eid in seen: findings.append(Finding('ACL03_EXTENSION_ID_INVALID',Severity.BLOCKER,'manifest.extensions','extension id is missing or duplicated','use a unique registered extension_id',{'extension_id':eid}).to_dict())
        seen.add(eid)
        if kind not in ALLOWED_KINDS: findings.append(Finding('ACL03_EXTENSION_KIND_FORBIDDEN',Severity.BLOCKER,'manifest.extensions','extension kind is not permitted in ACL-03','use an allowed extension kind',{'extension_kind':kind}).to_dict())
        bad=sorted(caps&FORBIDDEN_CAPABILITIES)
        if bad: findings.append(Finding('ACL03_EXTENSION_CAPABILITY_FORBIDDEN',Severity.BLOCKER,'manifest.extensions','extension requests forbidden capabilities','remove forbidden capabilities',{'capabilities':bad}).to_dict())
        if ext.get('public_ports_only') is not True: findings.append(Finding('ACL03_EXTENSION_PRIVATE_IMPORT_FORBIDDEN',Severity.BLOCKER,'manifest.extensions','extension is not restricted to public ports','declare public_ports_only=true').to_dict())
        resolved.append({'extension_id':eid,'extension_kind':kind,'capabilities':sorted(caps),'public_ports_only':bool(ext.get('public_ports_only')),'status':'RESOLVED' if not bad and kind in ALLOWED_KINDS else 'REJECTED'})
    body={'schema_version':'1.0.0','context_id':package['manifest']['context_id'],'extensions':resolved,'extension_count':len(resolved),'passed':not findings}
    return {**body,'findings':findings,'resolution_digest':digest_object(body)}
