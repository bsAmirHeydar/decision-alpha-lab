from __future__ import annotations
from dataclasses import asdict
from .canonical import canonical_sha256
from .contracts import RuntimeRequest,RuntimeDecision

def replay(host,requests):
    ordered=sorted(requests,key=lambda r:(r.known_time_ms,r.request_id))
    decisions=tuple(host.decide(r) for r in ordered)
    return decisions,canonical_sha256([d.decision_hash for d in decisions])
def assert_prefix_stable(host_factory,requests):
    full,full_hash=replay(host_factory(),requests)
    for i in range(1,len(requests)+1):
        prefix,_=replay(host_factory(),requests[:i])
        if tuple(d.decision_hash for d in prefix)!=tuple(d.decision_hash for d in full[:i]):return False
    return True
