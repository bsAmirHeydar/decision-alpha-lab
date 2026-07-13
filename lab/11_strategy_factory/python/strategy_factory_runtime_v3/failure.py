from __future__ import annotations
from .canonical import stable_id
from .contracts import *
from .enums import FailureCode

def qualify_failures(bundle_hash:str,*,artifact_hash_ok:bool=True,feature_order_ok:bool=True,context_fresh:bool=True,symbol_available:bool=True,inference_ok:bool=True,latency_ok:bool=True,queue_ok:bool=True,restart_reconciled:bool=True,kill_switch_safe:bool=True,signature_ok:bool=True,parity_ok:bool=True,created_at_ms:int=0)->RuntimeFailureReport:
    checks=[
      (FailureCode.CORRUPT_ARTIFACT,artifact_hash_ok,'quarantine_bundle'),(FailureCode.FEATURE_ORDER_MISMATCH,feature_order_ok,'refuse_activation'),(FailureCode.STALE_CONTEXT,context_fresh,'abstain'),(FailureCode.SYMBOL_UNAVAILABLE,symbol_available,'abstain'),(FailureCode.INFERENCE_FAILURE,inference_ok,'fallback_manual_or_abstain'),(FailureCode.LATENCY_BREACH,latency_ok,'abstain_and_alert'),(FailureCode.QUEUE_PRESSURE,queue_ok,'shed_load'),(FailureCode.RESTART_RECONCILIATION,restart_reconciled,'block_activation'),(FailureCode.KILL_SWITCH,kill_switch_safe,'reject'),(FailureCode.SIGNATURE_FAILURE,signature_ok,'refuse_activation'),(FailureCode.PARITY_FAILURE,parity_ok,'refuse_activation')]
    findings=[]
    critical={FailureCode.CORRUPT_ARTIFACT,FailureCode.FEATURE_ORDER_MISMATCH,FailureCode.RESTART_RECONCILIATION,FailureCode.SIGNATURE_FAILURE,FailureCode.PARITY_FAILURE,FailureCode.KILL_SWITCH}
    for code,ok,disp in checks:findings.append(FailureFinding(code,'critical' if code in critical else 'warning',not ok,disp,{'check_passed':ok}))
    passed=not any(f.detected and f.severity=='critical' for f in findings)
    return RuntimeFailureReport(stable_id('runtime_failure_report',{'bundle':bundle_hash,'findings':[(f.code.value,f.detected) for f in findings]}),bundle_hash,tuple(findings),passed,created_at_ms)
