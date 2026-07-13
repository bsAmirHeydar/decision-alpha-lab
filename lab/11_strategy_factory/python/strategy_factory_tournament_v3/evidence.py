from __future__ import annotations
from dataclasses import asdict
from .canonical import canonical_sha256

def build_evidence_bundle(**artifacts):
 payload={k:(asdict(v) if hasattr(v,'__dataclass_fields__') else v) for k,v in sorted(artifacts.items())}
 return {'version':'1.0.0','artifacts':payload,'bundle_hash':canonical_sha256(payload)}
def verify_evidence_bundle(bundle)->bool:
 return bundle.get('bundle_hash')==canonical_sha256(bundle.get('artifacts',{}))
