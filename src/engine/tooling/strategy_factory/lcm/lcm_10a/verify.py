from __future__ import annotations
from pathlib import Path
from .canonical import digest_object, file_digest
from .constants import INVENTORY_ID, UPSTREAM_HANDOFF_DIGEST
from .errors import VerificationError
from .io import load_json, load_jsonl, nonempty_lines

REQUIRED=("input/upstream_binding.json","source/source_file_freeze.jsonl","source/source_freeze_summary.json","inventory/treatment_atom_registry.json","inventory/treatment_atom_registry.jsonl","execution/execution_capability_registry.json","execution/execution_capability_registry.jsonl","reachability/broker_api_reachability.json","reachability/broker_api_reachability.jsonl","authority/authority_boundary_map.json","risk/risk_assumption_registry.json","unknowns/execution_unknown_queue.json","bindings/setup_treatment_binding_inventory.json","security/security_restricted_execution_paths.json","reconciliation/lcm01_capability_reconciliation.json","plans/treatment_extraction_order.json","plans/execution_boundary_violation_registry.json","reports/portfolio_closure_report.json","reports/hostile_review.json","reports/acceptance_report.json","handoff/lcm10a_to_lcm10b_handoff.json","LCM10A_TO_LCM10B_HANDOFF.json","required_artifact_locator.json","treatment_inventory_marker.json","provenance/treatment_inventory_provenance_graph.json","events/treatment_inventory_event_ledger.json","output_manifest.json","treatment_inventory_receipt.json")

def verify_package(root: Path) -> dict:
    root=root.resolve()
    for rel in REQUIRED:
        if not (root/rel).is_file(): raise VerificationError('LCM10A_REQUIRED_ARTIFACT_MISSING:'+rel)
    manifest=load_json(root/'output_manifest.json')
    for row in manifest['files']:
        p=root/row['path']
        if not p.is_file() or p.stat().st_size!=row['size_bytes'] or file_digest(p)!=row['sha256']: raise VerificationError('LCM10A_MANIFEST_MISMATCH:'+row['path'])
    binding=load_json(root/'input/upstream_binding.json'); acceptance=load_json(root/'reports/acceptance_report.json'); closure=load_json(root/'reports/portfolio_closure_report.json'); handoff=load_json(root/'handoff/lcm10a_to_lcm10b_handoff.json'); receipt=load_json(root/'treatment_inventory_receipt.json')
    atoms=load_json(root/'inventory/treatment_atom_registry.json'); caps=load_json(root/'execution/execution_capability_registry.json'); reaches=load_json(root/'reachability/broker_api_reachability.json'); unknowns=load_json(root/'unknowns/execution_unknown_queue.json'); setup=load_json(root/'bindings/setup_treatment_binding_inventory.json')
    if binding['lcm09b_handoff_digest']!=UPSTREAM_HANDOFF_DIGEST: raise VerificationError('LCM10A_UPSTREAM_DIGEST_MISMATCH')
    if setup['record_count']!=60: raise VerificationError('LCM10A_SETUP_BINDING_COUNT_MISMATCH')
    if reaches['record_count']<=0 or caps['record_count']<=0 or atoms['record_count']<=0: raise VerificationError('LCM10A_EMPTY_CORE_REGISTRY')
    if not acceptance['acceptance_gate_passed'] or not closure['all_setup_dependencies_accounted']: raise VerificationError('LCM10A_ACCEPTANCE_NOT_CLOSED')
    for field in ('consumer_cutover_allowed','source_move_allowed','source_delete_allowed','promotion_authority_created','runtime_authority_created','live_order_authority_created','capital_authority_created'):
        if handoff.get(field): raise VerificationError('LCM10A_AUTHORITY_EXPANSION:'+field)
    if digest_object(handoff,'handoff_digest')!=handoff['handoff_digest']: raise VerificationError('LCM10A_HANDOFF_DIGEST_INVALID')
    if digest_object(receipt,'receipt_digest')!=receipt['receipt_digest']: raise VerificationError('LCM10A_RECEIPT_DIGEST_INVALID')
    if receipt['output_manifest_digest']!=manifest['manifest_digest']: raise VerificationError('LCM10A_RECEIPT_MANIFEST_CHAIN_INVALID')
    if (root/'LCM10A_TO_LCM10B_HANDOFF.json').read_bytes()!=(root/'handoff/lcm10a_to_lcm10b_handoff.json').read_bytes(): raise VerificationError('LCM10A_NAMED_HANDOFF_NOT_IDENTICAL')
    return {"passed":True,"inventory_id":INVENTORY_ID,"manifest_file_count":manifest['file_count'],"manifest_total_bytes":manifest['total_size_bytes'],"source_file_count":closure['counts']['scanned_source_file_count'],"treatment_atom_count":atoms['record_count'],"execution_capability_count":caps['record_count'],"broker_reachability_record_count":reaches['record_count'],"unknown_count":unknowns['record_count'],"setup_binding_count":setup['record_count']}

def verify_installation(repo_root: Path, inventory_root: Path, patch_index: Path) -> dict:
    paths=nonempty_lines(patch_index)
    missing=[rel for rel in paths if not (repo_root/rel).exists()]
    if missing: raise VerificationError('LCM10A_PATCH_INDEX_MISSING:'+str(missing[:10]))
    legacy_mutations=[rel for rel in paths if rel.startswith(('mql5/','lab/10_infrastructure/','src/engine/packages/','research/'))]
    if legacy_mutations: raise VerificationError('LCM10A_LEGACY_SOURCE_MUTATION_IN_PATCH:'+str(legacy_mutations[:10]))
    return {**verify_package(inventory_root),"patch_index_count":len(paths),"installation_passed":True}
