from __future__ import annotations
from pathlib import Path
from typing import Any
from .artifact_manifest import verify_output_manifest
from .canonical import digest_file, digest_object, verify_embedded_digest, with_digest
from .errors import IntegrityError
from .io import load_json
from .policies import HANDOFF_IN, REQUIRED_UPSTREAM_ACTIONS, FORBIDDEN_UPSTREAM_ACTIONS

def _require(condition: bool, code: str) -> None:
    if not condition: raise IntegrityError(code)

def load_acl09_bundle(root: Path) -> dict[str, Any]:
    _require((root/'.acl09_generated_root').is_file(), 'ACL09_MARKER_MISSING')
    manifest = load_json(root/'output_manifest.json')
    receipt = load_json(root/'memory_receipt.json')
    handoff = load_json(root/'handoff/acl10_handoff.json')
    memory_run = load_json(root/'run/memory_run.json')
    memory_index = load_json(root/'memory/memory_index.json')
    admission_bundle = load_json(root/'memory/admission_bundle.json')
    portfolio = load_json(root/'planner/plan_portfolio.json')
    events = load_json(root/'events/memory_event_ledger.json')
    provenance = load_json(root/'lineage/memory_provenance_graph.json')
    security = load_json(root/'security/security_boundary_report.json')
    integrity = load_json(root/'reports/integrity_report.json')
    _require(verify_output_manifest(root, manifest), 'ACL09_MANIFEST_INVALID')
    for document, field, code in [
        (receipt,'receipt_digest','ACL09_RECEIPT_DIGEST_INVALID'),(handoff,'handoff_digest','ACL09_HANDOFF_DIGEST_INVALID'),
        (memory_run,'memory_run_digest','ACL09_MEMORY_RUN_DIGEST_INVALID'),(memory_index,'memory_index_digest','ACL09_MEMORY_INDEX_DIGEST_INVALID'),
        (admission_bundle,'admission_bundle_digest','ACL09_ADMISSION_BUNDLE_DIGEST_INVALID'),(portfolio,'portfolio_digest','ACL09_PORTFOLIO_DIGEST_INVALID'),
        (events,'ledger_digest','ACL09_EVENT_LEDGER_DIGEST_INVALID'),(provenance,'graph_digest','ACL09_PROVENANCE_DIGEST_INVALID'),
        (security,'security_report_digest','ACL09_SECURITY_DIGEST_INVALID'),(integrity,'integrity_report_digest','ACL09_INTEGRITY_DIGEST_INVALID')]:
        _require(verify_embedded_digest(document, field), code)
    _require(handoff.get('handoff_type') == HANDOFF_IN, 'ACL09_HANDOFF_TYPE_INVALID')
    _require(set(handoff.get('required_acl10_actions',[])) == REQUIRED_UPSTREAM_ACTIONS, 'ACL09_REQUIRED_ACTIONS_INVALID')
    _require(set(handoff.get('forbidden_acl10_actions',[])) == FORBIDDEN_UPSTREAM_ACTIONS, 'ACL09_FORBIDDEN_ACTIONS_INVALID')
    _require(handoff['memory_run_digest'] == memory_run['memory_run_digest'], 'ACL09_HANDOFF_MEMORY_RUN_MISMATCH')
    _require(handoff['memory_index_digest'] == memory_index['memory_index_digest'], 'ACL09_HANDOFF_MEMORY_INDEX_MISMATCH')
    _require(handoff['plan_portfolio_digest'] == portfolio['portfolio_digest'], 'ACL09_HANDOFF_PORTFOLIO_MISMATCH')
    _require(receipt['output_manifest_digest'] == manifest['manifest_digest'], 'ACL09_RECEIPT_MANIFEST_MISMATCH')
    _require(receipt['acl10_handoff_digest'] == handoff['handoff_digest'], 'ACL09_RECEIPT_HANDOFF_MISMATCH')
    _require(memory_run.get('state') == 'COMPLETED_NON_PROMOTIONAL', 'ACL09_RUN_STATE_INVALID')
    _require(memory_index.get('append_only') is True and memory_index.get('history_rewritten') is False, 'ACL09_MEMORY_IMMUTABILITY_INVALID')
    _require(security.get('passed') is True and integrity.get('passed') is True, 'ACL09_SECURITY_OR_INTEGRITY_FAILED')
    _require(not any([handoff.get('research_execution_allowed'),handoff.get('promotion_allowed'),handoff.get('live_order_submission_allowed'),handoff.get('capital_activation_allowed')]), 'ACL09_AUTHORITY_ESCALATION')
    _require(provenance.get('reaches_acl07_validation') is True and provenance.get('source_decisions_mutated') is False, 'ACL09_PROVENANCE_INVALID')
    decisions = []
    for item in admission_bundle.get('admission_decisions',[]):
        path = root/'memory/admission_decisions'/f"{item['admission_decision_id']}.json"
        document = load_json(path)
        _require(verify_embedded_digest(document,'admission_decision_digest'),'ACL09_ADMISSION_DECISION_INVALID')
        _require(document['admission_decision_digest'] == item['admission_decision_digest'],'ACL09_ADMISSION_DECISION_INDEX_MISMATCH')
        decisions.append(document)
    entries = {}
    for item in memory_index.get('entries',[]):
        document = load_json(root/'memory/entries'/f"{item['memory_entry_id']}.json")
        _require(verify_embedded_digest(document,'memory_entry_digest'),'ACL09_MEMORY_ENTRY_INVALID')
        _require(document['memory_entry_digest'] == item['memory_entry_digest'],'ACL09_MEMORY_ENTRY_INDEX_MISMATCH')
        entries[document['memory_entry_id']] = document
    quarantines = {}
    for item in memory_index.get('quarantines',[]):
        document = load_json(root/'memory/quarantine'/f"{item['quarantine_id']}.json")
        _require(verify_embedded_digest(document,'quarantine_digest'),'ACL09_QUARANTINE_INVALID')
        quarantines[document['quarantine_id']] = document
    proposals = []
    for item in portfolio.get('proposals',[]):
        document = load_json(root/'planner/proposals'/f"{item['proposal_id']}.json")
        _require(verify_embedded_digest(document,'proposal_digest'),'ACL09_PROPOSAL_INVALID')
        _require(document['proposal_digest'] == item['proposal_digest'],'ACL09_PROPOSAL_INDEX_MISMATCH')
        proposals.append(document)
    binding_body = {'schema_version':'1.0.0','memory_run_id':memory_run['memory_run_id'],'report_id':handoff['report_id'],'validation_id':handoff['validation_id'],'run_id':handoff['run_id'],'batch_id':handoff['batch_id'],'handoff_digest':handoff['handoff_digest'],'memory_run_digest':memory_run['memory_run_digest'],'memory_index_digest':memory_index['memory_index_digest'],'admission_bundle_digest':admission_bundle['admission_bundle_digest'],'plan_portfolio_digest':portfolio['portfolio_digest'],'event_ledger_digest':events['ledger_digest'],'provenance_graph_digest':provenance['graph_digest'],'reporting_eligible_candidate_count':handoff['reporting_eligible_candidate_count'],'source_decision_count':len(decisions),'source_memory_entry_count':len(entries),'source_quarantine_count':len(quarantines),'source_proposal_count':len(proposals)}
    return {'manifest':manifest,'receipt':receipt,'handoff':handoff,'memory_run':memory_run,'memory_index':memory_index,'admission_bundle':admission_bundle,'portfolio':portfolio,'events':events,'provenance':provenance,'security':security,'integrity':integrity,'decisions':decisions,'entries':entries,'quarantines':quarantines,'proposals':proposals,'binding':with_digest(binding_body,'binding_digest')}
