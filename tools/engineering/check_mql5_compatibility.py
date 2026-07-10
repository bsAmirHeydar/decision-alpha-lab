#!/usr/bin/env python3
"""Scan MQL5 source for known Decision Alpha Lab compatibility hazards.

This is a static preflight, not a replacement for MetaEditor compilation.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

RULES = [
    ('ERROR','unsupported-long-to-string',re.compile(r'\bLongToString\s*\('),
     'Use the compiler-tested IntegerToString pattern for integer/long serialization.'),
    ('ERROR','case-function-assignment',re.compile(r'=\s*StringTo(?:Upper|Lower)\s*\('),
     'StringToUpper/Lower mutate a writable string and return bool.'),
    ('ERROR','case-function-comparison',re.compile(r'StringTo(?:Upper|Lower)\s*\([^;\n]+\)\s*(?:==|!=)'),
     'Normalize into a writable local variable before comparison.'),
    ('WARN','direct-temporary-case-mutation',re.compile(r'StringTo(?:Upper|Lower)\s*\(\s*[A-Za-z_]\w*\s*\('),
     'The argument appears to be a temporary expression, not an lvalue.'),
    ('WARN','broad-object-delete',re.compile(r'ObjectsDeleteAll\s*\(\s*0\s*\)'),
     'Delete only objects owned by a deterministic module prefix.'),
]


def strip_comments(text: str) -> str:
    text=re.sub(r'/\*.*?\*/','',text,flags=re.S)
    text=re.sub(r'//.*','',text)
    return text


def main() -> int:
    root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
    findings=[]
    for p in sorted(list(root.rglob('*.mq5'))+list(root.rglob('*.mqh'))):
        if '.git' in p.parts: continue
        raw=p.read_text(encoding='utf-8',errors='replace')
        text=strip_comments(raw)
        lines=text.splitlines()
        for severity,rid,pat,msg in RULES:
            for i,line in enumerate(lines,1):
                if pat.search(line): findings.append((severity,p.relative_to(root).as_posix(),i,rid,msg,line.strip()))
    errors=sum(1 for f in findings if f[0]=='ERROR')
    warnings=sum(1 for f in findings if f[0]=='WARN')
    print(f'MQL5 compatibility scan: errors={errors} warnings={warnings}')
    for f in findings:
        print(f'{f[0]} {f[1]}:{f[2]} [{f[3]}] {f[4]} :: {f[5]}')
    return 1 if errors else 0

if __name__=='__main__':
    raise SystemExit(main())
