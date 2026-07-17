from __future__ import annotations
from pathlib import Path
from typing import Any
from .artifact_manifest import verify_output_manifest
from .canonical import digest_object, with_digest
from .event_ledger import verify_event_ledger
from .io import load_json

def verify_frozen_batch(root: Path) -> dict[str,Any]:
    batch=load_json(root/"batch/batch_definition.json"); manifest=load_json(root/"output_manifest.json"); receipt=load_json(root/"batch_receipt.json"); events=load_json(root/"events/batch_event_ledger.json")
    checks={"root_marker":(root/".acl05_generated_root").is_file(),"batch_frozen":batch.get("state")=="FROZEN" and batch.get("material_mutation_allowed") is False,"output_manifest":verify_output_manifest(root,manifest),"event_chain":verify_event_ledger(events),"receipt_digest":receipt.get("receipt_digest")==digest_object({k:v for k,v in receipt.items() if k!="receipt_digest"}),"receipt_binds_manifest":receipt.get("output_manifest_digest")==manifest.get("manifest_digest"),"order_denied":receipt.get("live_order_submission_allowed") is False,"capital_denied":receipt.get("capital_activation_allowed") is False}
    return with_digest({"schema_version":"1.0.0","batch_id":batch.get("batch_id"),"checks":checks,"passed":all(checks.values())},"report_digest")
