from __future__ import annotations
from collections import Counter
from datetime import datetime
from typing import Any
from .chain import build_chain, verify_chain
from .canonical import content_hash, stable_id
from .contracts import EXPOSURE_TYPES
from .errors import ContractError, IntegrityError, BudgetExceededError
REQ={"event_id","actor_id","actor_type","data_role","exposure_type","object_type","object_id","object_hash","occurred_at","known_at","query_id","hypothesis_id","experiment_id","trial_id","purpose","manual","metadata"}

def _time(v): return datetime.fromisoformat(str(v).replace("Z","+00:00"))

def build(raw_events:list[dict[str,Any]], actors:dict[str,dict[str,Any]], roles:dict[str,dict[str,Any]], policy, budget)->dict[str,Any]:
    if len(raw_events)>budget.maximum_exposures: raise BudgetExceededError("exposure budget exceeded")
    seen=set(); dedup=set(); ordered=[]; duplicate_suppressed=0
    for e in raw_events:
        if set(e)!=REQ: raise ContractError("exposure event fields mismatch")
        if e["event_id"] in seen: raise IntegrityError("duplicate exposure event id")
        seen.add(e["event_id"])
        if e["actor_id"] not in actors or e["actor_type"]!=actors[e["actor_id"]]["actor_type"]: raise IntegrityError("actor mismatch")
        if e["data_role"] not in roles: raise IntegrityError("unknown data role")
        if e["exposure_type"] not in EXPOSURE_TYPES or e["exposure_type"] not in roles[e["data_role"]]["allowed_exposure_types"]: raise IntegrityError("exposure type not allowed for role")
        if _time(e["known_at"])>_time(e["occurred_at"]): raise IntegrityError("exposure known_at after occurred_at")
        if e["data_role"] in {"hidden_evaluation","protected_final"}: raise IntegrityError("protected evidence exposure forbidden")
        key=(e["actor_id"],e["data_role"],e["exposure_type"],e["object_hash"],e["query_id"],e["occurred_at"])
        if key in dedup:
            duplicate_suppressed+=1; continue
        dedup.add(key); ordered.append(dict(e))
    chain=build_chain(ordered,"exposure_ledger"); receipt=verify_chain(chain,"exposure_ledger")
    by_type=Counter(e["exposure_type"] for e in ordered); by_role=Counter(e["data_role"] for e in ordered); by_actor=Counter(e["actor_id"] for e in ordered)
    limits={"chart_render":budget.maximum_chart_renders,"metric_read":budget.maximum_metric_reads,"agent_summary":budget.maximum_agent_summaries,"row_export":budget.maximum_row_exports,"narrative_generated":budget.maximum_narratives,"hypothesis_modified":budget.maximum_hypothesis_modifications,"manual_intervention":budget.maximum_manual_interventions}
    exceeded={k:{"count":by_type.get(k,0),"limit":v} for k,v in limits.items() if by_type.get(k,0)>v}
    if exceeded: raise BudgetExceededError(f"exposure subtype budget exceeded: {exceeded}")
    payload={"phase":"SAED_V4_27","entries":chain,"chain_receipt":receipt,"event_count":len(chain),"duplicate_events_suppressed":duplicate_suppressed,"counts_by_type":dict(sorted(by_type.items())),"counts_by_data_role":dict(sorted(by_role.items())),"counts_by_actor":dict(sorted(by_actor.items())),"hidden_evaluation_queries":0,"protected_evidence_exposures":0,"runtime_compilations":0,"order_submissions":0,"online_policy_mutations":0,"network_requests":0,"complete":True,"append_only":True,"hash_linked":True}
    payload["exposure_ledger_id"]=stable_id("complete_exposure_ledger",payload); payload["exposure_ledger_hash"]=content_hash(payload)
    return payload
