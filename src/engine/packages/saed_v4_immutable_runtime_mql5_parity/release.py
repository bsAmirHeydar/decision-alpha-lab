from __future__ import annotations
from .canonical import seal

def build_release_candidate(bundle:dict,manifest:dict,codegen:dict,parity:dict,external:dict,authority:dict)->dict:
 internal_passed=bool(parity["passed"] and manifest["file_count"]>=2 and codegen["source_count"]>=2)
 external_passed=bool(external["external_runtime_evidence_complete"])
 production_authorized=False
 gates=[
  {"gate_id":"G01_BUNDLE_IMMUTABILITY","status":"PASSED" if bundle["mutable_fields"]==[] else "FAILED"},
  {"gate_id":"G02_HERMETIC_BUILD","status":"PASSED" if bundle["network_dependencies"]==[] else "FAILED"},
  {"gate_id":"G03_SYNTHETIC_PARITY","status":"PASSED" if parity["passed"] else "FAILED"},
  {"gate_id":"G04_METAEDITOR_COMPILE","status":"PASSED" if external["actual_metaeditor_compile_passed"] else "PENDING_EXTERNAL"},
  {"gate_id":"G05_TERMINAL_PARITY","status":"PASSED" if external["actual_terminal_parity_passed"] else "PENDING_EXTERNAL"},
  {"gate_id":"G06_PRODUCTION_AUTHORITY","status":"DENIED"},]
 return seal({"phase":"SAED_V4_38","bundle_hash":bundle["bundle_hash"],"manifest_hash":manifest["manifest_hash"],"codegen_hash":codegen["codegen_hash"],"parity_report_hash":parity["parity_report_hash"],"external_matrix_hash":external["matrix_hash"],"gates":gates,"internal_reference_accepted":internal_passed,"external_runtime_qualified":external_passed,"release_eligible_for_v4_39_shadow":internal_passed and external_passed,"production_authorized":production_authorized,"capital_activation_allowed":False,"order_submission_allowed":False,"decision":"ACCEPT_REFERENCE_BLOCK_EXTERNAL" if internal_passed and not external_passed else "REJECT" if not internal_passed else "READY_FOR_V4_39_SHADOW_ONLY","research_only":True},"v438_release","release_candidate_id","release_candidate_hash")
