from tools.repository_paths import find_repository_root
from pathlib import Path
import hashlib, json
ROOT = find_repository_root(__file__)
A = ROOT / "releases/history/strategy_factory/artifacts/saed_v4_09"
paths = sorted(p for p in A.glob("*.JSON"))
manifest = {
    "phase": "SAED_V4_09",
    "version": "1.0.0",
    "artifact_hashes": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
    "claims": {"reference_implementation": True, "real_alpha": False, "runtime_parity": False, "production_authorization": False},
}
(A / "RELEASE_MANIFEST.JSON").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print("release manifest built")
