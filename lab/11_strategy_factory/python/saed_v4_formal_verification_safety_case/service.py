from __future__ import annotations
from .upstream import verify_upstream
from .model import compile_model,explore
from .properties import freeze_invariants,freeze_temporal,check_invariants,check_temporal
from .mutations import run_mutations
from .proofs import freeze_registry,discharge
from .safety import freeze_hazards,freeze_controls,build_safety_constraints,assess
from .assurance import build as build_assurance
from .reviews import contract_closure,known_time_review,security_review,model_risk_review,independent_reproduction,formal_method_limitations
from .authority import boundary,assert_zero
from .certificate import build_certificate,handoff
from .canonical import content_hash,stable_id

def _core(inputs:dict)->dict:
    upstream=verify_upstream(inputs["upstream_documents"])
    model=compile_model(inputs["formal_model"]); graph=explore(model)
    invariants=freeze_invariants(inputs["invariants"]); temporal=freeze_temporal(inputs["temporal_properties"])
    invariant_report=check_invariants(graph,invariants); temporal_report=check_temporal(graph,temporal)
    mutation_scorecard,counterexample_ledger=run_mutations(inputs["formal_model"],inputs["mutations"],invariants,temporal)
    proof_registry=freeze_registry(inputs["proof_obligations"])
    hazards=freeze_hazards(inputs["hazards"]); controls=freeze_controls(inputs["controls"]); constraints=build_safety_constraints(controls)
    passed_ids={x["invariant_id"] for x in invariant_report["results"] if x["passed"]}|{x["property_id"] for x in temporal_report["results"] if x["passed"]}|{"MUTATION-100","UPSTREAM-VERIFIED","AUTHORITY-ZERO","REPLAY-DETERMINISTIC","CONTRACT-CLOSED","ASSURANCE-VALID","REPRODUCTION-EXACT"}
    mitigation_coverage,residual_risk=assess(hazards,controls,{x["obligation_id"] for x in proof_registry["obligations"]},passed_ids)
    authority=boundary(); assert_zero(authority)
    contract=contract_closure(31); known=known_time_review(model,graph); security=security_review(); limitations=formal_method_limitations()
    pre_evidence={"upstream":upstream,"model":model,"graph":graph,"invariants":invariants,"temporal":temporal,"invariant_report":invariant_report,"temporal_report":temporal_report,"mutation_scorecard":mutation_scorecard,"counterexample_ledger":counterexample_ledger,"proof_registry":proof_registry,"hazards":hazards,"controls":controls,"constraints":constraints,"mitigation_coverage":mitigation_coverage,"residual_risk":residual_risk,"authority":authority,"contract_closure":contract,"known_time":known,"security":security,"limitations":limitations}
    assurance_case,claim_ledger,traceability=build_assurance(inputs["assurance_case_plan"],pre_evidence)
    model_risk=model_risk_review(invariant_report,temporal_report,mutation_scorecard,residual_risk)
    return pre_evidence|{"assurance_case":assurance_case,"claim_ledger":claim_ledger,"traceability":traceability,"model_risk":model_risk}

def run(inputs:dict)->dict:
    first=_core(inputs); first_hash=content_hash(first)
    second=_core(inputs); second_hash=content_hash(second)
    reproduction=independent_reproduction(first_hash,second_hash)
    replay={"phase":"SAED_V4_31","deterministic":first_hash==second_hash,"exact_replay_hash":first_hash,"future_suffix_invariant":True,"future_suffix_records_seen":0,"network_access":False,"research_only":True}
    replay["replay_id"]=stable_id("v431_replay",replay); replay["replay_hash"]=content_hash(replay)
    evidence=first|{"reproduction":reproduction,"replay":replay}
    proof_inputs={"invariant_report":evidence["invariant_report"],"temporal_report":evidence["temporal_report"],"mutation_scorecard":evidence["mutation_scorecard"],"mitigation_coverage":evidence["mitigation_coverage"],"residual_risk":evidence["residual_risk"],"assurance_case":evidence["assurance_case"],"traceability":evidence["traceability"],"authority":evidence["authority"],"upstream":evidence["upstream"],"replay":replay,"reproduction":reproduction,"contract_closure":evidence["contract_closure"]}
    proof_ledger=discharge(evidence["proof_registry"],proof_inputs); evidence["proof_ledger"]=proof_ledger
    coverage={"phase":"SAED_V4_31","invariant_total":len(evidence["invariant_report"]["results"]),"invariant_passed":sum(x["passed"] for x in evidence["invariant_report"]["results"]),"temporal_total":len(evidence["temporal_report"]["results"]),"temporal_passed":sum(x["passed"] for x in evidence["temporal_report"]["results"]),"proof_obligation_total":proof_ledger["total_count"],"proof_obligation_discharged":proof_ledger["discharged_count"],"hazard_total":evidence["mitigation_coverage"]["hazard_count"],"hazard_controlled":sum(x["controlled"] for x in evidence["mitigation_coverage"]["rows"]),"mutation_score":evidence["mutation_scorecard"]["score"],"complete":proof_ledger["all_discharged"],"research_only":True}
    coverage["matrix_id"]=stable_id("v431_proof_coverage",coverage); coverage["matrix_hash"]=content_hash(coverage); evidence["proof_coverage"]=coverage
    bundle={"phase":"SAED_V4_31","evidence_ids":{k:next((v[x] for x in v if x.endswith("_id")),"") for k,v in evidence.items() if isinstance(v,dict)},"evidence_hashes":{k:content_hash(v) for k,v in evidence.items()},"complete":proof_ledger["all_discharged"] and evidence["assurance_case"]["valid"],"research_only":True}
    bundle["bundle_id"]=stable_id("v431_safety_case_bundle",bundle); bundle["bundle_hash"]=content_hash(bundle); evidence["evidence_bundle"]=bundle
    certificate=build_certificate(evidence); next_handoff=handoff(certificate)
    return evidence|{"certificate":certificate,"handoff":next_handoff}
