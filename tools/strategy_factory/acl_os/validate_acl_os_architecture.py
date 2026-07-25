from __future__ import annotations
import argparse, json, re
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator
from .common import REPO_ROOT, SCHEMA_ROOT, load_json, result

WIKILINK=re.compile(r"\[\[([^\]|#]+)")

def validate(repo: Path=REPO_ROOT) -> dict:
    checks=[]; vault=repo/"docs"/"alpha_lab_master_architecture"/"context_lifecycle_os"
    notes=list(vault.rglob("*.md")); stems=set()
    for md in repo.rglob("*.md"):
        stems.add(md.stem)
        stems.add(re.sub(r"^\d+_", "", md.stem))
    checks.append(result(len(notes)>=200,"OBSIDIAN_NOTE_COUNT","architecture note count",count=len(notes)))
    missing_front=[]; missing_links=[]
    for p in notes:
        text=p.read_text(encoding="utf-8",errors="replace")
        if not text.startswith("---\n"): missing_front.append(str(p.relative_to(repo)))
        for target in WIKILINK.findall(text):
            if Path(target).stem not in stems: missing_links.append(f"{p.relative_to(repo)} -> {target}")
    checks.append(result(not missing_front,"FRONTMATTER","all architecture notes have frontmatter",files=missing_front[:100]))
    checks.append(result(not missing_links,"WIKILINK_CLOSURE","all wikilinks resolve",links=missing_links[:200]))
    schema_errors=[]
    for p in SCHEMA_ROOT.glob("*.schema.json"):
        try: Draft202012Validator.check_schema(load_json(p))
        except Exception as exc: schema_errors.append(f"{p.name}: {exc}")
    checks.append(result(len(list(SCHEMA_ROOT.glob('*.schema.json')))>=10 and not schema_errors,"SCHEMA_CLOSURE","closed public schemas",count=len(list(SCHEMA_ROOT.glob('*.schema.json'))),errors=schema_errors))
    yaml_errors=[]
    for p in (repo/"registry"/"acl_os").rglob("*.yaml"):
        try: yaml.safe_load(p.read_text(encoding="utf-8"))
        except Exception as exc: yaml_errors.append(f"{p.relative_to(repo)}: {exc}")
    checks.append(result(not yaml_errors,"YAML_PARSE","registry YAML parses",errors=yaml_errors))
    required=[
      "releases/history/misc/readmes/README_ALPHA_LAB_CONTEXT_LIFECYCLE_OS_ARCHITECTURE.md","releases/history/acl_os/manifests/ACL_OS_ARCHITECTURE_PATCH_MANIFEST.json",
      "registry/acl_os/README.md","lab/11_strategy_factory/contexts/_template/context_manifest.yaml",
      "tools/strategy_factory/acl_os/scaffold_context.py","tools/strategy_factory/acl_os/validate_context_package.py"
    ]
    missing=[x for x in required if not (repo/x).is_file()]
    checks.append(result(not missing,"REQUIRED_ARTIFACTS","required architecture artifacts",missing=missing))
    security_notes=list((vault/"08_SECURITY").glob("*.md")); checks.append(result(len(security_notes)>=25,"SECURITY_COVERAGE","security note coverage",count=len(security_notes)))
    phase_notes=list((vault/"11_IMPLEMENTATION_PROGRAM").glob("ACL_*.md")); checks.append(result(len(phase_notes)>=16,"IMPLEMENTATION_PHASES","ACL-00 through ACL-15",count=len(phase_notes)))
    passed=all(c["passed"] for c in checks)
    return {"passed":passed,"repo":str(repo),"checks":checks,"counts":{"notes":len(notes),"schemas":len(list(SCHEMA_ROOT.glob('*.schema.json'))),"security_notes":len(security_notes),"phase_notes":len(phase_notes)}}

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--repo",type=Path,default=REPO_ROOT); ap.add_argument("--json",action="store_true")
    ns=ap.parse_args(); out=validate(ns.repo)
    print(json.dumps(out,indent=2,sort_keys=True) if ns.json else ("PASS" if out["passed"] else "FAIL")); return 0 if out["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
