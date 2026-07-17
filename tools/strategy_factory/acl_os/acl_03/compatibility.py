from __future__ import annotations
from typing import Any
from .canonical import digest_object
from .types import Finding,Severity

SUPPORTED_CONTEXT_SCHEMA_MAJOR=1
SUPPORTED_COMPILER_MAJOR=1

def _major(value:str)->int:
    try:return int(str(value).split('.',1)[0])
    except Exception:return -1

def validate_compatibility(package:dict[str,Any],compiler_version:str)->dict[str,Any]:
    findings=[]; schema_version=package['manifest'].get('schema_version','')
    if _major(schema_version)!=SUPPORTED_CONTEXT_SCHEMA_MAJOR:
        findings.append(Finding('ACL03_CONTEXT_SCHEMA_INCOMPATIBLE',Severity.BLOCKER,'manifest.schema_version','Context schema major version is not supported','migrate the Context package through an approved migration',{'schema_version':schema_version}).to_dict())
    if _major(compiler_version)!=SUPPORTED_COMPILER_MAJOR:
        findings.append(Finding('ACL03_COMPILER_VERSION_INCOMPATIBLE',Severity.BLOCKER,'compiler_version','compiler major version is not supported','use a compatible compiler or migration',{'compiler_version':compiler_version}).to_dict())
    body={'schema_version':'1.0.0','context_id':package['manifest']['context_id'],'context_schema_version':schema_version,'compiler_version':compiler_version,'compatible':not findings,'requirements':[{'component':'acl_00','minimum_version':'1.0.0'},{'component':'acl_01','minimum_version':'1.0.0'},{'component':'acl_02','minimum_version':'1.0.0'}],'reason_codes':[x['code'] for x in findings]}
    return {**body,'findings':findings,'compatibility_digest':digest_object(body)}
