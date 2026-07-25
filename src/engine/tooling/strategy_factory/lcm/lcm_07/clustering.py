from collections import defaultdict
from .canonical import content_id,digest_object,slug

def family(path):
    parts=path.split("/")
    for token in ("DayeTrader","FlagCountingPhoenix","IntermarketDivergenceExecution","IntermarketDivergence","M0001","M0002","M0003","M0004","M0005","Execution","Debug"):
        if token in parts or token in path:return token.upper()
    return (parts[2] if len(parts)>2 else "UNKNOWN").upper()
def category(members):
    text=" ".join(x["function_name"]+" "+x["artifact_path"] for x in members).lower()
    if any(x["flags"]["order_api"] for x in members): return "EXECUTION_SENSITIVE"
    if "closedcandle" in text or "newopen" in text or "newclosed" in text:return "CLOSED_BAR_CLOCK"
    if "timeconfig" in text or "timerange" in text or "newyork" in text or "timeframe" in text:return "TIME_SESSION_CONFIGURATION"
    if "format" in text:return "DETERMINISTIC_FORMATTING"
    if "hash" in text or "prefix" in text:return "IDENTITY_HASH"
    if any(x["flags"]["object_mutation_api"] for x in members):return "OBJECT_LIFECYCLE"
    if "shouldrun" in text or "allowed" in text:return "CONFIGURATION_GATE"
    if "stream" in text or "state" in text:return "STATE_STREAM"
    if "reference" in text or "lifecycle" in text:return "REFERENCE_LIFECYCLE"
    if "diverg" in text or "hunt" in text or "geometry" in text:return "DOMAIN_LOGIC"
    return "GENERIC_UTILITY"
def cluster(records):
    grouped=defaultdict(list)
    for r in records:grouped[r["normalized_body_sha256"]].append(r)
    out=[]
    for body_sha,members in sorted(grouped.items()):
        paths=sorted({x["artifact_path"] for x in members})
        if len(paths)<2:continue
        members=sorted(members,key=lambda x:(x["artifact_path"],x["line_start"],x["function_name"]))
        cats=category(members); signatures=sorted({(x["return_type"],tuple(x["parameter_types"])) for x in members})
        flags={k:any(x["flags"][k] for x in members) for k in members[0]["flags"]}
        cid=content_id("ENGCAND",{"body_sha":body_sha,"paths":paths})
        record={"schema_version":"1.0.0","candidate_id":cid,"category":cats,"normalized_body_sha256":body_sha,"consumer_count":len(members),"distinct_artifact_count":len(paths),"families":sorted({family(x["artifact_path"]) for x in members}),"signature_count":len(signatures),"signatures":[{"return_type":a,"parameter_types":list(b)} for a,b in signatures],"flags":flags,"members":members,"candidate_digest":None}
        record["candidate_digest"]=digest_object(record,"candidate_digest");out.append(record)
    out.sort(key=lambda x:(-x["distinct_artifact_count"],-x["consumer_count"],x["candidate_id"]))
    return out

def select(clusters,limit=14):
    desired=("CLOSED_BAR_CLOCK","TIME_SESSION_CONFIGURATION","DETERMINISTIC_FORMATTING","IDENTITY_HASH","OBJECT_LIFECYCLE","CONFIGURATION_GATE","STATE_STREAM","REFERENCE_LIFECYCLE","DOMAIN_LOGIC","EXECUTION_SENSITIVE","GENERIC_UTILITY")
    selected=[];seen=set()
    for cat in desired:
        for c in clusters:
            if c["category"]==cat and c["candidate_id"] not in seen:
                selected.append(c);seen.add(c["candidate_id"]);break
    for c in clusters:
        if len(selected)>=limit:break
        if c["candidate_id"] not in seen:selected.append(c);seen.add(c["candidate_id"])
    return selected
