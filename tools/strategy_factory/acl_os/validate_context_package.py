from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator
from .common import SCHEMA_ROOT, PLACEHOLDER_RE, load_json, result

REQUIRED_DIRS=("doctrine","contracts","security","setups/manual","setups/ai","setups/baselines","fixtures/positive","fixtures/negative","fixtures/ambiguous","adapters","generated","tests")

def validate_context(root: Path, allow_placeholders: bool=False) -> dict:
    checks=[]
    manifest_path=root/"context_manifest.yaml"
    if not manifest_path.is_file():
        return {"passed":False,"checks":[result(False,"MISSING_MANIFEST",str(manifest_path))]}
    try: manifest=yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"passed":False,"checks":[result(False,"INVALID_YAML",str(exc))]}
    schema=load_json(SCHEMA_ROOT/"context_manifest.schema.json")
    errors=sorted(Draft202012Validator(schema).iter_errors(manifest),key=lambda e:list(e.path))
    checks.append(result(not errors,"MANIFEST_SCHEMA","context manifest schema",errors=[e.message for e in errors]))
    for d in REQUIRED_DIRS: checks.append(result((root/d).is_dir(),"REQUIRED_DIRECTORY",d))
    contracts=manifest.get("contracts",{}) if isinstance(manifest,dict) else {}
    for key,rel in contracts.items(): checks.append(result((root/str(rel)).is_file(),"CONTRACT_FILE",f"{key}:{rel}"))
    placeholders=[]
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md",".yaml",".yml",".json",".txt"}:
            for i,line in enumerate(p.read_text(encoding="utf-8",errors="replace").splitlines(),1):
                if PLACEHOLDER_RE.search(line): placeholders.append(f"{p.relative_to(root)}:{i}")
    checks.append(result(allow_placeholders or not placeholders,"PLACEHOLDER_SCAN",f"{len(placeholders)} placeholders",locations=placeholders[:200]))
    for kind in ("positive","negative","ambiguous"):
        count=sum(1 for p in (root/"fixtures"/kind).glob("*.json")) if (root/"fixtures"/kind).is_dir() else 0
        checks.append(result(count>0,"FIXTURE_COVERAGE",kind,count=count))
    generated_files=[p for p in (root/"generated").rglob("*") if p.is_file() and p.name!=".gitkeep"] if (root/"generated").exists() else []
    checks.append(result(not generated_files,"GENERATED_TEMPLATE_EMPTY","generated directory must be compiler-owned",files=[str(x) for x in generated_files]))
    passed=all(c["passed"] for c in checks)
    return {"passed":passed,"context_root":str(root),"allow_placeholders":allow_placeholders,"checks":checks}

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("context_root",type=Path); ap.add_argument("--allow-placeholders",action="store_true"); ap.add_argument("--json",action="store_true")
    ns=ap.parse_args(); out=validate_context(ns.context_root,ns.allow_placeholders)
    print(json.dumps(out,indent=2,sort_keys=True) if ns.json else ("PASS" if out["passed"] else "FAIL"))
    return 0 if out["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
