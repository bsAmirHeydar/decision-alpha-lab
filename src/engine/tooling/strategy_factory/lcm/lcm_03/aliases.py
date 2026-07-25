from __future__ import annotations
from collections import defaultdict
from pathlib import Path,PurePosixPath
from .alias_extraction import extract
from .canonical import content_id,digest_object,normalize_alias
from .registries import EDGE_TO_ALIAS

def _record(alias_type,value,scope,identity_id,source_path,evidence,status='ACTIVE_REFERENCE',case_sensitive=False,confidence=10000):
    normalized=normalize_alias(value,case_sensitive)
    material={'type':alias_type,'value':normalized,'scope':scope,'source_path':source_path,'identity_id':identity_id}
    r={'alias_id':content_id('ALIAS',material,24),'alias_type':alias_type,'alias_value':value,'normalized_alias_value':normalized,'alias_scope':scope,'case_sensitive':case_sensitive,'identity_id':identity_id,'source_artifact_path':source_path,'alias_status':status,'resolution_status':'RESOLVABLE' if identity_id else 'UNKNOWN_IDENTITY_BLOCKED','evidence_codes':evidence,'confidence_bps':confidence,'redirect_materialized':False,'cutover_authorized':False,'alias_digest':None}
    r['alias_digest']=digest_object(r,'alias_digest'); return r

def build_aliases(repo_root: Path, active_records: list[dict], identity_by_path: dict, edges: list[dict]):
    aliases=[]
    for r in active_records:
        path=r['artifact_path']; iid=identity_by_path.get(path)
        aliases.append(_record('LEGACY_PATH',path,'GLOBAL',iid,path,['LCM02_ACTIVE_CANDIDATE_PATH']))
        aliases.append(_record('FILE_BASENAME',PurePosixPath(path).name,'GLOBAL',iid,path,['FILESYSTEM_BASENAME'],confidence=8000))
        if path.lower().endswith('.md'):
            aliases.append(_record('DOCUMENT_SLUG',PurePosixPath(path).stem,'GLOBAL',iid,path,['MARKDOWN_FILENAME_STEM'],confidence=8000))
        if iid:
            found=extract(repo_root/path,path)
            for value in found['functions']: aliases.append(_record('FUNCTION_NAME',value,iid,iid,path,['STATIC_SYMBOL_EXTRACTION'],case_sensitive=True,confidence=8500))
            for value in found['inputs']: aliases.append(_record('INPUT_NAME',value,iid,iid,path,['MQL5_INPUT_EXTRACTION'],case_sensitive=True,confidence=9000))
            for value in found['object_prefixes']: aliases.append(_record('OBJECT_PREFIX',value,'GLOBAL',iid,path,['STATIC_OBJECT_PREFIX_EXTRACTION'],case_sensitive=True,confidence=7000))
            for value in found['experiment_codes']: aliases.append(_record('EXPERIMENT_CODE',value,'GLOBAL',iid,path,['PATH_EXPERIMENT_CODE_EXTRACTION'],confidence=7000))
    for e in edges:
        alias_type=EDGE_TO_ALIAS.get(e.get('edge_type'))
        target=e.get('resolved_path','')
        if not alias_type or e.get('resolution_status')!='RESOLVED_INTERNAL' or target not in identity_by_path: continue
        iid=identity_by_path.get(target); source=e.get('source_path','')
        scope=PurePosixPath(source).parent.as_posix() or 'ROOT'
        aliases.append(_record(alias_type,e.get('raw_target',''),scope,iid,target,['LCM01_RESOLVED_DEPENDENCY_EDGE'],case_sensitive=alias_type in {'MQL5_INCLUDE','PYTHON_IMPORT'},confidence=9500))
    # exact duplicate alias records are removed by stable key; provenance remains in evidence source fields.
    unique={}
    for a in aliases:
        key=(a['alias_type'],a['normalized_alias_value'],a['alias_scope'],a['identity_id'],a['source_artifact_path'])
        unique.setdefault(key,a)
    return sorted(unique.values(),key=lambda x:(x['alias_type'],x['alias_scope'],x['normalized_alias_value'],str(x['identity_id']),x['source_artifact_path']))

def analyze_collisions(aliases: list[dict]):
    groups=defaultdict(list)
    for a in aliases: groups[(a['alias_type'],a['alias_scope'],a['normalized_alias_value'])].append(a)
    collisions=[]; blocked=set()
    for key,items in sorted(groups.items()):
        ids=sorted({x['identity_id'] for x in items if x['identity_id']})
        unknown=any(not x['identity_id'] for x in items)
        if len(ids)>1 or unknown:
            cid=content_id('ALCOLL',{'key':key,'ids':ids,'unknown':unknown},24)
            c={'collision_id':cid,'alias_type':key[0],'alias_scope':key[1],'normalized_alias_value':key[2],'identity_ids':ids,'source_artifact_paths':sorted({x['source_artifact_path'] for x in items}),'contains_unknown_identity':unknown,'resolution_status':'AMBIGUOUS_BLOCKED','automatic_resolution_allowed':False,'reason_codes':['ALIAS_RESOLVES_TO_MULTIPLE_IDENTITIES'] if len(ids)>1 else ['ALIAS_TARGET_IDENTITY_UNKNOWN'],'collision_digest':None}
            c['collision_digest']=digest_object(c,'collision_digest'); collisions.append(c); blocked.add(key)
    out=[]
    for a in aliases:
        key=(a['alias_type'],a['alias_scope'],a['normalized_alias_value'])
        if key in blocked:
            a=dict(a);a['alias_status']='AMBIGUOUS_BLOCKED';a['resolution_status']='AMBIGUOUS_BLOCKED';a['alias_digest']=digest_object(a,'alias_digest')
        out.append(a)
    index={}
    for a in out:
        if a['resolution_status']=='RESOLVABLE':
            key='|'.join([a['alias_type'],a['alias_scope'],a['normalized_alias_value']])
            prior=index.get(key)
            if prior and prior!=a['identity_id']: raise AssertionError('resolver collision escaped analysis')
            index[key]=a['identity_id']
    return out,collisions,index
