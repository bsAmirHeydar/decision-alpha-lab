from __future__ import annotations
from pathlib import Path
from .canonical import digest_object,sha256_file
from .errors import IntegrityError
from .io import read_json,read_jsonl

def latest_identity(repo_root: Path) -> Path:
    roots=sorted((repo_root/'registry/history/lcm/identities').glob('IDENTITY_*'))
    if not roots: raise IntegrityError('LCM-03 identity package not found')
    return roots[-1]

def verify_manifest(root: Path):
    m=read_json(root/'output_manifest.json')
    if m.get('output_manifest_digest')!=digest_object(m,'output_manifest_digest'): raise IntegrityError('LCM-03 manifest digest mismatch')
    declared=set()
    for a in m.get('artifacts',[]):
        p=root/a['path'];declared.add(a['path'])
        if not p.is_file() or p.stat().st_size!=a['size_bytes'] or sha256_file(p)!=a['sha256']: raise IntegrityError(f'LCM-03 artifact mismatch: {a["path"]}')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='output_manifest.json'}
    if actual!=declared: raise IntegrityError('LCM-03 artifact set mismatch')
    return m

def verify_identity(root: Path):
    m=verify_manifest(root);marker=read_json(root/'identity_marker.json');receipt=read_json(root/'identity_receipt.json');handoff=read_json(root/'handoff/lcm03_to_lcm04_handoff.json')
    for obj,field,name in [(marker,'marker_digest','marker'),(receipt,'receipt_digest','receipt'),(handoff,'handoff_digest','handoff')]:
        if obj.get(field)!=digest_object(obj,field): raise IntegrityError(f'LCM-03 {name} digest mismatch')
    if receipt['handoff_digest']!=handoff['handoff_digest'] or receipt['identity_run_id']!=marker['identity_run_id']: raise IntegrityError('LCM-03 binding mismatch')
    if handoff.get('characterization_execution_allowed') is not False: raise IntegrityError('unexpected legacy execution authority')
    return {'root':root,'manifest':m,'marker':marker,'receipt':receipt,'handoff':handoff,
            'identities':list(read_jsonl(root/'identities/canonical_identity_candidates.jsonl')),
            'ambiguities':list(read_jsonl(root/'unresolved/identity_ambiguity_queue.jsonl'))}
