from pathlib import Path
import json,re,yaml

def validate(root: Path) -> dict:
    docs=root/"docs/history/systems/saed_v3"
    md=list(docs.rglob("*.md")); stems={p.stem for p in md}; missing=[]
    for p in md:
        text=p.read_text(encoding="utf-8")
        if not text.startswith("---\n"): raise ValueError(f"missing frontmatter: {p}")
        for target in re.findall(r"\[\[([^\]|#]+)",text):
            if Path(target).name not in stems: missing.append((str(p),target))
    for p in docs.rglob("*.yaml"): yaml.safe_load(p.read_text(encoding="utf-8"))
    for p in docs.rglob("*.json"): json.loads(p.read_text(encoding="utf-8"))
    return {"markdown":len(md),"missing_links":missing}

if __name__=="__main__":
    import sys; print(json.dumps(validate(Path(sys.argv[1] if len(sys.argv)>1 else ".")),indent=2))
