from __future__ import annotations
from typing import Any
from .canonical import digest_object,stable_id
from .contracts import validate_package
from .errors import ContractError
from .expressions import evaluate_expression

class CanonicalSetupEvaluator:
    """Pure deterministic evaluator over a caller-supplied canonical Context snapshot.

    It owns no clock, I/O, drawing, broker or persistence surface.  Unknown or
    blocked contracts always produce a first-class BLOCKED abstention record.
    """
    def evaluate(self,package:dict[str,Any],snapshot:dict[str,Any],*,sequence:int=1,prior_state:dict[str,Any]|None=None)->dict[str,Any]:
        failures=validate_package(package)
        if failures:raise ContractError("LCM09B_PACKAGE_INVALID:"+",".join(failures))
        self._validate_snapshot(package,snapshot)
        if package["package_status"]=="REFERENCE_BLOCKED":
            return self._record(package,snapshot,sequence,"BLOCKED",package["reason_codes"]+ ["LCM09B_FAIL_CLOSED_BLOCKED_PACKAGE"],prior_state)
        env={"context":snapshot,"features":snapshot.get("features",{}),"prior_state":prior_state or {}}
        ordered=("cancellation","expiry","invalidation","confirmation","trigger","eligibility","abstention")
        state_map={"cancellation":"CANCELLED","expiry":"EXPIRED","invalidation":"INVALIDATED","confirmation":"CONFIRMED","trigger":"TRIGGERED","eligibility":"ELIGIBLE","abstention":"ABSTAINED"}
        for name in ordered:
            rule=package["rules"].get(name)
            if rule is not None and evaluate_expression(rule,env):
                return self._record(package,snapshot,sequence,state_map[name],[f"LCM09B_RULE_{name.upper()}_TRUE"],prior_state)
        return self._record(package,snapshot,sequence,"ABSTAINED",["LCM09B_NO_RULE_MATCH"],prior_state)
    def _validate_snapshot(self,package:dict[str,Any],snapshot:dict[str,Any])->None:
        required=("context_identity_id","context_version","occurrence_id","observed_at","available_at","known_time_complete","snapshot_digest")
        missing=[k for k in required if k not in snapshot]
        if missing:raise ContractError("LCM09B_CONTEXT_SNAPSHOT_MISSING:"+",".join(missing))
        binding=package["context_binding"]
        if binding["state"]=="BOUND" and snapshot["context_identity_id"] not in binding["allowed_context_identity_ids"]:raise ContractError("LCM09B_CONTEXT_BINDING_MISMATCH")
        if snapshot["known_time_complete"] is not True:raise ContractError("LCM09B_KNOWN_TIME_INCOMPLETE")
        if snapshot["available_at"]<snapshot["observed_at"]:raise ContractError("LCM09B_AVAILABILITY_PRECEDES_OBSERVATION")
    def _record(self,package,snapshot,sequence,state,reasons,prior_state):
        body={"schema_version":"1.0.0","decision_id":stable_id("SETUPDECISION",package["setup_id"],snapshot["occurrence_id"],sequence,state),"setup_id":package["setup_id"],"package_id":package["package_id"],"occurrence_id":snapshot["occurrence_id"],"context_identity_id":snapshot["context_identity_id"],"sequence":sequence,"decision_state":state,"reason_codes":sorted(set(reasons)),"observed_at":snapshot["observed_at"],"available_at":snapshot["available_at"],"prior_decision_digest":None if prior_state is None else prior_state.get("decision_digest"),"no_trade":state in {"ABSTAINED","BLOCKED","INVALIDATED","CANCELLED","EXPIRED"},"promotion_authority":False,"runtime_authority":False,"live_order_authority":False,"capital_authority":False}
        return {**body,"decision_digest":digest_object(body)}
