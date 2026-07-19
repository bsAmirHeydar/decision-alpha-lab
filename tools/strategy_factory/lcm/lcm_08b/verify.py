from __future__ import annotations
import json,re
from pathlib import Path
from .canonical import file_digest,digest_object
from .errors import VerificationError

REQUIRED=("pilot_migration_marker.json","input/lcm08a_binding.json","evidence/source_evidence_manifest.json","contracts/canonical_context_contract.json","contracts/legacy_adapter_contract.json","fixtures/golden_case_catalog.json","parity/parity_report.json","parity/variance_decision_registry.json","reports/hostile_review.json","reports/acceptance_report.json","handoff/lcm08b_to_lcm08c_handoff.json","output_manifest.json","pilot_migration_receipt.json")

def load(path):return json.loads(path.read_text(encoding="utf-8"))
def verify_package(root:Path):
    root=root.resolve()
    for rel in REQUIRED:
        if not (root/rel).is_file():raise VerificationError(f"missing package artifact: {rel}")
    manifest=load(root/'output_manifest.json')
    for row in manifest['files']:
        p=root/row['path']
        if not p.is_file():raise VerificationError(f"manifest path missing: {row['path']}")
        if p.stat().st_size!=row['size_bytes'] or file_digest(p)!=row['sha256']:raise VerificationError(f"manifest mismatch: {row['path']}")
    parity=load(root/'parity/parity_report.json');acceptance=load(root/'reports/acceptance_report.json');hostile=load(root/'reports/hostile_review.json');handoff=load(root/'handoff/lcm08b_to_lcm08c_handoff.json')
    if not parity['hard_parity_passed']:raise VerificationError('hard parity failed')
    if parity['unknown_mandatory_dimension_count']!=0:raise VerificationError('mandatory UNKNOWN remains')
    if not hostile['hostile_review_passed']:raise VerificationError('hostile review failed')
    if not acceptance['acceptance_gate_passed']:raise VerificationError('acceptance failed')
    for key in ('consumer_cutover_allowed','source_move_allowed','source_delete_allowed','runtime_authority_created','live_order_authority_created','capital_authority_created'):
        if handoff.get(key):raise VerificationError(f'authority expansion: {key}')
    return {"passed":True,"pilot_migration_id":acceptance['pilot_migration_id'],"golden_case_count":parity['case_count'],"manifest_file_count":manifest['file_count']}

def verify_installation(repo_root:Path,package_root:Path,patch_index:Path):
    lines=[x.strip() for x in patch_index.read_text(encoding='utf-8').splitlines() if x.strip()]
    missing=[x for x in lines if not (repo_root/x).exists()]
    if missing:raise VerificationError(f"patch index missing: {missing[:10]}")
    source=repo_root/'lab/03_experiments/EXP0015_intermarket_time_divergence/experiment.py'
    expected=load(package_root/'evidence/source_evidence_manifest.json')['source_artifact_sha256']
    if file_digest(source)!=expected:raise VerificationError('legacy source changed')
    return {**verify_package(package_root),"patch_index_count":len(lines),"installation_passed":True}
