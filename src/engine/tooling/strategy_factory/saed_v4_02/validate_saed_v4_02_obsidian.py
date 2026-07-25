from tools.repository_paths import find_repository_root
from pathlib import Path
import re, yaml
ROOT=find_repository_root(__file__)
vault=ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4'
new_roots=[vault/'62_PHASE_DELIVERIES_V4/V4_02',vault/'63_ATOMIC_CONCEPTS_V4/V4_02']
files=list(vault.rglob('*.md'));stems={p.stem for p in files};titles={};front=[];broken=[]
for p in files:
    text=p.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        front.append(p);continue
    end=text.find('\n---\n',4)
    if end<0:
        front.append(p);continue
    meta=yaml.safe_load(text[4:end]) or {};title=meta.get('title')
    if title:titles.setdefault(title,[]).append(p)
    for target in re.findall(r'\[\[([^\]|#]+)',text):
        name=target.strip().split('/')[-1]
        if name not in stems and name not in titles:broken.append((p,name))
new_dups=[]
for title,paths in titles.items():
    if len(paths)>1 and any(any(root in p.parents or p.parent==root for root in new_roots) for p in paths):new_dups.append((title,paths))
if front or broken or new_dups:
    raise SystemExit(f'obsidian validation failed front={len(front)} broken={len(broken)} new_duplicates={len(new_dups)}')
print(f'obsidian validation passed files={len(files)} broken=0 new_duplicate_titles=0')
