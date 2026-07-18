from __future__ import annotations

from pathlib import Path

from .canonical import content_id, digest_object, sha256_file


def build_baseline_manifest(records: list[dict], scope_policy_digest: str) -> dict:
    identity_material = [
        {"path": r["path"], "kind": r["kind"], "size_bytes": r["size_bytes"], "sha256": r.get("sha256"), "symlink_target": r.get("symlink_target")}
        for r in records
    ]
    baseline_id = content_id("BASELINE", {"records": identity_material, "scope_policy_digest": scope_policy_digest})
    value = {
        "schema_version": "1.0.0",
        "baseline_id": baseline_id,
        "phase_id": "LCM-00",
        "path_semantics": "ROOT_RELATIVE_POSIX_BYTE_EXACT",
        "scope_policy_digest": scope_policy_digest,
        "record_count": len(records),
        "records": records,
        "manifest_digest": "",
    }
    value["manifest_digest"] = digest_object(value, "manifest_digest")
    return value


def build_output_manifest(root: Path) -> dict:
    records: list[dict] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p.name != "output_manifest.json"):
        rel = path.relative_to(root).as_posix()
        records.append({"path": rel, "size_bytes": path.stat().st_size, "sha256": sha256_file(path)})
    value = {
        "schema_version": "1.0.0",
        "artifact_count": len(records),
        "artifacts": records,
        "output_manifest_digest": "",
    }
    value["output_manifest_digest"] = digest_object(value, "output_manifest_digest")
    return value
