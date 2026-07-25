from __future__ import annotations
import csv,json
from pathlib import Path
from .canonical import digest_object,sha256_file
from .errors import IntegrityError
from .event_ledger import verify as verify_events
from .io import read_json
from .upstream import latest_survey,verify_survey

def verify_output_manifest(root: Path):
    m=read_json(root/'output_manifest.json')
    if m.get('output_manifest_digest')!=digest_object(m,'output_manifest_digest'): raise IntegrityError('LCM-02 output manifest digest mismatch')
    declared=set()
    for a in m.get('artifacts',[]):
        p=root/a['path']; declared.add(a['path'])
        if not p.is_file() or p.stat().st_size!=a['size_bytes'] or sha256_file(p)!=a['sha256']: raise IntegrityError(f'LCM-02 artifact mismatch: {a["path"]}')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='output_manifest.json'}
    if actual!=declared: raise IntegrityError(f'LCM-02 artifact set mismatch missing={sorted(declared-actual)[:3]} extra={sorted(actual-declared)[:3]}')
    return m

def verify_package(root: Path):
    m=verify_output_manifest(root); marker=read_json(root/'classification_marker.json'); cid=marker['classification_id']
    if marker.get('marker_digest')!=digest_object(marker,'marker_digest'): raise IntegrityError('marker digest mismatch')
    summary=read_json(root/'reports/classification_summary.json')
    if summary.get('summary_digest')!=digest_object(summary,'summary_digest'): raise IntegrityError('classification summary digest mismatch')
    with (root/'artifacts/artifact_classification_records.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
    if len(rows)!=summary['artifact_count'] or len({r['artifact_path'] for r in rows})!=len(rows): raise IntegrityError('classification record cardinality mismatch')
    if not all(r['primary_disposition'] for r in rows): raise IntegrityError('missing primary disposition')
    if any(r['artifact_role']=='GENERATED_PROJECTION' and r['generated_projection_canonical_authority']=='true' for r in rows): raise IntegrityError('generated projection promoted to canonical')
    if any(r['protected_platform_asset']=='true' and r['source_move_authorized']=='true' for r in rows): raise IntegrityError('protected platform move authority')
    if any(r['security_sensitive']=='true' and r['primary_disposition']!='SECURITY_RESTRICTED' for r in rows): raise IntegrityError('security-sensitive disposition downgrade')
    owner=read_json(root/'owners/owner_role_registry.json')
    if owner.get('registry_digest')!=digest_object(owner,'registry_digest'): raise IntegrityError('owner registry digest mismatch')
    unresolved=read_json(root/'unresolved/unresolved_summary.json')
    if unresolved.get('summary_digest')!=digest_object(unresolved,'summary_digest'): raise IntegrityError('unresolved summary digest mismatch')
    verify_events(read_json(root/'events/classification_event_ledger.json'))
    handoff=read_json(root/'handoff/lcm02_to_lcm03_handoff.json')
    if handoff.get('handoff_digest')!=digest_object(handoff,'handoff_digest'): raise IntegrityError('handoff digest mismatch')
    receipt=read_json(root/'classification_receipt.json')
    if receipt.get('receipt_digest')!=digest_object(receipt,'receipt_digest'): raise IntegrityError('receipt digest mismatch')
    if receipt.get('classification_id')!=cid or receipt.get('artifact_classification_record_count')!=len(rows): raise IntegrityError('receipt classification binding mismatch')
    if receipt.get('classification_summary_digest')!=summary['summary_digest']: raise IntegrityError('receipt summary binding mismatch')
    if receipt.get('owner_registry_digest')!=owner['registry_digest']: raise IntegrityError('receipt owner registry binding mismatch')
    if receipt.get('unresolved_summary_digest')!=unresolved['summary_digest']: raise IntegrityError('receipt unresolved summary binding mismatch')
    if receipt.get('handoff_digest')!=handoff['handoff_digest']: raise IntegrityError('receipt handoff binding mismatch')
    denied=['source_move_performed','source_delete_performed','semantic_refactor_performed','merge_performed','cutover_performed','human_approval_claimed','runtime_authority_created','live_order_authority_created','capital_authority_created']
    if any(receipt.get(k) for k in denied): raise IntegrityError('receipt authority escalation')
    return {'passed':True,'classification_id':cid,'artifact_count':len(rows),'security_sensitive_count':summary['security_sensitive_count'],'unknown_role_count':summary['unknown_role_count'],'active_candidate_count':summary['active_candidate_count'],'package_artifact_count':m['artifact_count']}

def verify_installation(repo_root: Path, classification_root: Path, patch_index: Path):
    verify_survey(latest_survey(repo_root)); result=verify_package(classification_root); missing=[]
    for line in patch_index.read_text(encoding='utf-8').splitlines():
        rel=line.strip().replace('\\','/')
        if rel and not (repo_root/rel).is_file():missing.append(rel)
    return {**result,'installation_passed':not missing,'missing_patch_files':missing}
