from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml
from .canonical import digest_object
from .errors import ContractError
from ..common import REPO_ROOT

POLICY_ROOT=REPO_ROOT/"registry"/"acl_os"/"acl_01"/"policies"/"v1"
REQUIRED=("artifact_kinds","repository_zones","path_templates","ownership_policy","version_policy","schema_registry_policy","plugin_registry_policy","dependency_policy","lineage_edge_types","compatibility_policy","migration_policy","locator_policy","generated_content_policy","reserved_namespaces","reason_codes")

@dataclass(frozen=True,slots=True)
class PolicyBundle:
    documents:dict[str,dict[str,Any]]
    digest:str

    @classmethod
    def load(cls,root:Path=POLICY_ROOT)->"PolicyBundle":
        docs={}
        for name in REQUIRED:
            p=root/f"{name}.yaml"
            if not p.is_file(): raise ContractError(f"missing ACL-01 policy: {p}")
            obj=yaml.safe_load(p.read_text(encoding="utf-8"))
            if not isinstance(obj,dict): raise ContractError(f"policy must be object: {p}")
            docs[name]=obj
        return cls(docs,digest_object(docs))
