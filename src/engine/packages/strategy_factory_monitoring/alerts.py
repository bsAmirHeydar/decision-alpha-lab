from __future__ import annotations
from dataclasses import dataclass
from .enums import AlertState,Severity
from .hashing import stable_id
from .models import AlertEvent,AlertPolicy

@dataclass
class _Runtime:
    state:AlertState=AlertState.CLEAR
    breach_count:int=0
    recovery_count:int=0
    occurrence:int=0
    last_emit_ms:int=-1
    severity:Severity=Severity.INFO

class AlertEngine:
    def __init__(self,policies:tuple[AlertPolicy,...]):
        if len({p.policy_id for p in policies})!=len(policies):raise ValueError("duplicate alert policy")
        self.policies={p.metric_name:p for p in policies};self.runtime={p.policy_id:_Runtime() for p in policies}
    @staticmethod
    def _severity(p:AlertPolicy,value:float)->Severity:
        x=abs(value) if p.comparison=="ABS_HIGH" else value
        if p.comparison=="LOW":
            if x<=p.critical_threshold:return Severity.CRITICAL
            if x<=p.warning_threshold:return Severity.WARNING
        else:
            if x>=p.critical_threshold:return Severity.CRITICAL
            if x>=p.warning_threshold:return Severity.WARNING
        return Severity.INFO
    def observe(self,metric_name:str,value:float,known_time_ms:int,correlation_id:str)->tuple[AlertEvent,...]:
        p=self.policies.get(metric_name)
        if p is None:return ()
        rt=self.runtime[p.policy_id];sev=self._severity(p,value);breach=sev!=Severity.INFO;out=[]
        if breach:
            rt.breach_count+=1;rt.recovery_count=0
            if rt.state in {AlertState.CLEAR,AlertState.RECOVERING}:rt.state=AlertState.PENDING
            should_fire=rt.breach_count>=p.consecutive_breaches
            escalation=rt.state==AlertState.FIRING and list(Severity).index(sev)>list(Severity).index(rt.severity)
            reminder=rt.state==AlertState.FIRING and rt.last_emit_ms>=0 and known_time_ms-rt.last_emit_ms>=p.reminder_ms
            cooldown_ok=rt.last_emit_ms<0 or known_time_ms-rt.last_emit_ms>=p.cooldown_ms
            if should_fire and (rt.state!=AlertState.FIRING or escalation or reminder) and cooldown_ok:
                rt.state=AlertState.FIRING;rt.occurrence+=1;rt.last_emit_ms=known_time_ms;rt.severity=sev
                threshold=p.critical_threshold if sev==Severity.CRITICAL else p.warning_threshold
                aid=stable_id("sf19-alert",p.policy_id,rt.occurrence,known_time_ms,sev.value)
                out.append(AlertEvent(aid,p.policy_id,metric_name,rt.state,sev,value,threshold,known_time_ms,rt.occurrence,correlation_id,f"{metric_name} breached {sev.value}"))
        else:
            rt.breach_count=0
            if rt.state==AlertState.FIRING:
                rt.state=AlertState.RECOVERING;rt.recovery_count=1
            elif rt.state==AlertState.RECOVERING:rt.recovery_count+=1
            elif rt.state==AlertState.PENDING:rt.state=AlertState.CLEAR;rt.recovery_count=0
            if rt.state==AlertState.RECOVERING and rt.recovery_count>=p.consecutive_recoveries:
                rt.state=AlertState.CLEAR;rt.occurrence+=1;rt.last_emit_ms=known_time_ms;rt.severity=Severity.INFO
                aid=stable_id("sf19-alert-recovery",p.policy_id,rt.occurrence,known_time_ms)
                out.append(AlertEvent(aid,p.policy_id,metric_name,AlertState.CLEAR,Severity.INFO,value,p.warning_threshold,known_time_ms,rt.occurrence,correlation_id,f"{metric_name} recovered"))
        return tuple(out)
    def active(self)->tuple[tuple[str,Severity],...]:
        return tuple((pid,rt.severity) for pid,rt in self.runtime.items() if rt.state==AlertState.FIRING)
