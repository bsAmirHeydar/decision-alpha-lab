from __future__ import annotations
from decimal import Decimal
from .canonical import stable_id,digest_object

def symbol_fixture(symbol:str="EURUSD")->dict:
    return {"symbol":symbol,"bid":"99.99","ask":"100.01","quote_age_ms":100,"max_quote_age_ms":1000,"max_spread":"0.05","tick_size":"0.01","volume_min":"0.01","volume_max":"100.00","volume_step":"0.01","stops_level":"0.05","freeze_level":"0.02","session_open":True,"reconciliation_ok":True,"kill_switch_active":False}

def build_request_case(package:dict)->dict:
    pid=package["treatment_package_id"];types=set(package.get("atom_types",[]));buy=int(pid[-1],16)%2==0;side="BUY" if buy else "SELL"
    entry_kind="MARKET" if "ENTRY_MARKET" in types else ("LIMIT" if "ENTRY_PRICE" in types else "UNSPECIFIED")
    entry_price=None if entry_kind=="MARKET" else ("100.00" if entry_kind=="LIMIT" else None)
    stop=None
    if "STOP_LOSS" in types:stop={"price":"99.00" if buy else "101.00","unit":"PRICE"}
    targets=[]
    if "TAKE_PROFIT" in types:targets=[{"price":"102.00" if buy else "98.00","unit":"PRICE","fraction":"1.0"}]
    volume={"value":"1.00","unit":"LOTS"} if "VOLUME_SIZING" in types else {"value":None,"unit":"UNKNOWN"}
    expiry={"kind":"TIME","value":"2099-01-01T00:00:00Z"} if "EXPIRY" in types or "TIME_EXIT" in types else None
    intent={"schema_version":"1.0.0","request_id":stable_id("DRYREQ",pid),"treatment_package_id":pid,"side":side,"symbol":"EURUSD","decision_time":"2000-01-01T00:00:00Z","availability_time":"2000-01-01T00:00:00Z","entry":{"kind":entry_kind,"price":entry_price,"unit":"PRICE" if entry_price else "UNKNOWN"},"stop":stop,"targets":targets,"volume_request":volume,"expiry":expiry,"cancellation":{"enabled":"CANCELLATION" in types},"management":{"trailing":"TRAILING" in types,"partial_exit":"PARTIAL_EXIT" in types},"source_evidence":package.get("source_digests",[]),"mode":"DRY_RUN"}
    case={"case_id":stable_id("DRYCASE",pid),"package_id":pid,"source_package_digest":package["package_digest"],"intent":intent,"symbol_fixture":symbol_fixture(),"expected_submission_count":0}
    case["case_digest"]=digest_object(case,"case_digest")
    return case
