from __future__ import annotations
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from .canonical import content_id, digest_object, file_digest
from .constants import *
from .io import load_json, load_jsonl

_SUPPORT_NAMES = re.compile(r"(?:^|_)(?:validate|validator|test|selftest|audit|types?|contracts?|display|renderer|render|store|events?|identity|ledger|journal|config|schema|report|writer|reader|adapter)(?:_|$)", re.I)
_CHART_RE = re.compile(r"Chart(?:ID|First|Next|Get|Set|Redraw)|ChartsTotal|CHART_", re.I)
_BROKER_RE = re.compile(r"(?:CTrade|MqlTradeRequest|OrderSend|PositionOpen|PositionModify|PositionClose|trade\.(?:Buy|Sell)|SymbolInfoTick)", re.I)
_FUTURE_RE = re.compile(r"(?:lookahead|future[_ -]?derived|shift\s*=\s*0|\[\s*0\s*\]|current\s*bar)", re.I)


def _by(rows, key):
    return {row[key]: row for row in rows if row.get(key) is not None}


def _granularity(path: str, identity: dict) -> str:
    low = path.lower()
    name = Path(path).stem
    if identity.get("protected_platform_asset") or "/contexts/" in low and "lab/11_strategy_factory/contexts/" in low:
        return "CANONICAL_CONTEXT_REFERENCE"
    if low.startswith("docs/"):
        return "CONTEXT_DOCUMENTATION_PROJECTION"
    if "/tests/" in low or "/tools/" in low or name.lower().startswith(("test_", "validate_")):
        return "CONTEXT_TEST_OR_VALIDATOR"
    if low.endswith("/experiment.py") or (low.startswith("lab/03_experiments/") and Path(path).name == "experiment.py"):
        return "PACKAGE_CONTEXT"
    if low.endswith(".mq5") and ("/experts/" in low or "/indicators/" in low):
        return "COMPOSITE_CONTEXT_SHELL"
    if low.endswith(".mqh") or _SUPPORT_NAMES.search(name):
        return "EMBEDDED_CONTEXT_FRAGMENT"
    if low.endswith(".py") and ("/contexts/" in low or name.lower() in {"context", "engine"}):
        return "PACKAGE_CONTEXT"
    return "AMBIGUOUS_CONTEXT_LIKE"


def _family_wave(family: str, risk_class: str, granularity: str) -> str:
    if granularity in {"CONTEXT_DOCUMENTATION_PROJECTION", "CONTEXT_TEST_OR_VALIDATOR", "AMBIGUOUS_CONTEXT_LIKE"}:
        return "BLOCKED_UNRESOLVED"
    if family.startswith("M000"):
        return "WAVE_02_M_SERIES"
    if family in {"EXP0015_INTERMARKET_TIME", "EXP0016_INTERMARKET_EXECUTION", "EXP0017_CYCLE_GROUP"}:
        return "WAVE_03_EXP0015_EXP0016_EXP0017"
    if family == "EXP0018_DAYE_TRADER":
        return "WAVE_04_EXP0018_DAYE_TRADER"
    if family == "EXP0019_FAERIE_PROTOCOL":
        return "WAVE_05_EXP0019_FAERIE_PROTOCOL"
    if family == "FLAG_COUNTING_NDS_HOOK_ZONE":
        return "WAVE_09_HIGH_RISK_COMPOSITE"
    if "HOOK" in family:
        return "WAVE_07_HOOK"
    if "NDS" in family:
        return "WAVE_08_NDS"
    if risk_class in {"CRITICAL", "HIGH", "UNKNOWN"}:
        return "WAVE_09_HIGH_RISK_COMPOSITE"
    return "WAVE_01_LOW_RISK_PILOT"


def _doc_evidence(root: Path, source_path: str) -> list[str]:
    source = root / source_path
    evidence=[]
    parent=source.parent
    for name in ("README.md","metadata.yaml","metadata.yml","context.yaml","context_manifest.yaml"):
        p=parent/name
        if p.is_file(): evidence.append(p.relative_to(root).as_posix())
    return sorted(evidence)


def _package_file_count(root: Path, source_path: str) -> int:
    parent=(root/source_path).parent
    try: return sum(1 for p in parent.rglob('*') if p.is_file())
    except OSError: return 0


def _read_source(root: Path, path: str) -> str:
    try: return (root/path).read_text(encoding='utf-8',errors='ignore')
    except OSError: return ''


