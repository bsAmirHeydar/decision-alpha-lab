#!/usr/bin/env python3
"""Static MQL5 checks used when MetaEditor is unavailable."""
from __future__ import annotations
import argparse,re
from pathlib import Path

def strip_literals(text:str)->str:
    text=re.sub(r'//.*','',text)
    text=re.sub(r'/\*.*?\*/','',text,flags=re.S)
    text=re.sub(r'"(?:\\.|[^"\\])*"','""',text)
    return text

def main()->int:
    parser=argparse.ArgumentParser();parser.add_argument("root",nargs="?",default=".");args=parser.parse_args();root=Path(args.root).resolve()
    paths=list((root/"mql5/Include/AlphaLab/StrategyFactory/Contracts").glob("UCE03_*.mqh"))+list((root/"mql5/Experts").rglob("UCE_I01_*.mq5"))
    failures=[]
    for path in paths:
        text=path.read_text(encoding="utf-8",errors="ignore")
        if "LongToString(" in text:failures.append(f"{path}: LongToString is disallowed")
        clean=strip_literals(text)
        for left,right in (("{","}"),("(",")"),("[","]")):
            if clean.count(left)!=clean.count(right):failures.append(f"{path}: unbalanced {left}{right}")
        for include in re.findall(r'#include\s+"([^"]+)"',text):
            candidate=path.parent/include
            if not candidate.exists():failures.append(f"{path}: unresolved local include {include}")
    if len(paths)<17:failures.append(f"expected at least 17 MQL5-owned files, found {len(paths)}")
    if failures:
        print("UCE-I01 MQL5 static check: FAIL");print("\n".join(str(x) for x in failures));return 1
    print(f"UCE-I01 MQL5 static check: PASS ({len(paths)} files)")
    return 0
if __name__=="__main__":raise SystemExit(main())
