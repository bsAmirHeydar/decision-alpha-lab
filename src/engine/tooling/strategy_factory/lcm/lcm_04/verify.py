from __future__ import annotations
from pathlib import Path
from .canonical import digest_object,sha256_file
from .errors import IntegrityError
from .event_ledger import verify as verify_events
from .io import read_json,read_jsonl
from .trace import reference_inputs,build_trace,trace_bundle
from .known_time import audit
from .upstream import latest_identity,verify_identity

def verify_manifest(root: Path):
    m=read_json(root/'output_manifest.json')
    if m.get('output_manifest_digest')!=digest_object(m,'output_manifest_digest'): raise IntegrityError('LCM-04 manifest digest mismatch')
    declared=set()
    for a in m['artifacts']:
        p=root/a['path'];declared.add(a['path'])
        if not p.is_file() or p.stat().st_size!=a['size_bytes'] or sha256_file(p)!=a['sha256']: raise IntegrityError(f'LCM-04 artifact mismatch: {a["path"]}')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='output_manifest.json'}
    if actual!=declared: raise IntegrityError('LCM-04 artifact set mismatch')
    return m

def verify_package(root: Path):
    m=verify_manifest(root);marker=read_json(root/'characterization_marker.json');receipt=read_json(root/'characterization_receipt.json')
    summary=read_json(root/'reports/characterization_summary.json');coverage=read_json(root/'reports/coverage_report.json');handoff=read_json(root/'handoff/lcm04_to_lcm05_handoff.json')
    for obj,field in [(marker,'marker_digest'),(receipt,'receipt_digest'),(summary,'summary_digest'),(coverage,'coverage_digest'),(handoff,'handoff_digest')]:
        if obj.get(field)!=digest_object(obj,field): raise IntegrityError(f'digest mismatch: {field}')
    packets=list(read_jsonl(root/'packets/characterization_packet_index.jsonl'));amb=list(read_jsonl(root/'packets/identity_ambiguity_characterization_queue.jsonl'))
    profiles=list(read_jsonl(root/'profiles/source_static_profiles.jsonl'));plans=list(read_jsonl(root/'instrumentation/instrumentation_plans.jsonl'))
    if len(packets)!=summary['identity_packet_count'] or len(amb)!=summary['identity_ambiguity_packet_count']: raise IntegrityError('packet count mismatch')
    if len(profiles)!=len(packets) or len(plans)!=len(packets): raise IntegrityError('profile or plan coverage mismatch')
    if any(x['legacy_execution_allowed'] for x in packets): raise IntegrityError('unexpected legacy execution eligibility')
    bundle=read_json(root/'traces/reference_trace_bundle.json');recomputed=trace_bundle(build_trace(reference_inputs()))
    if bundle['bundle_digest']!=recomputed['bundle_digest']: raise IntegrityError('reference replay mismatch')
    events=list(read_jsonl(root/'traces/reference_normalized_events.jsonl'))
    if audit(events)['status']!='PASS': raise IntegrityError('known-time audit failed')
    verify_events(read_json(root/'events/characterization_event_ledger.json'))
    if summary['legacy_trace_execution_count']!=0 or summary['acceptance_gate_passed'] is not False: raise IntegrityError('legacy completion overclaim')
    denied=['source_instrumentation_mutation_performed','source_move_performed','source_delete_performed','semantic_refactor_performed','merge_performed','cutover_performed','runtime_authority_created','live_order_authority_created','capital_authority_created']
    if any(summary.get(k) for k in denied): raise IntegrityError('LCM-04 authority escalation')
    return {'passed':True,'characterization_run_id':marker['characterization_run_id'],'identity_packet_count':len(packets),
            'ambiguity_packet_count':len(amb),'reference_case_count':summary['reference_fixture_case_count'],
            'reference_event_count':summary['reference_fixture_event_count'],'legacy_trace_execution_count':0,
            'package_artifact_count':m['artifact_count']}

def verify_installation(repo_root: Path,characterization_root: Path,patch_index: Path):
    verify_identity(latest_identity(repo_root));result=verify_package(characterization_root);missing=[]
    for line in patch_index.read_text(encoding='utf-8').splitlines():
        rel=line.strip().replace('\\','/')
        if rel and not (repo_root/rel).is_file(): missing.append(rel)
    return {**result,'installation_passed':not missing,'missing_patch_files':missing}
