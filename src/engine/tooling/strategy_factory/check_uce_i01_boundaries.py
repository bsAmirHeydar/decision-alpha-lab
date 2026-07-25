#!/usr/bin/env python3
"""Fail-closed architecture boundary guard for UCE-I01-owned files."""
from __future__ import annotations
import argparse
from pathlib import Path

FORBIDDEN=("OrderSend(","OrderCheck(","CTrade","PositionOpen(","requests.","urllib.request","subprocess.Popen","sklearn","torch","tensorflow","xgboost","lightgbm")
OWNED=("mql5/Include/AlphaLab/StrategyFactory/Contracts/UCE03_","mql5/Tests/Experts/StrategyFactory/UCE_I01_","mql5/Experts/StrategyFactory/UCE_I01_","src/engine/packages/strategy_factory_contracts_v3")

def main()->int:
    parser=argparse.ArgumentParser();parser.add_argument("root",nargs="?",default=".");args=parser.parse_args();root=Path(args.root).resolve()
    failures=[]
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".py",".mqh",".mq5"}:continue
        rel=path.relative_to(root).as_posix()
        if not any(rel.startswith(prefix) for prefix in OWNED):continue
        text=path.read_text(encoding="utf-8",errors="ignore")
        for token in FORBIDDEN:
            if token in text:failures.append(f"{rel}: forbidden boundary token {token}")
    if failures:
        print("UCE-I01 boundary guard: FAIL");print("\n".join(failures));return 1
    print("UCE-I01 boundary guard: PASS")
    return 0
if __name__=="__main__":raise SystemExit(main())
