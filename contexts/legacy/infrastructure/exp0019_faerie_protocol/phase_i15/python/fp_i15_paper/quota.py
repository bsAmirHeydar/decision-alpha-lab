from dataclasses import replace
from .contracts import *
from .canonical import *
from .errors import FPI15Error

class PaperQuotaStore:
    def __init__(self): self._records={}
    def get(self,key): return self._records.get(key,PaperQuotaRecord(key,QuotaState.AVAILABLE))
    def reserve(self,plan:ExecutionPlan,policy:PaperPolicyConfig):
        if policy.consume_event==PaperConsumeEvent.UNSET: raise FPI15Error("FP_PAPER_POLICY_UNSET","paper policy must be explicit")
        cur=self.get(plan.quota_key_id)
        if cur.state==QuotaState.RESERVED and cur.winner_signal_id==plan.signal_id: return cur
        if cur.state in (QuotaState.RESERVED,QuotaState.CONSUMED): raise FPI15Error("FP_PAPER_QUOTA_ALREADY_OWNED","quota already owned")
        rid=stable_id("FPPRES",{"quota":plan.quota_key_id,"signal":plan.signal_id,"plan":plan.plan_id,"generation":cur.generation+1,"policy":policy.policy_hash})
        rec=PaperQuotaRecord(plan.quota_key_id,QuotaState.RESERVED,plan.signal_id,plan.plan_id,rid,PaperConsumeEvent.UNSET,cur.generation+1,policy.policy_hash,("FP_PAPER_QUOTA_RESERVED",),"")
        rec=replace(rec,record_hash=sha256(rec))
        self._records[plan.quota_key_id]=rec
        return self.trigger(plan.quota_key_id,PaperConsumeEvent.PLAN_CREATED,policy,"FP_PAPER_PLAN_CREATED")
    def trigger(self,key,event:PaperConsumeEvent,policy:PaperPolicyConfig,reason=""):
        cur=self.get(key)
        if cur.state==QuotaState.CONSUMED: return cur
        if cur.state!=QuotaState.RESERVED: return cur
        if policy.consume_event==event:
            rec=replace(cur,state=QuotaState.CONSUMED,consumed_event=event,reason_codes=tuple(sorted(set(cur.reason_codes+("FP_PAPER_QUOTA_CONSUMED",reason)))),record_hash="")
            rec=replace(rec,record_hash=sha256(rec)); self._records[key]=rec; return rec
        return cur
    def release(self,key,policy:PaperPolicyConfig,reason_code:str):
        cur=self.get(key)
        if cur.state!=QuotaState.RESERVED: return cur
        if reason_code not in policy.releasable_reason_codes: return cur
        rec=replace(cur,state=QuotaState.RELEASED,reason_codes=tuple(sorted(set(cur.reason_codes+("FP_PAPER_QUOTA_RELEASED",reason_code)))),record_hash="")
        rec=replace(rec,record_hash=sha256(rec)); self._records[key]=rec; return rec
    def snapshot(self): return tuple(self._records[k] for k in sorted(self._records))
