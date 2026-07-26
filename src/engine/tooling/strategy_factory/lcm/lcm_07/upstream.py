from .canonical import digest_object,sha256_bytes
from .errors import IntegrityError
from .io import read_json

def latest_framework(repo):
    roots=sorted((repo/"registry/history/lcm/frameworks").glob("FRAMEWORK_*"))
    roots=[x for x in roots if x.is_dir() and not x.is_symlink()]
    if not roots: raise IntegrityError("LCM-06 framework package not found")
    return roots[-1]
def _verify_manifest(root,manifest):
    seen=set()
    for rec in manifest.get("artifacts",[]):
        rel=rec["path"]
        if rel in seen: raise IntegrityError(f"duplicate upstream manifest path: {rel}")
        seen.add(rel); p=root/rel
        if p.is_symlink() or not p.is_file(): raise IntegrityError(f"invalid upstream artifact: {rel}")
        if p.stat().st_size!=rec["size_bytes"] or sha256_bytes(p.read_bytes())!=rec["sha256"]: raise IntegrityError(f"upstream manifest mismatch: {rel}")
    if manifest.get("artifact_count")!=len(seen) or digest_object(manifest,"output_manifest_digest")!=manifest.get("output_manifest_digest"): raise IntegrityError("upstream manifest invalid")
def load(repo):
    root=latest_framework(repo); marker=read_json(root/"framework_marker.json"); handoff=read_json(root/"handoff/lcm06_to_lcm07_handoff.json"); manifest=read_json(root/"output_manifest.json"); receipt=read_json(root/"framework_receipt.json")
    _verify_manifest(root,manifest)
    if marker.get("phase_id")!="LCM-06" or marker.get("framework_run_id")!=root.name: raise IntegrityError("LCM-06 marker invalid")
    if handoff.get("handoff_type")!="LCM06_TO_LCM07" or digest_object(handoff,"handoff_digest")!=handoff.get("handoff_digest"): raise IntegrityError("LCM-06 handoff invalid")
    if receipt.get("handoff_digest")!=handoff.get("handoff_digest"): raise IntegrityError("LCM-06 receipt binding invalid")
    if handoff.get("shared_engine_extraction_authorized") is not False: raise IntegrityError("upstream extraction authority unexpectedly enabled")
    return {"root":root,"marker":marker,"handoff":handoff,"manifest":manifest,"receipt":receipt}
