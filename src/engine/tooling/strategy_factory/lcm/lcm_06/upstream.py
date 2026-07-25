from .canonical import digest_object, sha256_bytes
from .errors import IntegrityError
from .io import read_json, read_jsonl


def latest_topology(repo):
    roots = sorted((repo / "registry/legacy_context_migration/target_paths").glob("TOPOLOGY_*"))
    roots = [root for root in roots if root.is_dir() and not root.is_symlink()]
    if not roots:
        raise IntegrityError("LCM-05 topology package not found")
    return roots[-1]


def verify_manifest(root, manifest):
    seen = set()
    for record in manifest.get("artifacts", []):
        relative_path = record["path"]
        if relative_path in seen:
            raise IntegrityError(f"duplicate upstream manifest path: {relative_path}")
        seen.add(relative_path)
        path = root / relative_path
        if path.is_symlink():
            raise IntegrityError(f"upstream symlink forbidden: {relative_path}")
        if not path.is_file():
            raise IntegrityError(f"missing upstream artifact: {relative_path}")
        if path.stat().st_size != record["size_bytes"] or sha256_bytes(path.read_bytes()) != record["sha256"]:
            raise IntegrityError(f"upstream manifest mismatch: {relative_path}")
    if manifest.get("artifact_count") != len(seen):
        raise IntegrityError("upstream manifest artifact count invalid")
    if digest_object(manifest, "output_manifest_digest") != manifest.get("output_manifest_digest"):
        raise IntegrityError("upstream manifest digest invalid")
    return True


def load(repo):
    root = latest_topology(repo)
    marker = read_json(root / "topology_marker.json")
    handoff = read_json(root / "handoff/lcm05_to_lcm06_handoff.json")
    manifest = read_json(root / "output_manifest.json")
    receipt = read_json(root / "topology_receipt.json")
    verify_manifest(root, manifest)
    if marker.get("phase_id") != "LCM-05" or marker.get("topology_run_id") != root.name:
        raise IntegrityError("LCM-05 topology marker binding invalid")
    if handoff.get("handoff_type") != "LCM05_TO_LCM06" or handoff.get("topology_run_id") != marker.get("topology_run_id"):
        raise IntegrityError("LCM-05 handoff type or run binding invalid")
    if digest_object(handoff, "handoff_digest") != handoff.get("handoff_digest"):
        raise IntegrityError("LCM05 handoff digest invalid")
    if receipt.get("handoff_digest") != handoff.get("handoff_digest"):
        raise IntegrityError("LCM05 receipt binding invalid")
    if receipt.get("topology_run_id") != marker.get("topology_run_id"):
        raise IntegrityError("LCM05 receipt run binding invalid")
    return {
        "root": root,
        "marker": marker,
        "handoff": handoff,
        "manifest": manifest,
        "receipt": receipt,
        "artifact_maps": read_jsonl(root / "mappings/artifact_target_map.jsonl"),
        "identity_maps": read_jsonl(root / "mappings/identity_target_map.jsonl"),
        "ambiguities": read_jsonl(root / "mappings/identity_ambiguity_target_queue.jsonl"),
        "blockers": read_json(root / "blockers/materialization_blockers.json"),
    }
