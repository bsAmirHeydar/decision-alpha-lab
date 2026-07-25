from __future__ import annotations
from dataclasses import asdict
from .canonical import canonical_sha256
from .parity import certify_parity
def run_conformance(manifest,preprocessing,model,export_bytes,vectors,tolerance):
    cert=certify_parity(manifest,preprocessing,model,export_bytes,vectors,tolerance,created_at_ms=0)
    return {'status':cert.status.value,'certificate_hash':cert.certificate_hash,'observation_count':len(cert.observations),'vector_hash':cert.vector_set_hash,'max_absolute_error':max(o.max_absolute_error for o in cert.observations)}
