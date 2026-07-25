from __future__ import annotations
from .models import *
from .enums import *
from .retcodes import retcode_is_success
from .safety import KillSwitch, CircuitBreaker, preflight_reason
from .ledger import AppendOnlyLiveLedger
from .hashing import stable_id, cfloat, cbool

class LiveExecutionCoordinator:
    """Fail-closed coordinator around a broker port.

    The Python implementation is a conformance mirror only. A real broker port is deliberately
    absent. Live authority exists only in the isolated MQL5 adapter.
    """
    def __init__(self, run_id: str, mode: LiveMode, release: MicroLiveRelease,
            authorization: LiveAuthorization, policy: LiveSafetyPolicy, broker: BrokerPort,
            *, magic_number: int = 180018, maximum_ledger_records: int = 4096) -> None:
        if not run_id: raise ValueError("run_id")
        release.validate(); authorization.validate(); policy.validate()
        if authorization.release_hash!=release.derived_hash(): raise ValueError("authorization release mismatch")
        self.run_id=run_id; self.mode=mode; self.release=release; self.authorization=authorization
        self.policy=policy; self.broker=broker; self.magic_number=magic_number
        self.kill_switch=KillSwitch(); self.circuit=CircuitBreaker(policy.maximum_consecutive_failures,
            policy.cooldown_after_failure_milliseconds)
        self.ledger=AppendOnlyLiveLedger(maximum_ledger_records)
        self.intent_hashes: dict[str,str]={}; self.decisions: dict[str,LiveDecisionRecord]={}
        self.authorization_state=AuthorizationState.ARMED if mode==LiveMode.DRY_RUN else AuthorizationState.LOCKED
        self.session_orders=0; self.intents_received=0; self.preflight_passed=0; self.rejected=0
        self.checks_accepted=0; self.sends_attempted=0; self.sends_accepted=0

    def arm_micro_live(self, now_utc_msc: int) -> bool:
        if self.mode!=LiveMode.MICRO_LIVE: return False
        if now_utc_msc>self.authorization.expires_at_utc_msc: self.authorization_state=AuthorizationState.EXPIRED; return False
        if not self.kill_switch.disarm(self.authorization,now_utc_msc): return False
        self.authorization_state=AuthorizationState.ARMED
        self.ledger.append(LiveTransactionType.KILL_SWITCH_DISARMED,self.authorization.authorization_id,
            now_utc_msc,self.authorization.derived_hash(),"micro-live authorization armed")
        return True

    def engage_kill_switch(self, reason: str, now_utc_msc: int) -> None:
        self.kill_switch.engage(reason,now_utc_msc); self.authorization_state=AuthorizationState.REVOKED
        self.ledger.append(LiveTransactionType.KILL_SWITCH_ENGAGED,self.run_id,now_utc_msc,
            stable_id("ksw",reason),reason)

    def _decision(self, intent: ExecutionIntentRecord, decision: LiveDecision, reason: LiveRejectReason,
                  now: int, request_id: str = "", message: str = "") -> LiveDecisionRecord:
        canonical="|".join((intent.intent_id,str(int(decision)),str(int(reason)),request_id,
            self.authorization.authorization_id,self.release.derived_hash(),str(now),message))
        did=stable_id("ldec",canonical); row=LiveDecisionRecord(did,intent.intent_id,decision,reason,request_id,
            self.authorization.authorization_id,self.release.derived_hash(),now,message,did)
        self.decisions[intent.intent_id]=row; return row

    def _request(self, intent: ExecutionIntentRecord) -> NormalizedBrokerRequest:
        canonical="|".join((self.run_id,intent.intent_id,intent.intent_hash,str(int(BrokerAction.OPEN)),intent.symbol,
            str(intent.direction),str(int(intent.order_kind)),cfloat(intent.volume),cfloat(intent.entry_price),
            cfloat(intent.stop_price),cfloat(intent.target_price),cbool(intent.has_target),
            str(self.policy.maximum_deviation_points),str(self.magic_number),str(intent.expires_at_utc_msc)))
        rid=stable_id("lreq",canonical)
        return NormalizedBrokerRequest(rid,intent.intent_id,intent.intent_hash,BrokerAction.OPEN,intent.symbol,
            intent.direction,intent.order_kind,intent.volume,intent.entry_price,intent.stop_price,intent.target_price,
            intent.has_target,self.policy.maximum_deviation_points,self.magic_number,intent.expires_at_utc_msc,rid)

    def submit(self, intent: ExecutionIntentRecord, account: AccountGuardSnapshot,
               quote: QuoteSnapshot, now_utc_msc: int) -> LiveDecisionRecord:
        self.intents_received+=1
        self.ledger.append(LiveTransactionType.INTENT_RECEIVED,intent.intent_id,now_utc_msc,
            getattr(intent,"intent_hash","invalid"),"live intent received")
        if intent.intent_id in self.intent_hashes:
            if self.intent_hashes[intent.intent_id]!=intent.intent_hash:
                self.rejected+=1
                row=self._decision(intent,LiveDecision.REJECT,LiveRejectReason.DUPLICATE_HASH_CONFLICT,now_utc_msc,message="duplicate hash conflict")
                self.ledger.append(LiveTransactionType.PREFLIGHT_REJECTED,intent.intent_id,now_utc_msc,row.decision_hash,row.message); return row
            prior=self.decisions[intent.intent_id]
            return LiveDecisionRecord(prior.decision_id,prior.intent_id,prior.decision,LiveRejectReason.IDEMPOTENT_REPLAY,
                prior.request_id,prior.authorization_id,prior.release_hash,now_utc_msc,"idempotent replay",prior.decision_hash)
        self.intent_hashes[intent.intent_id]=intent.intent_hash
        if self.authorization_state!=AuthorizationState.ARMED:
            reason=LiveRejectReason.AUTHORIZATION_CONSUMED if self.authorization_state==AuthorizationState.CONSUMED else LiveRejectReason.AUTHORIZATION_MISSING
        else:
            reason=preflight_reason(mode=self.mode,intent=intent,release=self.release,authorization=self.authorization,
                policy=self.policy,account=account,quote=quote,now_utc_msc=now_utc_msc,session_orders=self.session_orders,
                kill_switch=self.kill_switch,circuit=self.circuit)
        if reason!=LiveRejectReason.NONE:
            self.rejected+=1; row=self._decision(intent,LiveDecision.REJECT,reason,now_utc_msc,message=reason.name.lower())
            self.ledger.append(LiveTransactionType.PREFLIGHT_REJECTED,intent.intent_id,now_utc_msc,row.decision_hash,row.message)
            return row
        self.preflight_passed+=1; request=self._request(intent)
        self.ledger.append(LiveTransactionType.PREFLIGHT_PASSED,intent.intent_id,now_utc_msc,request.request_hash,"preflight passed")
        self.ledger.append(LiveTransactionType.ORDER_CHECK_REQUESTED,request.request_id,now_utc_msc,request.request_hash,"broker check requested")
        check=self.broker.check(request,now_utc_msc)
        if not check.api_ok or not retcode_is_success(check.retcode):
            self.rejected+=1; opened=self.circuit.record_failure(f"check:{check.retcode}",now_utc_msc)
            self.ledger.append(LiveTransactionType.ORDER_CHECK_REJECTED,request.request_id,now_utc_msc,check.result_hash,"broker check rejected")
            if opened: self.ledger.append(LiveTransactionType.CIRCUIT_OPENED,self.run_id,now_utc_msc,check.result_hash,"circuit opened after check")
            return self._decision(intent,LiveDecision.REJECT,LiveRejectReason.ORDER_CHECK_REJECTED,now_utc_msc,request.request_id,"order check rejected")
        self.checks_accepted+=1; self.ledger.append(LiveTransactionType.ORDER_CHECK_ACCEPTED,request.request_id,now_utc_msc,check.result_hash,"broker check accepted")
        if self.mode==LiveMode.DRY_RUN:
            self.circuit.record_success()
            return self._decision(intent,LiveDecision.CHECK_ONLY,LiveRejectReason.NONE,now_utc_msc,request.request_id,"dry-run check accepted")
        self.sends_attempted+=1; self.ledger.append(LiveTransactionType.ORDER_SEND_REQUESTED,request.request_id,now_utc_msc,request.request_hash,"broker send requested")
        send=self.broker.send(request,now_utc_msc)
        if not send.api_ok or not retcode_is_success(send.retcode):
            self.rejected+=1; opened=self.circuit.record_failure(f"send:{send.retcode}",now_utc_msc)
            self.ledger.append(LiveTransactionType.ORDER_SEND_REJECTED,request.request_id,now_utc_msc,send.result_hash,"broker send rejected")
            if opened: self.ledger.append(LiveTransactionType.CIRCUIT_OPENED,self.run_id,now_utc_msc,send.result_hash,"circuit opened after send")
            return self._decision(intent,LiveDecision.REJECT,LiveRejectReason.BROKER_RETCODE_REJECTED,now_utc_msc,request.request_id,"order send rejected")
        self.sends_accepted+=1; self.session_orders+=1; self.circuit.record_success()
        self.ledger.append(LiveTransactionType.ORDER_SEND_ACCEPTED,request.request_id,now_utc_msc,send.result_hash,"broker send accepted")
        if self.policy.one_shot_authorization:
            self.authorization_state=AuthorizationState.CONSUMED
            self.ledger.append(LiveTransactionType.AUTHORIZATION_CONSUMED,self.authorization.authorization_id,
                now_utc_msc,self.authorization.derived_hash(),"one-shot authorization consumed")
        return self._decision(intent,LiveDecision.ACCEPTED,LiveRejectReason.NONE,now_utc_msc,request.request_id,"broker accepted request")

    def report(self, now_utc_msc: int) -> LiveExecutionReport:
        canonical="|".join((self.run_id,str(int(self.mode)),str(self.intents_received),str(self.preflight_passed),
            str(self.rejected),str(self.checks_accepted),str(self.sends_attempted),str(self.sends_accepted),
            str(self.session_orders),str(self.circuit.consecutive_failures),str(int(self.circuit.state)),
            str(int(self.kill_switch.state)),self.ledger.tail_hash,str(now_utc_msc)))
        rid=stable_id("lrpt",canonical)
        return LiveExecutionReport(rid,self.run_id,self.mode,self.intents_received,self.preflight_passed,self.rejected,
            self.checks_accepted,self.sends_attempted,self.sends_accepted,self.session_orders,
            self.circuit.consecutive_failures,self.circuit.state,self.kill_switch.state,self.ledger.tail_hash,
            now_utc_msc,rid)
