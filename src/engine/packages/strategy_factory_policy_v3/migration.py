from __future__ import annotations
from .errors import PolicyError

def migrate_graph_document(document):
    doc=dict(document); version=doc.get('version')
    if version=='1.0.0': return doc
    if version=='0.9.0':
        if 'policy_id' not in doc: raise PolicyError('legacy_graph_missing_policy_id','0.9.0 graph requires policy_id')
        doc['graph_id']=doc.pop('policy_id'); doc['version']='1.0.0'; doc.setdefault('mode','manual_only'); return doc
    raise PolicyError('unsupported_graph_version',f'unsupported graph version {version!r}')
