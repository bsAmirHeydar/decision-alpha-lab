from __future__ import annotations
from pathlib import Path
from .io import load_json,load_jsonl
PACKAGE_REL="registry/legacy_context_migration/setup_contract_freezes/SETUPFREEZE_8638449DF9A774634FE9B8F9E17EF891"
def load_reference_freeze(repo:Path)->dict:
    root=repo/PACKAGE_REL
    return {"root":root,"marker":load_json(root/"setup_freeze_marker.json"),"inventory":load_jsonl(root/"inventory/setup_inventory.jsonl"),"embedded":load_jsonl(root/"embedded/embedded_setup_registry.jsonl"),"families":load_json(root/"families/setup_family_registry.json"),"variants":load_jsonl(root/"variants/setup_variant_registry.jsonl"),"context_bindings":load_jsonl(root/"bindings/setup_context_binding_registry.jsonl"),"unknowns":load_jsonl(root/"unknowns/setup_unknown_queue.jsonl"),"summary":load_json(root/"reports/setup_portfolio_summary.json"),"acceptance":load_json(root/"reports/acceptance_report.json"),"handoff":load_json(root/"handoff/lcm09a_to_lcm09b_handoff.json")}
