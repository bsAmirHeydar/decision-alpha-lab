from pathlib import Path
import re,yaml
ROOT=Path(__file__).resolve().parents[3]
folders=[ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_03',ROOT/'docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_03']
titles={};errors=[]
for folder in folders:
    for p in folder.glob('*.md'):
        text=p.read_text()
        m=re.match(r'^---\n(.*?)\n---\n',text,re.S)
        if not m:
            errors.append(f'frontmatter:{p}')
            continue
        meta=yaml.safe_load(m.group(1))
        title=meta.get('title')
        if not title:errors.append(f'title:{p}')
        if title in titles:errors.append(f'duplicate:{title}')
        titles[title]=p
if errors:raise SystemExit(';'.join(errors))
print(f'Obsidian validation passed for {len(titles)} notes')
