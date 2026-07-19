from __future__ import annotations
import json
from pathlib import Path
from .canonical import file_digest, digest_object
from .errors import VerificationError
from .io import load_json, load_jsonl

REQUIRED=[
"context_portfolio_marker.json","authority/authority_permit.json","input/lcm07_binding.json","portfolio/context_portfolio_registry.jsonl","portfolio/context_portfolio_registry.csv","risk/context_risk_assessment.jsonl","risk/context_risk_assessment.csv","dependencies/context_dependency_graph.json","waves/context_wave_assignment.json","pilot/pilot_candidate_evaluations.jsonl","pilot/pilot_selection_decision.json","unresolved/unresolved_context_queue.jsonl","reports/context_portfolio_summary.json","reports/hostile_review.json","reports/acceptance_report.json","handoff/lcm08a_to_lcm08b_handoff.json","events/context_portfolio_event_ledger.json","provenance/context_portfolio_provenance_graph.json","output_manifest.json","context_portfolio_receipt.json"]


def verify_package(root: Path) -> dict:
    root=root.resolve()
    for rel in REQUIRED:
        if not (root/rel).is_file(): raise VerificationError(f"missing package artifact: {rel}")
    manifest=load_json(root/'output_manifest.json')
    for row in manifest['files']:
        path=root/row['path']
        if not path.is_file(): raise VerificationError(f"manifest path missing: {row['path']}")
        if path.stat().st_size!=row['size_bytes']: raise VerificationError(f"size mismatch: {row['path']}")
        if file_digest(path)!=row['sha256']: raise VerificationError(f"digest mismatch: {row['path']}")
    records=load_jsonl(root/'portfolio/context_portfolio_registry.jsonl')
    evaluations=load_jsonl(root/'pilot/pilot_candidate_evaluations.jsonl')
    selected=[e for e in evaluations if e.get('selected')]
    summary=load_json(root/'reports/context_portfolio_summary.json')
    hostile=load_json(root/'reports/hostile_review.json')
    acceptance=load_json(root/'reports/acceptance_report.json')
    handoff=load_json(root/'handoff/lcm08a_to_lcm08b_handoff.json')
    if len(records)!=summary['context_candidate_count']:raise VerificationError('portfolio count mismatch')
    if len(selected)!=1:raise VerificationError('exactly one selected pilot required')
    if selected[0]['identity_id']!=summary['selected_pilot_identity_id']:raise VerificationError('selected pilot mismatch')
    if not hostile['hostile_review_passed']:raise VerificationError('hostile review failed')
    if not acceptance['acceptance_gate_passed']:raise VerificationError('acceptance failed')
    if handoff.get('source_move_allowed') or handoff.get('source_delete_allowed'):raise VerificationError('handoff authority expansion')
    if any(load_json(root/p).get('runtime_authority_created') for p in ['context_portfolio_marker.json','reports/context_portfolio_summary.json','reports/acceptance_report.json','handoff/lcm08a_to_lcm08b_handoff.json']):raise VerificationError('runtime authority created')
    return {"passed":True,"portfolio_id":summary['portfolio_id'],"context_candidate_count":len(records),"selected_pilot_identity_id":selected[0]['identity_id'],"manifest_file_count":manifest['file_count']}


def verify_installation(repo_root: Path, package_root: Path, patch_index: Path) -> dict:
    repo_root=repo_root.resolve(); package_root=package_root.resolve()
    lines=[x.strip() for x in patch_index.read_text(encoding='utf-8').splitlines() if x.strip()]
    missing=[x for x in lines if not (repo_root/x).exists()]
    if missing:raise VerificationError(f"patch index missing paths: {missing[:10]}")
    return {**verify_package(package_root),"patch_index_count":len(lines),"installation_passed":True}
