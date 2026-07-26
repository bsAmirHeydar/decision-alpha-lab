from __future__ import annotations
import json
from pathlib import Path
from .registries import ARTIFACT_ROLES,PRIMARY_DISPOSITIONS,ACTIVITY_STATUSES,AUTHORITY_SURFACES

def validate(repo_root: Path):
    base=repo_root/'registry/history/lcm/lcm_02'
    json_count=0
    for p in sorted(base.rglob('*.json')):
        json.loads(p.read_text(encoding='utf-8')); json_count+=1
    required=[repo_root/'docs/architecture/master/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/11_PHASE_DELIVERIES/LCM_02/00_MOC.md',repo_root/'docs/architecture/master/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/05_PHASES/LCM_02_CLASSIFICATION_OWNERSHIP_AND_AUTHORITY.md']
    return {'passed':all(p.is_file() for p in required),'registry_json_count':json_count,'role_count':len(ARTIFACT_ROLES),'disposition_count':len(PRIMARY_DISPOSITIONS),'activity_count':len(ACTIVITY_STATUSES),'authority_surface_count':len(AUTHORITY_SURFACES),'missing_required_docs':[str(p) for p in required if not p.is_file()]}
