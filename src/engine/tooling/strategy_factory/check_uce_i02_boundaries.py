#!/usr/bin/env python3
"""Enforce UCE-I02 authority, dependency, and phase ownership boundaries."""
from __future__ import annotations
import argparse
from pathlib import Path

FORBIDDEN=("OrderSend(","OrderCheck(","CTrade","PositionOpen(","PositionClose(","Buy(","Sell(")
FUTURE_IMPORTS=("strategy_factory_treatment","strategy_factory_trainer_v3","strategy_factory_outcome_cube")

def main()->int:
    parser=argparse.ArgumentParser();parser.add_argument("root",nargs="?",default=".");args=parser.parse_args();root=Path(args.root).resolve();failures=[]
    owned=[root/"mql5/Include/AlphaLab/StrategyFactory/ContextPackage",root/"mql5/Experts/StrategyFactory/UCE_I02_ContextPackageDiagnostic.mq5",root/"mql5/Tests/Experts/StrategyFactory/UCE_I02_ContextPackageSelfTest.mq5",root/"mql5/Tests/Experts/StrategyFactory/UCE_I02_EXP0017ReferenceSelfTest.mq5",root/"src/engine/packages/strategy_factory_contexts_v3"]
    files=[]
    for path in owned:
        if path.is_file(): files.append(path)
        elif path.is_dir(): files.extend(p for p in path.rglob("*") if p.is_file() and p.suffix in {".mqh",".mq5",".py"})
        else: failures.append(f"missing owned path: {path.relative_to(root)}")
    for path in files:
        text=path.read_text(encoding="utf-8",errors="ignore")
        for token in FORBIDDEN:
            if token in text: failures.append(f"{path.relative_to(root)}: forbidden live authority token {token}")
        if path.suffix==".py":
            for token in FUTURE_IMPORTS:
                if token in text: failures.append(f"{path.relative_to(root)}: imports future phase module {token}")
    if failures:
        print("UCE-I02 boundary check: FAIL");print("\n".join(failures));return 1
    print(f"UCE-I02 boundary check: PASS ({len(files)} owned source files)");return 0
if __name__=="__main__": raise SystemExit(main())
