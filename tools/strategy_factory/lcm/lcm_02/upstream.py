from __future__ import annotations
import csv
from pathlib import Path
from .canonical import digest_object,sha256_file
from .errors import IntegrityError
from .io import read_json

def latest_survey(repo_root: Path) -> Path:
    roots=sorted((repo_root/'registry/legacy_context_migration/surveys').glob('SURVEY_*'))
    if not roots: raise IntegrityError('LCM-01 survey not found')
    return roots[-1]
def verify_survey(root: Path) -> dict:
    manifest=read_json(root/'output_manifest.json')
    if manifest.get('output_manifest_digest')!=digest_object(manifest,'output_manifest_digest'): raise IntegrityError('LCM-01 manifest digest mismatch')
    for a in manifest.get('artifacts',[]):
        p=root/a['path']
        if not p.is_file() or p.stat().st_size!=a['size_bytes'] or sha256_file(p)!=a['sha256']: raise IntegrityError(f'LCM-01 artifact mismatch: {a["path"]}')
    summary=read_json(root/'reports/survey_summary.json')
    if summary.get('summary_digest')!=digest_object(summary,'summary_digest'): raise IntegrityError('LCM-01 summary digest mismatch')
    handoff=read_json(root/'handoff/lcm01_to_lcm02_handoff.json')
    if handoff.get('handoff_digest')!=digest_object(handoff,'handoff_digest'): raise IntegrityError('LCM-01 handoff digest mismatch')
    if 'CLASSIFY_SURVEYED_ARTIFACTS' not in handoff.get('allowed_actions',[]): raise IntegrityError('LCM-02 classification not authorized')
    with (root/'inventory/artifact_inventory.csv').open(encoding='utf-8',newline='') as f: count=sum(1 for _ in csv.DictReader(f))
    if count!=summary['artifact_count']: raise IntegrityError('LCM-01 inventory cardinality mismatch')
    return {'survey_id':summary['survey_id'],'summary':summary,'handoff':handoff,'manifest':manifest}
