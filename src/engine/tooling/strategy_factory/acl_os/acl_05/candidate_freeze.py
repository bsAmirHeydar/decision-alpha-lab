from __future__ import annotations
from typing import Any
from .canonical import digest_object, stable_id, with_digest
from .errors import ContractError, MutationError
from .policies import DIAGNOSTIC_STATUS, ELIGIBLE_STATUS

def freeze_candidates(candidates: list[dict[str,Any]], request: dict[str,Any]) -> dict[str,Any]:
    by_id={c["setup_id"]:c for c in candidates}
    selection=request["candidate_selection"]
    if selection["mode"]=="ALL_CANONICAL": selected=list(by_id)
    else:
        selected=selection["setup_ids"]
        if len(selected)!=len(set(selected)) or not set(selected).issubset(by_id): raise ContractError("explicit setup selection invalid")
    research=[]; diagnostic=[]
    for sid in sorted(selected):
        c=by_id[sid]
        ref={"setup_id":sid,"candidate_id":c["candidate_id"],"candidate_digest":c["candidate_digest"],"behavior_digest":c["behavior_digest"],"origin":c["origin"],"status":c["status"],"payload_mutable":False}
        if c["status"]==ELIGIBLE_STATUS: research.append(ref)
        elif c["status"]==DIAGNOSTIC_STATUS:
            if request["diagnostic_policy"]=="SEGREGATE_AND_INCLUDE": diagnostic.append(ref)
        else: raise ContractError(f"candidate status not batchable: {c['status']}")
    if not research: raise ContractError("research candidate set cannot be empty")
    if any(r["setup_id"] in {d["setup_id"] for d in diagnostic} for r in research): raise MutationError("diagnostic/research overlap")
    body={"schema_version":"1.0.0","freeze_id":stable_id("CANDIDATE_FREEZE",request["batch_key"],digest_object(research),digest_object(diagnostic)),"selection_mode":selection["mode"],"research_candidates":research,"diagnostic_candidates":diagnostic,"research_count":len(research),"diagnostic_count":len(diagnostic),"candidate_payloads_mutable":False,"diagnostic_candidates_selectable":False}
    return with_digest(body,"candidate_freeze_digest")

def freeze_search_space(exposure: dict[str,Any],dedup: dict[str,Any],candidate_freeze: dict[str,Any]) -> dict[str,Any]:
    body={"schema_version":"1.0.0","search_exposure_ledger_digest":exposure["ledger_digest"],"deduplication_report_digest":dedup["report_digest"],"candidate_freeze_digest":candidate_freeze["candidate_freeze_digest"],"source_materialized_count":exposure["total_materialized"],"canonical_count":dedup["canonical_count"],"new_candidate_generation_allowed":False,"search_authority_broadening_allowed":False,"candidate_repair_allowed":False,"frozen":True}
    return with_digest(body,"search_space_freeze_digest")
