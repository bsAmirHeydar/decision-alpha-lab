from pathlib import Path
import sys,re,json
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("docs/strategy_factory_universal_context_exploitation_engine")
errors=[]
md=list(root.rglob("*.md"))
if len(md)<180: errors.append(f"expected at least 180 markdown files, found {len(md)}")
for p in md:
    t=p.read_text(encoding="utf-8")
    if not t.startswith("---\n"): errors.append(f"missing front matter: {p}")
    if not re.search(r"^# ",t,re.M): errors.append(f"missing H1: {p}")
    if len(re.findall(r"\b[\w'-]+\b",t))<80: errors.append(f"document too small: {p}")
required=[root/"00_UNIVERSAL_CONTEXT_EXPLOITATION_ENGINE_MOC.md",root/"34_IMPLEMENTATION_ROADMAP.md"]
for p in required:
    if not p.exists(): errors.append(f"missing required: {p}")
for sub,count in {"contracts":15,"representations":10,"tasks":12,"treatments":18,"training":20,"validation":20,"operations":15,"examples":8,"roadmap_phases":16}.items():
    n=len(list((root/sub).glob("*.md")))
    if n<count: errors.append(f"{sub}: expected >= {count}, found {n}")
if errors:
    print("UCEE V2 VALIDATION FAILED")
    for e in errors: print("-",e)
    raise SystemExit(1)
print(f"UCEE V2 VALIDATION PASS: {len(md)} markdown files")
