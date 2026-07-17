from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml
from ..common import REPO_ROOT
from .canonical import digest_object
from .errors import PolicyError

CATALOG_ROOT=REPO_ROOT/"registry"/"acl_os"/"acl_00"/"policies"/"v1"

@dataclass(frozen=True, slots=True)
class PolicyBundle:
    documents: dict[str,dict[str,Any]]
    digest: str

    @classmethod
    def load(cls,root:Path=CATALOG_ROOT)->"PolicyBundle":
        docs={}
        for path in sorted(root.glob("*.yaml")):
            obj=yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(obj,dict): raise PolicyError(f"{path} is not a mapping")
            docs[path.stem]=obj
        required={"lifecycle_transitions","authority_roles","separation_of_duties","evidence_requirements","approval_policy","security_hook_policy","waiver_policy","claim_ceiling_bindings","reason_codes","action_catalog"}
        missing=required-set(docs)
        if missing: raise PolicyError(f"missing policy documents: {sorted(missing)}")
        return cls(docs,digest_object(docs))

    def transition(self,from_state:str,to_state:str)->dict[str,Any]|None:
        key=f"{from_state}->{to_state}"
        return self.documents["lifecycle_transitions"]["transitions"].get(key)

    def role(self,role_id:str)->dict[str,Any]|None:
        return self.documents["authority_roles"]["roles"].get(role_id)

    def reason(self,code:str)->str:
        return self.documents["reason_codes"]["reasons"].get(code,code)
