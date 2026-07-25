from __future__ import annotations
from .contracts import exact,sha256
from .errors import UpstreamError
from .canonical import seal
CERT_KEYS=["actual_external_scale_evidence_complete","actual_failover_passed","actual_scale_soak_passed","capital_activation_allowed","certificate_hash","certificate_id","claim_ceiling","evidence_hash","fleet_reference_ready","live_order_submission_allowed","next_phase","phase","production_authorized","release_hash","research_only","status"]
HANDOFF_KEYS=["allowed_next_work","certificate_hash","forbidden_next_work","handoff_hash","handoff_id","kind","next_phase","phase","production_authorized","release_hash","required_external_gates","research_only"]
def verify_upstream(certificate:dict,handoff:dict)->dict:
 exact(certificate,CERT_KEYS,name="v4_40_certificate");exact(handoff,HANDOFF_KEYS,name="v4_40_handoff")
 if certificate["phase"]!="SAED_V4_40" or certificate["next_phase"]!="SAED_V4_41":raise UpstreamError("certificate phase mismatch")
 if handoff["phase"]!="SAED_V4_40" or handoff["next_phase"]!="SAED_V4_41" or handoff["kind"]!="v4_40_handoff":raise UpstreamError("handoff phase mismatch")
 for k in ["certificate_hash","release_hash"]:sha256(certificate[k],f"certificate.{k}");sha256(handoff[k],f"handoff.{k}")
 if any(certificate[k]!=handoff[k] for k in ["certificate_hash","release_hash"]):raise UpstreamError("upstream binding mismatch")
 if certificate["research_only"] is not True or handoff["research_only"] is not True:raise UpstreamError("research-only required")
 if certificate["production_authorized"] is not False or handoff["production_authorized"] is not False:raise UpstreamError("upstream authority boundary violated")
 required={"continuous_fleet_surveillance","drift_and_degradation_monitoring","incident_learning","context_retirement","model_retirement"}
 if not required<=set(handoff["allowed_next_work"]):raise UpstreamError("surveillance/retirement work not authorized")
 return seal({"phase":"SAED_V4_41","verified":True,"upstream_phase":"SAED_V4_40","certificate_hash":certificate["certificate_hash"],"release_hash":certificate["release_hash"],"required_external_gates":sorted(handoff["required_external_gates"]),"research_only":True,"production_authorized":False},"v441_upstream","receipt_id","receipt_hash")
