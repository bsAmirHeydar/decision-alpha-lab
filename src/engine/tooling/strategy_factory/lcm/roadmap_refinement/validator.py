from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

WIKI_RE=re.compile(r"\[\[([^\]]+)\]\]")
FM_RE=re.compile(r"\A---\n(.*?)\n---\n",re.S)

class ValidationError(RuntimeError): pass

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def load_registry(root:Path)->dict:
    p=root/'roadmap_registry.json'
    d=json.loads(p.read_text(encoding='utf-8'))
    if d.get('subphase_count')!=22: raise ValidationError('roadmap must contain exactly 22 planned subphases')
    rec=d.get('records',[])
    if len(rec)!=22: raise ValidationError('record count mismatch')
    ids=[r['subphase_id'] for r in rec]
    if len(ids)!=len(set(ids)): raise ValidationError('duplicate subphase id')
    if ids[0]!='LCM-08A' or ids[-1]!='LCM-16B': raise ValidationError('unexpected sequence boundary')
    for i,r in enumerate(rec):
        expected_prev='LCM-07' if i==0 else rec[i-1]['subphase_id']
        expected_next=None if i==len(rec)-1 else rec[i+1]['subphase_id']
        if r.get('predecessor')!=expected_prev or r.get('successor')!=expected_next:
            raise ValidationError(f"broken dependency chain at {r['subphase_id']}")
        if r.get('live_order_authority_created') or r.get('capital_authority_created'):
            raise ValidationError('forbidden authority in roadmap')
    return d

def frontmatter_ok(path:Path)->bool:
    t=path.read_text(encoding='utf-8')
    m=FM_RE.match(t)
    if not m:return False
    fm=m.group(1)
    return all(re.search(rf'^{k}:',fm,re.M) for k in ('title','status','version','updated','tags'))

def validate(repo:Path, registry_root:Path)->dict:
    d=load_registry(registry_root)
    docs=[]
    for r in d['records']:
        p=repo/r['document_path']
        if not p.is_file(): raise ValidationError(f'missing document {p}')
        if not frontmatter_ok(p): raise ValidationError(f'invalid frontmatter {p}')
        text=p.read_text(encoding='utf-8')
        required=('## Purpose','## Explicit non-goals','## Entry contract','## Engineering workstreams','## Mandatory verification','## Hostile review','## Failure semantics','## Rollback requirements','## Acceptance gate','## Handoff contract')
        for h in required:
            if h not in text: raise ValidationError(f'{r["subphase_id"]} missing {h}')
        docs.append(str(p.relative_to(repo)).replace('\\','/'))
    masters=json.loads((registry_root/'master_phase_partition_registry.json').read_text(encoding='utf-8'))['masters']
    if set(masters)!={f'LCM-{i:02d}' for i in range(8,17)}: raise ValidationError('master phase set mismatch')
    if any(len(v['parts']) not in (2,3) for v in masters.values()): raise ValidationError('master partition must have 2 or 3 parts')
    return {'passed':True,'roadmap_id':d['roadmap_id'],'subphase_count':len(docs),'document_count':len(docs),'next_subphase':d['next_subphase']}

def verify_installation(repo:Path, registry_root:Path, index:Path)->dict:
    result=validate(repo,registry_root)
    paths=[x.strip() for x in index.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
    missing=[x for x in paths if not (repo/x).exists()]
    result.update({'indexed_path_count':len(paths),'missing':missing,'passed':result['passed'] and not missing})
    return result

def main():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True)
    v=sp.add_parser('verify-package');v.add_argument('--repo-root',required=True);v.add_argument('--roadmap-root',required=True)
    i=sp.add_parser('verify-installation');i.add_argument('--repo-root',required=True);i.add_argument('--roadmap-root',required=True);i.add_argument('--patch-index',required=True)
    a=p.parse_args(); repo=Path(a.repo_root); rr=Path(a.roadmap_root)
    try:
        out=validate(repo,rr) if a.cmd=='verify-package' else verify_installation(repo,rr,Path(a.patch_index))
    except Exception as e:
        out={'passed':False,'error':f'{type(e).__name__}: {e}'}
    print(json.dumps(out,indent=2,sort_keys=True));raise SystemExit(0 if out.get('passed') else 1)
if __name__=='__main__':main()
