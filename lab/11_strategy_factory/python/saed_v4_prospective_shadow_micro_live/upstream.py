from __future__ import annotations
from copy import deepcopy
from .contracts import exact,sha256
from .errors import UpstreamError
from .canonical import seal
CERT_KEYS=["actual_metaeditor_compile_passed","actual_terminal_parity_passed","bundle_hash","capital_activation_allowed","certificate_hash","certificate_id","claim_ceiling","evidence_hash","next_phase","order_submission_allowed","phase","production_authorized","release_hash","research_only","status","synthetic_parity_passed"]
HANDOFF_KEYS=["allowed_next_work","bundle_hash","certificate_hash","external_runtime_evidence_complete","forbidden_next_work","handoff_hash","handoff_id","kind","next_phase","phase","production_authorized","required_external_gates","research_only"]
def verify_upstream(certificate:dict,handoff:dict)->dict:
 exact(certificate,CERT_KEYS,name="v4_38_certificate"); exact(handoff,HANDOFF_KEYS,name="v4_38_handoff")
 if certificate["phase"]!="SAED_V4_38" or certificate["next_phase"]!="SAED_V4_39":raise UpstreamError("certificate phase mismatch")
 if handoff["phase"]!="SAED_V4_38" or handoff["next_phase"]!="SAED_V4_39" or handoff["kind"]!="v4_38_handoff":raise UpstreamError("handoff phase mismatch")
 for k in ["bundle_hash","certificate_hash"]:
  sha256(certificate[k],f"certificate.{k}"); sha256(handoff[k],f"handoff.{k}")
 if certificate["certificate_hash"]!=handoff["certificate_hash"] or certificate["bundle_hash"]!=handoff["bundle_hash"]:raise UpstreamError("upstream binding mismatch")
 if certificate["research_only"] is not True or handoff["research_only"] is not True:raise UpstreamError("research-only upstream required")
 if certificate["production_authorized"] is not False or handoff["production_authorized"] is not False:raise UpstreamError("upstream production authority forbidden")
 if "prospective_paper" not in handoff["allowed_next_work"] or "shadow_replay" not in handoff["allowed_next_work"]:raise UpstreamError("required next work missing")
 return seal({"phase":"SAED_V4_39","verified":True,"upstream_phase":"SAED_V4_38","bundle_hash":certificate["bundle_hash"],"certificate_hash":certificate["certificate_hash"],"external_runtime_evidence_complete":handoff["external_runtime_evidence_complete"],"required_external_gates":sorted(handoff["required_external_gates"]),"research_only":True,"production_authorized":False},"v439_upstream","receipt_id","receipt_hash")
