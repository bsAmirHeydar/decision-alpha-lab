from __future__ import annotations
from collections import Counter, defaultdict
from datetime import datetime
from typing import Any
from .chain import build_chain, verify_chain
from .canonical import content_hash, stable_id
from .contracts import TRIAL_STATES, TERMINAL_STATES
from .errors import ContractError, StateTransitionError, IntegrityError

ALLOWED={
 None:{"proposed"},
 "proposed":{"compiled","duplicate","invalid","cancelled"},
 "compiled":{"running","duplicate","invalid","cancelled"},
 "running":{"pruned","failed","timed_out","cancelled","completed"},
 "completed":{"selected","rejected"},
}
REQ={"event_id","trial_id","experiment_id","family_id","state","actor_id","data_role","occurred_at","known_at","seed","attempt","retry_of","duplicate_of","reason","cost_units","metadata"}

def _time(v):
    return datetime.fromisoformat(str(v).replace("Z","+00:00"))

def build(raw_events:list[dict[str,Any]], manifests:list[dict[str,Any]], actors:set[str], policy, budget)->dict[str,Any]:
    expected={tid for m in manifests for tid in m["expected_trial_ids"]}; experiment_ids={m["experiment_id"] for m in manifests}; family_by_exp={m["experiment_id"]:m["family_id"] for m in manifests}
    if len(expected)>budget.maximum_trials: raise IntegrityError("trial universe exceeds global budget")
    prev_state={}; seen_event=set(); first_seen=set(); ordered=[]
    retry_edges={}; duplicate_edges={}
    for e in raw_events:
        if set(e)!=REQ: raise ContractError("trial event fields mismatch")
        if e["event_id"] in seen_event: raise IntegrityError("duplicate trial event id")
        seen_event.add(e["event_id"])
        if e["trial_id"] not in expected or e["experiment_id"] not in experiment_ids: raise IntegrityError("orphan trial event")
        if family_by_exp[e["experiment_id"]]!=e["family_id"]: raise IntegrityError("family mismatch")
        if e["actor_id"] not in actors: raise IntegrityError("unknown actor")
        if e["state"] not in TRIAL_STATES: raise StateTransitionError("unknown trial state")
        if e["data_role"] in {"hidden_evaluation","protected_final"}: raise IntegrityError("protected trial data role")
        if _time(e["known_at"])>_time(e["occurred_at"]): raise IntegrityError("trial known_at after occurred_at")
        prior=prev_state.get(e["trial_id"])
        if e["state"] not in ALLOWED.get(prior,set()): raise StateTransitionError(f"invalid transition {prior}->{e['state']}")
        if prior is None: first_seen.add(e["trial_id"])
        if e["state"]=="duplicate":
            if not e["duplicate_of"] or e["duplicate_of"]==e["trial_id"]: raise IntegrityError("invalid duplicate edge")
            duplicate_edges[e["trial_id"]]=e["duplicate_of"]
        if e["attempt"]>1:
            if not e["retry_of"] or e["retry_of"]==e["trial_id"]: raise IntegrityError("invalid retry edge")
            retry_edges[e["trial_id"]]=e["retry_of"]
        prev_state[e["trial_id"]]=e["state"]; ordered.append(dict(e))
    missing=sorted(expected-first_seen); orphan=sorted(first_seen-expected)
    nonterminal=sorted(t for t,s in prev_state.items() if s not in TERMINAL_STATES)
    if policy.orphan_runs_forbidden and (missing or orphan): raise IntegrityError("incomplete trial universe")
    if nonterminal: raise IntegrityError("nonterminal trials remain")
    for child,parent in {**retry_edges,**duplicate_edges}.items():
        if parent not in expected: raise IntegrityError("lineage edge points outside universe")
    chain=build_chain(ordered,"trial_ledger"); receipt=verify_chain(chain,"trial_ledger")
    counts=Counter(prev_state.values()); fam=Counter(e["family_id"] for e in ordered if e["state"]=="proposed")
    total_cost=sum(float(e["cost_units"]) for e in ordered)
    payload={"phase":"SAED_V4_27","entries":chain,"chain_receipt":receipt,"expected_trial_count":len(expected),"observed_trial_count":len(first_seen),"event_count":len(chain),"terminal_state_counts":dict(sorted(counts.items())),"family_trial_counts":dict(sorted(fam.items())),"retry_edges":dict(sorted(retry_edges.items())),"duplicate_edges":dict(sorted(duplicate_edges.items())),"missing_trial_ids":missing,"orphan_trial_ids":orphan,"nonterminal_trial_ids":nonterminal,"total_cost_units":total_cost,"complete":not(missing or orphan or nonterminal),"append_only":True,"hash_linked":True}
    payload["trial_ledger_id"]=stable_id("complete_trial_ledger",payload); payload["trial_ledger_hash"]=content_hash(payload)
    return payload
