from __future__ import annotations
from .errors import RuntimeContractError
def migrate_manifest(payload):
    version=payload.get('version')
    if version=='1.0.0':return dict(payload)
    if version=='0.9.0':
        out=dict(payload);out['version']='1.0.0';out.setdefault('limitations',[]);return out
    raise RuntimeContractError('unsupported_manifest_version','manifest version cannot be migrated',{'version':version})
