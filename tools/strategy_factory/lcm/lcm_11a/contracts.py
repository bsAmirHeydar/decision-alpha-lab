from __future__ import annotations
from pathlib import Path
from .anchors import build_anchor_contract
from .lifecycle import build_lifecycle_contract
from .namespace import build_namespace_contract
from .models import VisualSite

def build_contracts(repo_root: Path, sites: list[VisualSite], delete_sites: list[dict]):
    namespaces=[build_namespace_contract(site) for site in sites]
    anchors=[build_anchor_contract(site) for site in sites]
    lifecycles=[build_lifecycle_contract(repo_root,site,delete_sites) for site in sites]
    return namespaces,anchors,lifecycles
