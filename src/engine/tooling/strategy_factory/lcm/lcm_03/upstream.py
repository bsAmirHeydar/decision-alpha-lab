from __future__ import annotations
import csv
from pathlib import Path
from .canonical import digest_object,sha256_file
from .errors import IntegrityError
from .io import read_json

def latest_classification(repo_root: Path) -> Path:
    roots=sorted((repo_root/'registry/history/lcm/classifications').glob('CLASSIFICATION_*'))
    if not roots: raise IntegrityError('LCM-02 classification package not found')
    return roots[-1]
def survey_root(repo_root: Path, survey_id: str) -> Path:
    root=repo_root/'registry/history/lcm/surveys'/survey_id
    if not root.is_dir(): raise IntegrityError('bound LCM-01 survey not found')
    return root
def verify_classification(root: Path) -> dict:
    manifest=read_json(root/'output_manifest.json')
    if manifest.get('output_manifest_digest')!=digest_object(manifest,'output_manifest_digest'): raise IntegrityError('LCM-02 output manifest digest mismatch')
    for a in manifest.get('artifacts',[]):
        p=root/a['path']
        if not p.is_file() or p.stat().st_size!=a['size_bytes'] or sha256_file(p)!=a['sha256']: raise IntegrityError(f'LCM-02 artifact mismatch: {a["path"]}')
    marker=read_json(root/'classification_marker.json')
    if marker.get('marker_digest')!=digest_object(marker,'marker_digest'): raise IntegrityError('LCM-02 marker digest mismatch')
    summary=read_json(root/'reports/classification_summary.json')
    if summary.get('summary_digest')!=digest_object(summary,'summary_digest'): raise IntegrityError('LCM-02 summary digest mismatch')
    handoff=read_json(root/'handoff/lcm02_to_lcm03_handoff.json')
    if handoff.get('handoff_digest')!=digest_object(handoff,'handoff_digest'): raise IntegrityError('LCM-02 handoff digest mismatch')
    required={'REGISTER_CANONICAL_IDENTITIES','REGISTER_LEGACY_ALIASES','PROPOSE_FAMILY_IDENTITY_MAP'}
    if not required.issubset(set(handoff.get('allowed_actions',[]))): raise IntegrityError('LCM-03 actions not authorized')
    return {'classification_id':marker['classification_id'],'survey_id':summary['survey_id'],'summary':summary,'handoff':handoff,'manifest':manifest,'root':root}
