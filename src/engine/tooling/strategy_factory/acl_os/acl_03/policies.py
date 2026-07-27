from __future__ import annotations
from pathlib import Path
from ..common import PATHS
from .io import load_yaml
POLICY_ROOT=PATHS.acl_registry_root/"acl_03"/"policies"/"v1"
SCHEMA_ROOT=PATHS.acl_registry_root/"acl_03"/"schemas"/"v1"
def load_policy(name:str)->dict: return load_yaml(POLICY_ROOT/f"{name}.yaml")
