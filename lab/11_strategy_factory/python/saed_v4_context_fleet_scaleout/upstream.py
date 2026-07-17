from __future__ import annotations
from .contracts import exact,sha256
from .errors import UpstreamError
from .canonical import seal
CERT_KEYS=["actual_prospective_paper_passed","actual_prospective_shadow_passed","capital_activation_allowed","certificate_hash","certificate_id","claim_ceiling","evidence_hash","micro_live_authorized","micro_live_eligible","next_phase","order_submission_allowed","phase","production_authorized","reference_paper_passed","reference_shadow_passed","release_hash","research_only","runtime_bundle_hash","status"]
HANDOFF_KEYS=["allowed_next_work","certificate_hash","forbidden_next_work","handoff_hash","handoff_id","kind","micro_live_authorized","next_phase","phase","production_authorized","release_hash","required_external_gates","research_only","runtime_bundle_hash"]
def verify_upstream(certificate:dict,handoff:dict)->dict:
 exact(certificate,CERT_KEYS,name="v4_39_certificate");exact(handoff,HANDOFF_KEYS,name="v4_39_handoff")
 if certificate["phase"]!="SAED_V4_39" or certificate["next_phase"]!="SAED_V4_40":raise UpstreamError("certificate phase mismatch")
 if handoff["phase"]!="SAED_V4_39" or handoff["next_phase"]!="SAED_V4_40" or handoff["kind"]!="v4_39_handoff":raise UpstreamError("handoff phase mismatch")
 for k in ["certificate_hash","release_hash","runtime_bundle_hash"]:sha256(certificate[k],f"certificate.{k}");sha256(handoff[k],f"handoff.{k}")
 if any(certificate[k]!=handoff[k] for k in ["certificate_hash","release_hash","runtime_bundle_hash"]):raise UpstreamError("upstream binding mismatch")
 if certificate["research_only"] is not True or handoff["research_only"] is not True:raise UpstreamError("research-only required")
 if certificate["production_authorized"] is not False or handoff["production_authorized"] is not False or certificate["micro_live_authorized"] is not False:raise UpstreamError("upstream authority boundary violated")
 required={"context_fleet_control_plane","fleet_observability","fleet_rollout_simulation"}
 if not required<=set(handoff["allowed_next_work"]):raise UpstreamError("fleet work not authorized")
 return seal({"phase":"SAED_V4_40","verified":True,"upstream_phase":"SAED_V4_39","certificate_hash":certificate["certificate_hash"],"release_hash":certificate["release_hash"],"runtime_bundle_hash":certificate["runtime_bundle_hash"],"required_external_gates":sorted(handoff["required_external_gates"]),"research_only":True,"production_authorized":False},"v440_upstream","receipt_id","receipt_hash")
