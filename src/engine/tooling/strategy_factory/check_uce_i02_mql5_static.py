#!/usr/bin/env python3
"""Static MQL5 checks for UCE-I02 when MetaEditor is unavailable."""
from __future__ import annotations
import argparse,re
from pathlib import Path

def strip_literals(text:str)->str:
    text=re.sub(r'//.*','',text);text=re.sub(r'/\*.*?\*/','',text,flags=re.S);text=re.sub(r'"(?:\\.|[^"\\])*"','""',text);return text

def resolve_local(path:Path,inc:str,root:Path)->bool:
    if inc.startswith("AlphaLab/"):
        return (root/"mql5/Include"/inc).exists()
    return (path.parent/inc).resolve().exists()

def main()->int:
    parser=argparse.ArgumentParser();parser.add_argument("root",nargs="?",default=".");args=parser.parse_args();root=Path(args.root).resolve();failures=[]
    paths=list((root/"mql5/Include/AlphaLab/StrategyFactory/ContextPackage").glob("UCE02_*.mqh"))+list((root/"mql5/Experts").rglob("UCE_I02_*.mq5"))
    for path in paths:
        text=path.read_text(encoding="utf-8",errors="ignore")
        if "LongToString(" in text: failures.append(f"{path.relative_to(root)}: LongToString is disallowed")
        if path.suffix==".mqh":
            if not text.lstrip().startswith("#ifndef") or "#define" not in text or "#endif" not in text: failures.append(f"{path.relative_to(root)}: missing include guard")
        clean=strip_literals(text)
        for left,right in (("{","}"),("(",")"),("[","]")):
            if clean.count(left)!=clean.count(right): failures.append(f"{path.relative_to(root)}: unbalanced {left}{right}")
        for inc in re.findall(r'#include\s+["<]([^">]+)[">]',text):
            if inc.startswith("IntermarketDivergenceExecution/"): continue
            if not resolve_local(path,inc,root): failures.append(f"{path.relative_to(root)}: unresolved include {inc}")
    if len(paths)<16: failures.append(f"expected at least 16 UCE-I02 MQL5 files, found {len(paths)}")
    if failures:
        print("UCE-I02 MQL5 static check: FAIL");print("\n".join(failures));return 1
    print(f"UCE-I02 MQL5 static check: PASS ({len(paths)} files)");return 0
if __name__=="__main__": raise SystemExit(main())
