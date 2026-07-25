from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,seal
from .upstream import verify_upstream
from .constitution import freeze_constitution,authority_boundary
from .cohort import freeze_cohort,validate_observations
from .modes import freeze_mode_ladder
from .broker import freeze_broker_profile,qualification_matrix
from .risk import freeze_risk_envelope,evaluate_intent
from .intent import build_intent,intent_ledger
from .paper import simulate
from .shadow import run as run_shadow
from .reconciliation import reconcile
from .surveillance import monitor
from .incident import freeze_runbook,drill
from .external import freeze_external_evidence
from .stage_gate import qualify
from .governance import review_bundle
from .evidence import bundle as evidence_bundle

def run_reference(v:dict)->dict:
 up=verify_upstream(v["upstream_certificate"],v["upstream_handoff"]);constitution=freeze_constitution(v["constitution"]);authority=authority_boundary();cohort=freeze_cohort(v["cohort"]);obs_receipt=validate_observations(v["observations"],cohort);ladder=freeze_mode_ladder(v["mode_ladder"]);broker=freeze_broker_profile(v["broker_profile"]);risk=freeze_risk_envelope(v["risk_envelope"]);runbook=freeze_runbook(v["incident_runbook"]);external=freeze_external_evidence(v["external_evidence"])
 runtime_binding=seal({"phase":"SAED_V4_39","bundle_hash":up["bundle_hash"],"certificate_hash":up["certificate_hash"],"immutable":True,"runtime_mutation_allowed":False,"research_only":True},"v439_runtime_binding","binding_id","binding_hash")
 intents=[build_intent(o,runtime_binding) for o in v["observations"]]
 state={"orders_today":0,"concurrent_positions":0,"daily_loss_fraction":0.0,"drawdown_fraction":0.0,"kill_switch_armed":True}
 risk_decisions=[evaluate_intent(i,risk,state) for i in intents]
 intents_ledger=intent_ledger(intents);paper=simulate(intents,v["observations"],risk_decisions,broker);shadow=run_shadow(intents,v["observations"],paper);recon=reconcile(intents,paper);surv=monitor(v["observations"],paper,shadow,risk);drills=drill(runbook);broker_matrix=qualification_matrix(broker,external["items"]);qualification=qualify(cohort,paper,shadow,recon,surv,drills,external,broker_matrix);reviews=review_bundle(v["reviews"],qualification["qualification_hash"])
 baseline=seal({"phase":"SAED_V4_39","baseline_id":v["baseline_id"],"baseline_hash":content_hash([x["baseline_decision"] for x in v["observations"]]),"baseline_preserved":True,"baseline_mutation_count":0,"fallback_mode":"BASELINE_OR_ABSTAIN","research_only":True},"v439_baseline","receipt_id","receipt_hash")
 release=seal({"phase":"SAED_V4_39","runtime_bundle_hash":up["bundle_hash"],"qualification_hash":qualification["qualification_hash"],"reference_paper_passed":qualification["stages"][0]["internal_reference_passed"],"reference_shadow_passed":qualification["stages"][1]["internal_reference_passed"],"actual_paper_passed":qualification["stages"][0]["actual_external_passed"],"actual_shadow_passed":qualification["stages"][1]["actual_external_passed"],"micro_live_eligible":qualification["micro_live_eligible"],"micro_live_authorized":False,"order_submission_allowed":False,"capital_activation_allowed":False,"production_authorized":False,"release_decision":"ACCEPT_REFERENCE_EXTERNAL_GATES_OPEN","research_only":True},"v439_release","release_id","release_hash")
 evidence_items={"upstream_receipt":up,"constitution":constitution,"authority_boundary":authority,"cohort":cohort,"observation_receipt":obs_receipt,"mode_ladder":ladder,"runtime_binding":runtime_binding,"broker_profile":broker,"risk_envelope":risk,"intent_ledger":intents_ledger,"paper_ledger":paper,"shadow_ledger":shadow,"reconciliation_ledger":recon,"surveillance_report":surv,"incident_runbook":runbook,"incident_drills":drills,"external_evidence_matrix":external,"broker_qualification_matrix":broker_matrix,"stage_qualification":qualification,"review_bundle":reviews,"baseline_receipt":baseline,"release_candidate":release}
 ev=evidence_bundle(evidence_items)
 cert=seal({"phase":"SAED_V4_39","status":"ACCEPTED_REFERENCE_EXTERNAL_GATES_OPEN","runtime_bundle_hash":up["bundle_hash"],"release_hash":release["release_hash"],"evidence_hash":ev["evidence_bundle_hash"],"reference_paper_passed":release["reference_paper_passed"],"reference_shadow_passed":release["reference_shadow_passed"],"actual_prospective_paper_passed":release["actual_paper_passed"],"actual_prospective_shadow_passed":release["actual_shadow_passed"],"micro_live_eligible":False,"micro_live_authorized":False,"order_submission_allowed":False,"capital_activation_allowed":False,"production_authorized":False,"next_phase":"SAED_V4_40","claim_ceiling":"synthetic prospective paper and shadow qualification reference; actual MetaEditor, terminal, broker, paper, shadow and micro-live evidence pending","research_only":True},"v439_certificate","certificate_id","certificate_hash")
 handoff=seal({"kind":"v4_39_handoff","phase":"SAED_V4_39","next_phase":"SAED_V4_40","certificate_hash":cert["certificate_hash"],"release_hash":release["release_hash"],"runtime_bundle_hash":up["bundle_hash"],"allowed_next_work":["context_fleet_control_plane","fleet_observability","fleet_rollout_simulation","external_gate_completion"],"forbidden_next_work":["capital_activation_without_authorization","live_order_submission_without_signed_permit","claiming_external_evidence_from_synthetic_fixture","silent_runtime_mutation"],"required_external_gates":[x["evidence_type"] for x in external["items"] if x["status"]=="PENDING_EXTERNAL"],"micro_live_authorized":False,"production_authorized":False,"research_only":True},"v439_handoff","handoff_id","handoff_hash")
 return {**evidence_items,"evidence_bundle":ev,"certificate":cert,"handoff":handoff}
