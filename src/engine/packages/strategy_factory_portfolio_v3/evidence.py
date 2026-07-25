from __future__ import annotations
from .contracts import PortfolioEvidenceBundle
from .canonical import canonical_sha256
def build_evidence(ranked,model,quotes,plan,validation,runtime,telemetry,activation_allowed,limitations=()):
    return PortfolioEvidenceBundle('uce-i17-evidence','1.0.0',canonical_sha256(ranked),model.model_hash,tuple(q.quote_hash for q in quotes),plan.plan_hash,validation.report_hash,runtime.bundle_hash,telemetry.telemetry_hash,tuple(limitations),activation_allowed,'UCE-I18')