def _risk(identity, profile, packet, classification, granularity, duplicate_count, source_text, dependency_count, package_file_count):
    caps=profile.get("capabilities",{})
    flags={
        "statefulness": bool(caps.get("global_state") or re.search(r"\bstatic\b|global variable|state machine", source_text, re.I)),
        "multi_timeframe": bool(caps.get("timeframe_api") or re.search(r"PERIOD_|timeframe", source_text, re.I)),
        "session_dst": bool(caps.get("session_api") or caps.get("wall_clock") or re.search(r"session|timezone|DST|New York", source_text, re.I)),
        "persistence_file_io": bool(caps.get("file_io")),
        "drawing": bool(caps.get("drawing_api") or re.search(r"ObjectCreate|ObjectSet|ChartRedraw", source_text)),
        "multi_chart": bool(_CHART_RE.search(source_text)),
        "execution": bool(caps.get("order_api") or _BROKER_RE.search(source_text)),
        "broker_network": bool(caps.get("network_api") or caps.get("dynamic_exec")),
        "future_current_bar": bool(caps.get("current_bar") or caps.get("dynamic_exec") or _FUTURE_RE.search(source_text)),
        "nondeterminism": bool(caps.get("randomness")),
        "security": bool(identity.get("security_sensitive") or classification.get("security_sensitive")),
        "identity_ambiguity": bool(duplicate_count > 1 or identity.get("identity_status") not in {"PROVISIONAL_UNMERGED_IDENTITY_CANDIDATE","CANONICAL_IDENTITY"}),
        "owner_pending": identity.get("owner_resolution_status") != "HUMAN_APPROVED",
        "characterization_gap": not bool(packet.get("observed_behavior_captured")),
    }
    dimensions=[]
    weighted={
        "STATEFULNESS":12 if flags["statefulness"] else 0,
        "MULTI_TIMEFRAME_ALIGNMENT":12 if flags["multi_timeframe"] else 0,
        "SESSION_DST_DEPENDENCE":12 if flags["session_dst"] else 0,
        "PERSISTENCE_FILE_IO":10 if flags["persistence_file_io"] else 0,
        "DRAWING_OBJECT_LIFECYCLE":8 if flags["drawing"] else 0,
        "MULTI_CHART_BEHAVIOR":10 if flags["multi_chart"] else 0,
        "EXECUTION_COUPLING":100 if flags["execution"] else 0,
        "BROKER_OR_NETWORK_COUPLING":100 if flags["broker_network"] else 0,
        "CURRENT_BAR_OR_FUTURE_AWARENESS":80 if flags["future_current_bar"] else 0,
        "NONDETERMINISM":80 if flags["nondeterminism"] else 0,
        "SECURITY_SENSITIVITY":100 if flags["security"] else 0,
        "IDENTITY_AMBIGUITY":100 if flags["identity_ambiguity"] else 0,
        "OWNER_APPROVAL":20 if flags["owner_pending"] else 0,
        "CHARACTERIZATION_GAP":15 if flags["characterization_gap"] else 0,
        "PACKAGE_SURFACE_COMPLEXITY": min(10, max(0, profile.get("line_count",0)//250) + min(5, dependency_count//20) + min(5, package_file_count//20)),
    }
    critical_ids={"EXECUTION_COUPLING","BROKER_OR_NETWORK_COUPLING","CURRENT_BAR_OR_FUTURE_AWARENESS","NONDETERMINISM","SECURITY_SENSITIVITY","IDENTITY_AMBIGUITY"}
    for key,value in weighted.items():
        dimensions.append({"dimension_id":key,"score":value,"critical":key in critical_ids,"evidence_present":value>0})
    critical=[d["dimension_id"] for d in dimensions if d["critical"] and d["evidence_present"]]
    total=sum(min(d["score"],20) if d["critical"] else d["score"] for d in dimensions)
    if critical: risk_class="CRITICAL"
    elif not profile or not profile.get("file_exists") or granularity == "AMBIGUOUS_CONTEXT_LIKE": risk_class="UNKNOWN"
    elif total >= 55: risk_class="HIGH"
    elif total >= 20: risk_class="MODERATE"
    else: risk_class="LOW"
    return dimensions, critical, total, risk_class, flags


def build(upstream: dict):
    root=upstream["root"]; paths=upstream["paths"]
    identities=[x for x in load_jsonl(paths["identity_candidates"]) if x.get("identity_kind")=="CONTEXT"]
    profiles=_by(load_jsonl(paths["static_profiles"]),"identity_id")
    packets=_by(load_jsonl(paths["characterization_packets"]),"identity_id")
    classifications=_by(load_jsonl(paths["classification_records"]),"classification_id")
    targets=_by(load_jsonl(paths["identity_target_map"]),"identity_id")
    owner_registry=load_json(paths["owner_registry"])
    owner_roles={r["role_id"]:r for r in owner_registry.get("roles",[])}
    ambiguities=load_jsonl(paths["identity_ambiguities"])
    ambiguous_ids={x.get("identity_id") for x in ambiguities if x.get("identity_id")}
    digest_counts=Counter(x.get("source_artifact_sha256") for x in identities)
    candidate_paths={x["source_artifact_path"] for x in identities}
    dep_counts=Counter(); incoming_counts=Counter(); dep_rows=[]
    with paths["dependency_edges"].open("r",encoding="utf-8-sig",newline="") as handle:
        for row in csv.DictReader(handle):
            src=row.get("source_path",""); dst=row.get("resolved_path","")
            if src in candidate_paths:
                dep_counts[src]+=1
                dep_rows.append(row)
            if dst in candidate_paths:
                incoming_counts[dst]+=1
                dep_rows.append(row)
    shared_by_path=defaultdict(list)
    for cluster in load_jsonl(paths["shared_candidates"]):
        for member in cluster.get("members",[]):
            shared_by_path[member.get("artifact_path")].append(cluster["candidate_id"])
    records=[]; unresolved=[]
    for identity in sorted(identities,key=lambda x:x["identity_id"]):
        iid=identity["identity_id"]; path=identity["source_artifact_path"]
        profile=profiles.get(iid,{}) ; packet=packets.get(iid,{}) ; classification=classifications.get(identity.get("source_classification_id"),{}) ; target=targets.get(iid,{})
        text=_read_source(root,path); granularity=_granularity(path,identity); docs=_doc_evidence(root,path); pcount=_package_file_count(root,path)
        dims,critical,total,risk,flags=_risk(identity,profile,packet,classification,granularity,digest_counts[identity.get("source_artifact_sha256")],text,dep_counts[path],pcount)
        owner_role=owner_roles.get(identity.get("semantic_owner_role"),{})
        identity_collision=identity.get("source_artifact_sha256") in {k for k,v in digest_counts.items() if v>1} or iid in ambiguous_ids
        rec={
          "schema_version":"1.0.0","portfolio_record_id":content_id("CTXPORTREC",iid),"identity_id":iid,"identity_digest":identity.get("identity_digest"),"family_candidate":identity.get("family_candidate"),"semantic_name_candidate":identity.get("semantic_name_candidate"),"source_artifact_path":path,"source_artifact_sha256":identity.get("source_artifact_sha256"),"source_exists":bool(profile.get("file_exists") and (root/path).is_file()),"source_language":"MQL5" if path.lower().endswith((".mq5",".mqh")) else "PYTHON" if path.lower().endswith(".py") else "OTHER","granularity_class":granularity,"identity_status":identity.get("identity_status"),"identity_collision":identity_collision,"protected_platform_asset":bool(identity.get("protected_platform_asset")),"security_sensitive":bool(identity.get("security_sensitive")),"owner_state":{"semantic_owner_role":identity.get("semantic_owner_role"),"code_owner_role":identity.get("code_owner_role"),"role_binding_exists":bool(owner_role),"human_assignee_status":owner_role.get("assignment_status","UNKNOWN"),"architect_pilot_scope_approval":iid==PILOT_IDENTITY_ID},"characterization_state":{"packet_id":packet.get("packet_id"),"packet_status":packet.get("packet_status","UNKNOWN"),"observed_behavior_captured":bool(packet.get("observed_behavior_captured")),"required_case_types":packet.get("required_case_types",[])},"static_profile":{"line_count":profile.get("line_count",0),"function_count_estimate":profile.get("function_count_estimate",0),"dependency_count":dep_counts[path],"incoming_consumer_count":incoming_counts[path],"package_file_count":pcount,"capabilities":profile.get("capabilities",{})},"documentation_evidence":docs,"shared_engine_candidate_ids":sorted(set(shared_by_path.get(path,[]))),"target_path_proposal":target.get("target_package_root") or target.get("target_path"),"target_materialized":bool(target.get("canonical_path_materialized",False)),"risk_dimensions":dims,"critical_dimensions":critical,"aggregate_risk_score":total,"risk_class":risk,"wave_assignment":None,"pilot_eligibility":None,"record_digest":None}
        rec["wave_assignment"]=_family_wave(rec["family_candidate"] or "UNKNOWN",risk,granularity)
        if not rec["source_exists"] or granularity in {"AMBIGUOUS_CONTEXT_LIKE","CONTEXT_DOCUMENTATION_PROJECTION","CONTEXT_TEST_OR_VALIDATOR"} or identity_collision:
            reasons=[]
            if not rec["source_exists"]:reasons.append("SOURCE_MISSING")
            if granularity!="PACKAGE_CONTEXT" and granularity!="COMPOSITE_CONTEXT_SHELL":reasons.append("NOT_A_PACKAGE_CONTEXT")
            if identity_collision:reasons.append("IDENTITY_COLLISION")
            unresolved.append({"schema_version":"1.0.0","unresolved_id":content_id("CTXUNRES",[iid,reasons]),"identity_id":iid,"source_artifact_path":path,"reason_codes":sorted(set(reasons or ["BLOCKED_UNKNOWN"])),"blocking":True,"unresolved_digest":None})
            unresolved[-1]["unresolved_digest"]=digest_object(unresolved[-1],"unresolved_digest")
        rec["record_digest"]=digest_object(rec,"record_digest"); records.append(rec)
    return records, unresolved, dep_rows
