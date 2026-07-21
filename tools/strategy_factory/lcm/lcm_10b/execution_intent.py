from __future__ import annotations
from decimal import Decimal,InvalidOperation
from typing import Any
from .canonical import digest_object,stable_id
from .constants import CLAIM_CEILING,PRODUCER,TIME_SEMANTICS,OWNER,REVIEWER
from .models import Side,EntryKind,Finding

def _decimal(v:Any,field:str,findings:list[Finding])->str|None:
    if v is None:return None
    try:return format(Decimal(str(v)),"f")
    except (InvalidOperation,ValueError):findings.append(Finding("INVALID_DECIMAL",field,"Value is not a valid decimal"));return None

def validate_execution_intent(intent:dict[str,Any])->dict[str,Any]:
    findings=[]
    side=intent.get("side","UNKNOWN")
    if side not in {"BUY","SELL"}:findings.append(Finding("SIDE_REQUIRED","side","Side must be BUY or SELL"))
    symbol=intent.get("symbol")
    if not isinstance(symbol,str) or not symbol.strip():findings.append(Finding("SYMBOL_REQUIRED","symbol","Symbol must be explicit"))
    entry=intent.get("entry") or {};kind=entry.get("kind","UNSPECIFIED")
    if kind=="UNSPECIFIED":findings.append(Finding("ENTRY_KIND_REQUIRED","entry.kind","Missing entry kind never implies market"))
    if kind in {"LIMIT","STOP","STOP_LIMIT"} and entry.get("price") is None:findings.append(Finding("ENTRY_PRICE_REQUIRED","entry.price","Pending entry requires explicit price"))
    if kind=="MARKET" and entry.get("price") is not None:findings.append(Finding("MARKET_PRICE_MUST_BE_NULL","entry.price","Market intent must not smuggle a limit price"))
    ep=None
    try:ep=Decimal(str(entry.get("price"))) if entry.get("price") is not None else None
    except InvalidOperation:findings.append(Finding("INVALID_ENTRY_PRICE","entry.price","Invalid entry price"))
    stop=intent.get("stop") or {};sp=None
    try:sp=Decimal(str(stop.get("price"))) if stop.get("price") is not None else None
    except InvalidOperation:findings.append(Finding("INVALID_STOP_PRICE","stop.price","Invalid stop price"))
    if ep is not None and sp is not None:
        if side=="BUY" and sp>=ep:findings.append(Finding("BUY_STOP_NOT_BELOW_ENTRY","stop.price","BUY stop must be below explicit entry"))
        if side=="SELL" and sp<=ep:findings.append(Finding("SELL_STOP_NOT_ABOVE_ENTRY","stop.price","SELL stop must be above explicit entry"))
    for i,t in enumerate(intent.get("targets") or []):
        try:tp=Decimal(str(t.get("price")))
        except InvalidOperation:findings.append(Finding("INVALID_TARGET_PRICE",f"targets[{i}].price","Invalid target"));continue
        if ep is not None and side=="BUY" and tp<=ep:findings.append(Finding("BUY_TARGET_NOT_ABOVE_ENTRY",f"targets[{i}].price","BUY target must be above entry"))
        if ep is not None and side=="SELL" and tp>=ep:findings.append(Finding("SELL_TARGET_NOT_BELOW_ENTRY",f"targets[{i}].price","SELL target must be below entry"))
    if intent.get("submission_requested") is not False:findings.append(Finding("SUBMISSION_MUST_BE_FALSE","submission_requested","LCM-10B cannot request submission"))
    return {"passed":not any(x.blocking for x in findings),"finding_count":len(findings),"findings":[x.to_dict() for x in findings]}

def build_execution_intent(package:dict[str,Any],request:dict[str,Any])->dict[str,Any]:
    findings=[]
    side=str(request.get("side","UNKNOWN")).upper();kind=str((request.get("entry") or {}).get("kind","UNSPECIFIED")).upper()
    entry=request.get("entry") or {};stop=request.get("stop") or {};targets=request.get("targets") or []
    body={
      "schema_version":"1.0.0","intent_id":stable_id("EXECINTENT",package.get("treatment_package_id"),request.get("decision_id"),request.get("decision_time"),request.get("availability_time"),request.get("symbol"),side,kind),
      "treatment_package_id":package.get("treatment_package_id"),"treatment_version":package.get("treatment_version"),"decision_id":request.get("decision_id"),
      "side":side,"symbol":request.get("symbol"),"decision_time":request.get("decision_time"),"availability_time":request.get("availability_time"),
      "entry":{"kind":kind,"price":_decimal(entry.get("price"),"entry.price",findings),"price_unit":entry.get("price_unit","ABSOLUTE_PRICE"),"limit_price":_decimal(entry.get("limit_price"),"entry.limit_price",findings)},
      "stop":{"kind":stop.get("kind","NONE"),"price":_decimal(stop.get("price"),"stop.price",findings),"price_unit":stop.get("price_unit","ABSOLUTE_PRICE")},
      "targets":[{"target_id":str(t.get("target_id",i+1)),"price":_decimal(t.get("price"),f"targets[{i}].price",findings),"price_unit":t.get("price_unit","ABSOLUTE_PRICE"),"fraction":_decimal(t.get("fraction"),f"targets[{i}].fraction",findings)} for i,t in enumerate(targets)],
      "volume_request":{"mode":(request.get("volume_request") or {}).get("mode","UNSPECIFIED"),"value":_decimal((request.get("volume_request") or {}).get("value"),"volume_request.value",findings),"unit":(request.get("volume_request") or {}).get("unit","UNSPECIFIED")},
      "expiry":request.get("expiry") or {"mode":"NONE","time":None},"cancellation":request.get("cancellation") or {"mode":"NONE"},"management":request.get("management") or [],
      "source_evidence":sorted(set(request.get("source_evidence") or package.get("source_digests") or [])),"source_digests":sorted(set(request.get("source_evidence") or package.get("source_digests") or [])),"unsupported_fields":sorted(set(request.get("unsupported_fields") or [])),
      "rejection_reasons":[],"submission_requested":False,"adapter_mode":"DRY_RUN","claim_ceiling":CLAIM_CEILING,"producer":PRODUCER,"generated_at":None,"generated_time_semantics":TIME_SEMANTICS,"deterministic_identity":True,"owner":OWNER,"reviewer":REVIEWER,"validation_status":"PENDING"
    }
    pre={"passed":not findings,"findings":[x.to_dict() for x in findings]};v=validate_execution_intent(body);allf=pre["findings"]+v["findings"]
    body["rejection_reasons"]=[x["code"] for x in allf];body["validation_status"]="PASS" if not allf else "BLOCKED";body["intent_digest"]=digest_object(body,"intent_digest")
    return body
