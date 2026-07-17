from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from .canonical import digest_bytes, digest_object, verify_embedded_digest, with_digest
from .errors import BudgetError, ContractError, KnownTimeError
from .io import safe_relative
from .schema_validation import validate_instance

def _parse_utc(value: str) -> datetime:
    try: dt=datetime.fromisoformat(value.replace("Z","+00:00"))
    except ValueError as exc: raise ContractError(f"invalid timestamp: {value}") from exc
    if dt.tzinfo is None or dt.utcoffset()!=timezone.utc.utcoffset(dt): raise ContractError(f"UTC timestamp required: {value}")
    return dt

def validate_batch_request(doc: dict[str,Any], handoff: dict[str,Any]) -> dict[str,Any]:
    validate_instance("batch_request",doc)
    if not verify_embedded_digest(doc,"request_digest"): raise ContractError("batch request digest invalid")
    if doc["context_id"]!=handoff["context_id"] or doc["context_version"]!=handoff["context_version"]: raise ContractError("batch request context mismatch")
    if doc["upstream_handoff_digest"]!=handoff["handoff_digest"]: raise ContractError("batch request handoff mismatch")
    if doc["live_order_submission_allowed"] or doc["capital_activation_allowed"]: raise ContractError("batch request grants forbidden authority")
    if doc["candidate_selection"]["mode"] not in {"ALL_CANONICAL","EXPLICIT_SETUP_IDS"}: raise ContractError("candidate selection mode denied")
    if doc["diagnostic_policy"] not in {"SEGREGATE_AND_INCLUDE","EXCLUDE"}: raise ContractError("diagnostic policy denied")
    _parse_utc(doc["frozen_at"])
    return doc

def compile_dataset_snapshot(doc: dict[str,Any], fixture_root: Path) -> tuple[dict[str,Any],bytes]:
    validate_instance("dataset_snapshot",doc)
    source=safe_relative(fixture_root,doc["source_path"])
    if not source.is_file() or source.is_symlink(): raise ContractError("dataset source missing or unsafe")
    payload=source.read_bytes()
    if not payload: raise ContractError("empty dataset denied")
    lines=[line for line in payload.decode("utf-8").splitlines() if line.strip()]
    if len(lines)!=doc["row_count"]: raise ContractError("dataset row count mismatch")
    cut=_parse_utc(doc["cut_at"]); through=_parse_utc(doc["available_through"])
    if through>cut: raise KnownTimeError("available_through exceeds cut_at")
    for index,line in enumerate(lines,1):
        import json
        try: row=json.loads(line)
        except Exception as exc: raise ContractError(f"invalid NDJSON row {index}") from exc
        if _parse_utc(row["available_at"])>cut: raise KnownTimeError(f"row {index} unavailable at cut")
        if _parse_utc(row["event_time"])>_parse_utc(row["available_at"]): raise KnownTimeError(f"row {index} event/availability inversion")
    compiled={k:v for k,v in doc.items() if k!="snapshot_digest"}
    compiled.update({"content_digest":digest_bytes(payload),"size_bytes":len(payload),"known_time_verified":True})
    compiled["snapshot_digest"]=digest_object(compiled)
    return compiled,payload

def validate_label_contract(doc: dict[str,Any], snapshot: dict[str,Any]) -> dict[str,Any]:
    validate_instance("label_contract",doc)
    if not verify_embedded_digest(doc,"label_contract_digest"): raise ContractError("label contract digest invalid")
    if doc["dataset_snapshot_id"]!=snapshot["snapshot_id"]: raise ContractError("label dataset binding mismatch")
    if doc["maturity"]["horizon_seconds"]<=0: raise ContractError("positive label horizon required")
    if doc["maturity"]["available_after_seconds"]<doc["maturity"]["horizon_seconds"]: raise KnownTimeError("label available before maturity")
    if doc["role"]=="PRIMARY" and doc["uses_future_path_diagnostics"]: raise KnownTimeError("future path forbidden in primary label")
    if doc["role"]=="DIAGNOSTIC" and not doc["segregated_from_selection"]: raise ContractError("diagnostic label must be segregated")
    return doc

def validate_split_contract(doc: dict[str,Any], snapshot: dict[str,Any]) -> dict[str,Any]:
    validate_instance("split_contract",doc)
    if not verify_embedded_digest(doc,"split_digest"): raise ContractError("split digest invalid")
    if doc["dataset_snapshot_id"]!=snapshot["snapshot_id"]: raise ContractError("split dataset binding mismatch")
    if doc["method"]!="PURGED_WALK_FORWARD": raise ContractError("only purged walk-forward accepted")
    train_end=_parse_utc(doc["train"]["end"]); valid_start=_parse_utc(doc["validation"]["start"]); valid_end=_parse_utc(doc["validation"]["end"]); test_start=_parse_utc(doc["test"]["start"])
    if not train_end<valid_start or not valid_end<test_start: raise ContractError("split overlap or missing temporal ordering")
    if doc["purge_seconds"]<=0 or doc["embargo_seconds"]<=0: raise ContractError("purge and embargo required")
    if not doc["transform_fit_scope"]=="TRAIN_ONLY": raise KnownTimeError("transform fit scope must be train-only")
    return doc

def validate_environment_lock(doc: dict[str,Any]) -> dict[str,Any]:
    validate_instance("environment_lock",doc)
    if not verify_embedded_digest(doc,"environment_digest"): raise ContractError("environment digest invalid")
    denied=[doc["network_access_allowed"],doc["live_order_submission_allowed"],doc["capital_activation_allowed"],doc["secret_access_allowed"]]
    if any(denied): raise ContractError("environment grants forbidden capability")
    if not doc["python_lock_digest"].startswith("sha256:"): raise ContractError("Python lock must be content addressed")
    return doc

def validate_compute_budget(doc: dict[str,Any]) -> dict[str,Any]:
    validate_instance("compute_budget",doc)
    if not verify_embedded_digest(doc,"budget_digest"): raise ContractError("budget digest invalid")
    caps=(doc["max_tasks"],doc["max_cpu_seconds"],doc["max_memory_mb"],doc["max_store_bytes"],doc["max_store_objects"])
    if any(v<=0 for v in caps): raise BudgetError("budget caps must be positive")
    if doc["cancellation_policy"]!="FAIL_CLOSED_ON_FIRST_BREACH": raise BudgetError("cancellation policy denied")
    return doc
