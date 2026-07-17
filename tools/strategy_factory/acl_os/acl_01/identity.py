from __future__ import annotations
import re
from .errors import IdentityError

_COMPONENT=re.compile(r"^[a-z][a-z0-9]*(?:[-_][a-z0-9]+)*$")
_DIGEST=re.compile(r"^sha256:[0-9a-f]{64}$")
_ARTIFACT=re.compile(r"^al://([^/]+)/([^/]+)/([^/]+)/([^@]+)@(.+)$")


def validate_component(value:str,label:str="component"):
    if not isinstance(value,str) or not _COMPONENT.fullmatch(value):
        raise IdentityError(f"invalid {label}: {value!r}")
    if len(value)>96: raise IdentityError(f"{label} exceeds 96 characters")


def validate_digest(value:str):
    if not _DIGEST.fullmatch(value): raise IdentityError(f"invalid sha256 digest: {value!r}")


def build_artifact_id(tenant_id:str,namespace:str,kind:str,name:str,version:str)->str:
    for label,value in (("tenant_id",tenant_id),("namespace",namespace),("kind",kind),("name",name)):
        validate_component(value,label)
    from .semver import Version
    Version.parse(version)
    return f"al://{tenant_id}/{namespace}/{kind}/{name}@{version}"


def validate_artifact_id(identity):
    expected=build_artifact_id(identity.tenant_id,identity.namespace,identity.kind,identity.name,identity.version)
    if identity.artifact_id!=expected: raise IdentityError(f"artifact_id mismatch: expected {expected}")


def parse_artifact_id(value:str)->dict[str,str]:
    m=_ARTIFACT.fullmatch(value)
    if not m: raise IdentityError(f"invalid artifact id: {value}")
    tenant,namespace,kind,name,version=m.groups()
    expected=build_artifact_id(tenant,namespace,kind,name,version)
    if expected!=value: raise IdentityError("artifact id is not canonical")
    return {"tenant_id":tenant,"namespace":namespace,"kind":kind,"name":name,"version":version,"base_id":f"al://{tenant}/{namespace}/{kind}/{name}"}


def artifact_base(value:str)->str:
    return parse_artifact_id(value)["base_id"]
