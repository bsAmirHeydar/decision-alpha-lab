from __future__ import annotations
import ast, re, gc
from pathlib import Path, PurePosixPath
from .canonical import sha256_bytes

CAP_NODES={'eval':'DYNAMIC_EVAL','exec':'DYNAMIC_EXEC','open':'FILE_IO','compile':'DYNAMIC_COMPILE','__import__':'DYNAMIC_IMPORT'}
CAP_MODULES={'subprocess':'SUBPROCESS','socket':'NETWORK_API','requests':'NETWORK_API','urllib':'NETWORK_API','http':'NETWORK_API','pickle':'UNSAFE_DESERIALIZATION_INDICATOR','sqlite3':'PERSISTENT_STATE','random':'NONDETERMINISM_INDICATOR','secrets':'SECRET_GENERATION_INDICATOR'}

def module_map(paths: list[str]) -> dict[str,list[str]]:
    out={}
    for path in paths:
        pp=PurePosixPath(path)
        if pp.name=='__init__.py': mod='.'.join(pp.parent.parts)
        else: mod='.'.join(pp.with_suffix('').parts)
        out.setdefault(mod,[]).append(path)
    return out

def _resolve_relative(source: str, module: str|None, level: int, mmap: dict[str,list[str]]) -> tuple[str,str,list[str]]:
    pp=PurePosixPath(source)
    base=list(pp.parent.parts)
    if level:
        remove=max(0,level-1)
        if remove: base=base[:-remove]
    parts=base+((module or '').split('.') if module else [])
    key='.'.join([x for x in parts if x])
    hits=mmap.get(key,[])
    if len(hits)==1: return 'RESOLVED_INTERNAL',hits[0],hits
    if len(hits)>1: return 'AMBIGUOUS_INTERNAL','',hits
    return 'UNRESOLVED','',[]

def scan(repo_root: Path, paths: list[str]) -> tuple[list[dict],list[dict],list[dict],list[dict]]:
    mmap=module_map(paths); edges=[]; caps=[]; entries=[]; parse_fail=[]
    gc_was_enabled=gc.isenabled()
    if gc_was_enabled: gc.disable()
    try:
        for source in paths:
            p=repo_root/source; text=p.read_text(encoding='utf-8',errors='replace'); lines=text.splitlines()
            name=PurePosixPath(source).name.lower(); low=source.lower()
            if name.startswith('test_') or '/tests' in low or '/tests_' in low:
                entries.append({'path':source,'entry_point_type':'PYTHON_TEST_ENTRY','evidence':'PATH_OR_NAME','authority_inferred':False})
            if name in {'cli.py','__main__.py'} or 'if __name__' in text:
                entries.append({'path':source,'entry_point_type':'PYTHON_COMMAND_ENTRY','evidence':'CLI_OR_MAIN_GUARD','authority_inferred':False})
            try: tree=ast.parse(text,filename=source)
            except SyntaxError as exc:
                parse_fail.append({'path':source,'language':'PYTHON','reason':'SYNTAX_ERROR','line_number':exc.lineno or 0,'message_digest':sha256_bytes(str(exc).encode())}); continue
            for node in ast.walk(tree):
                if isinstance(node,ast.Import):
                    for alias in node.names:
                        mod=alias.name; top=mod.split('.')[0]
                        hits=mmap.get(mod,[])
                        status='RESOLVED_INTERNAL' if len(hits)==1 else ('AMBIGUOUS_INTERNAL' if len(hits)>1 else 'EXTERNAL_OR_STDLIB')
                        edges.append({'source_path':source,'edge_type':'PYTHON_IMPORT','raw_target':mod,'line_number':node.lineno,'resolution_status':status,'resolved_path':hits[0] if len(hits)==1 else '','resolution_candidates':hits,'semantic_reachability_claimed':False})
                        if top in CAP_MODULES:
                            caps.append(_cap(source,'PYTHON',CAP_MODULES[top],mod,node.lineno,lines))
                elif isinstance(node,ast.ImportFrom):
                    mod=node.module or ''; raw='.'*node.level+mod
                    if node.level: status,resolved,hits=_resolve_relative(source,mod,node.level,mmap)
                    else:
                        hits=mmap.get(mod,[]); status='RESOLVED_INTERNAL' if len(hits)==1 else ('AMBIGUOUS_INTERNAL' if len(hits)>1 else 'EXTERNAL_OR_STDLIB'); resolved=hits[0] if len(hits)==1 else ''
                    edges.append({'source_path':source,'edge_type':'PYTHON_FROM_IMPORT','raw_target':raw,'line_number':node.lineno,'resolution_status':status,'resolved_path':resolved,'resolution_candidates':hits,'semantic_reachability_claimed':False})
                    top=mod.split('.')[0] if mod else ''
                    if top in CAP_MODULES: caps.append(_cap(source,'PYTHON',CAP_MODULES[top],raw,node.lineno,lines))
                elif isinstance(node,ast.Call):
                    fn=''
                    if isinstance(node.func,ast.Name): fn=node.func.id
                    elif isinstance(node.func,ast.Attribute): fn=node.func.attr
                    if fn in CAP_NODES: caps.append(_cap(source,'PYTHON',CAP_NODES[fn],fn,node.lineno,lines))
            patterns=[('ENVIRONMENT_ACCESS',r'\bos\.environ\b'),('SHELL_EXECUTION',r'\bshell\s*=\s*True\b'),('FILE_MUTATION',r'\b(write_text|write_bytes|unlink|rmtree|replace|rename)\s*\(')]
            for kind,pat in patterns:
                for m in re.finditer(pat,text):
                    caps.append(_cap(source,'PYTHON',kind,m.group(0),text.count('\n',0,m.start())+1,lines))
    finally:
        if gc_was_enabled: gc.enable()
    edges.sort(key=lambda x:(x['source_path'],x['line_number'],x['raw_target']))
    caps.sort(key=lambda x:(x['path'],x['line_number'],x['capability_kind'],x['matched_token']))
    entries=sorted({(e['path'],e['entry_point_type'],e['evidence']):e for e in entries}.values(), key=lambda x:(x['path'],x['entry_point_type']))
    return edges,caps,entries,parse_fail

def _cap(path,lang,kind,token,line,lines):
    raw=lines[line-1] if line and line<=len(lines) else ''
    return {'path':path,'language':lang,'capability_kind':kind,'matched_token':token[:120],'line_number':line,'line_digest':sha256_bytes(raw.strip().encode()),'risk_indicator_only':True,'live_authority_inferred':False}
