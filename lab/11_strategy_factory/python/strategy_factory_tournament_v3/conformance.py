from __future__ import annotations
from .inventory import future_suffix_invariant
from .evidence import verify_evidence_bundle

def conformance_report(*,prefix,suffix,cut_ms,evidence_bundle,decision):
 checks={'future_suffix_invariant':future_suffix_invariant(prefix,suffix,cut_ms),'evidence_hash_valid':verify_evidence_bundle(evidence_bundle),'decision_not_fake_promote':not(decision.status.value=='promote' and decision.promotion_bundle_hash is None)}
 return {'version':'1.0.0','checks':checks,'passed':all(checks.values())}
