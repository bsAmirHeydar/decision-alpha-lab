from __future__ import annotations
from collections import defaultdict
from pathlib import PurePosixPath
from .canonical import digest_object

def _classify(namespace: str) -> str:
    low=namespace.lower()
    if 'atomic_concepts' in low or 'phase_deliveries' in low or 'obsidian_deep' in low or 'source_card' in low: return 'GENERATED_OR_DERIVED'
    if 'archive' in low or 'patches' in low: return 'ARCHIVE_OR_RELEASE_HISTORY'
    if 'alpha_lab_master_architecture' in low: return 'CANONICAL_ARCHITECTURE_CANDIDATE'
    if low.startswith('docs/'): return 'DOMAIN_DOCUMENTATION_CANDIDATE'
    return 'UNKNOWN'

def scan(records: tuple[dict,...]) -> tuple[list[dict],list[dict],list[dict]]:
    docs=[r for r in records if r['path'].startswith('docs/')]
    namespaces=set()
    for r in docs:
        parts=r['path'].split('/')
        if len(parts)>=2: namespaces.add('/'.join(parts[:2]))
        if len(parts)>=3 and parts[1] in {'alpha_lab_master_architecture','execution','strategy_factory','obsidian_deep'}: namespaces.add('/'.join(parts[:3]))
    rows=[]; maps={}
    for ns in sorted(namespaces):
        prefix=ns+'/'
        members=[r for r in docs if r['path'].startswith(prefix)]
        relmap={r['path'][len(prefix):]:r['sha256'] for r in members}
        maps[ns]=relmap
        ext={}
        for r in members: ext[r.get('extension') or '<none>']=ext.get(r.get('extension') or '<none>',0)+1
        fingerprint=digest_object({'members':sorted(relmap.items())})
        rows.append({'namespace':ns,'classification':_classify(ns),'file_count':len(members),'total_bytes':sum(r['size_bytes'] for r in members),'markdown_count':sum(1 for r in members if r.get('extension')=='.md'),'json_count':sum(1 for r in members if r.get('extension')=='.json'),'canvas_count':sum(1 for r in members if r.get('extension')=='.canvas'),'extension_counts':ext,'tree_fingerprint':fingerprint,'canonical_authority_claimed':False})
    byfp=defaultdict(list)
    for row in rows: byfp[row['tree_fingerprint']].append(row['namespace'])
    exact=[]
    for fp,nss in sorted(byfp.items()):
        if len(nss)>1:
            exact.append({'tree_fingerprint':fp,'namespaces':sorted(nss),'member_count':len(maps[nss[0]]),'exact_duplicate':True,'semantic_equivalence_claimed':False,'deletion_authority':False})
    # Compare top-level doc namespaces only for tractability and to avoid misleading nested containment.
    top=[r['namespace'] for r in rows if r['namespace'].count('/')==1]
    partial=[]
    for i,a in enumerate(top):
        A=maps[a]
        if len(A)<10: continue
        for b in top[i+1:]:
            B=maps[b]
            if len(B)<10: continue
            equal=sum(1 for k,v in A.items() if B.get(k)==v)
            denom=min(len(A),len(B))
            ratio=int(equal*10000/denom) if denom else 0
            if equal>=10 and ratio>=8000 and not (len(A)==len(B)==equal):
                smaller=a if len(A)<=len(B) else b; larger=b if smaller==a else a
                partial.append({'smaller_namespace':smaller,'larger_namespace':larger,'smaller_file_count':len(maps[smaller]),'larger_file_count':len(maps[larger]),'equal_relative_file_count':equal,'overlap_ratio_bps':ratio,'relation':'PARTIAL_SUPERSET_CANDIDATE','semantic_equivalence_claimed':False,'deletion_authority':False})
    return rows,exact,partial
