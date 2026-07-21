from __future__ import annotations
import ast
from pathlib import Path

FORBIDDEN_IMPORTS={'MetaTrader5','requests','httpx','socket','subprocess','ctypes'}
FORBIDDEN_CALL_SUFFIXES={'system','popen','run','Popen','connect','send','sendall'}

def scan_module(root: Path) -> dict:
    findings=[]; files=sorted(root.glob('*.py'))
    for path in files:
        tree=ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):
                for alias in node.names:
                    if alias.name.split('.')[0] in FORBIDDEN_IMPORTS: findings.append({"path":path.name,"line":node.lineno,"finding":"FORBIDDEN_IMPORT","value":alias.name})
            elif isinstance(node,ast.ImportFrom) and (node.module or '').split('.')[0] in FORBIDDEN_IMPORTS:
                findings.append({"path":path.name,"line":node.lineno,"finding":"FORBIDDEN_IMPORT","value":node.module})
    if findings: raise RuntimeError('LCM10A_STATIC_BOUNDARY_FAILED:'+str(findings[:10]))
    return {"passed":True,"scanned_file_count":len(files),"finding_count":0}
