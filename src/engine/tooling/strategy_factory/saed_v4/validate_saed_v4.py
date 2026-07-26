from pathlib import Path
import json,re,yaml

def validate(root: Path):
 d=root/"docs/history/systems/saed_v4"; md=list(d.rglob("*.md")); stems={p.stem for p in md}; missing=[]
 for p in md:
  x=p.read_text(encoding="utf-8")
  if not x.startswith("---\n"): raise ValueError(f"frontmatter {p}")
  for target in re.findall(r"\[\[([^\]|#]+)",x):
   if Path(target).name not in stems: missing.append((str(p),target))
 for p in d.rglob("*.yaml"): yaml.safe_load(p.read_text(encoding="utf-8"))
 for p in d.rglob("*.json"): json.loads(p.read_text(encoding="utf-8"))
 return {"markdown":len(md),"missing_links":missing}
if __name__=="__main__":
 import sys; print(json.dumps(validate(Path(sys.argv[1] if len(sys.argv)>1 else ".")),indent=2))
