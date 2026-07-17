from __future__ import annotations
from pathlib import Path
from ..common import REPO_ROOT
from .io import load_yaml

POLICY_ROOT = REPO_ROOT / "registry" / "acl_os" / "acl_04" / "policies" / "v1"
SCHEMA_ROOT = REPO_ROOT / "registry" / "acl_os" / "acl_04" / "schemas" / "v1"


def load_policy(name: str) -> dict:
    return load_yaml(POLICY_ROOT / f"{name}.yaml")
