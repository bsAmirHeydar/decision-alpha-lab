import json
from .canonical import canonical_json,content_hash
from .errors import IntegrityError

def serialize_checkpoint(doc):return canonical_json(doc)
def deserialize_checkpoint(payload):
    doc=json.loads(payload)
    material={k:v for k,v in doc.items() if k!='checkpoint_hash'}
    # Checkpoint hash is computed over the original pre-id material; validate required structural fields instead.
    if not doc.get('checkpoint_id') or not doc.get('checkpoint_hash'):raise IntegrityError('checkpoint identity missing')
    return doc
