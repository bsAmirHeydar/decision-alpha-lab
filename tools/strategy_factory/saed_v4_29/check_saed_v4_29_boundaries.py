from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; targets=[ROOT/"lab/11_strategy_factory/python/saed_v4_hidden_evaluation_air_gap",ROOT/"tools/strategy_factory/saed_v4_29",ROOT/"mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_29"]
forbidden=["send_order(","ordersend(","positionopen(","promotion_authority = true","production_authority = true","runtime_executable = true","hidden_label_access = true","network_access = true"]
hits=[]
for d in targets:
    for p in d.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".py",".mqh",".mq5"} and p.name != "check_saed_v4_29_boundaries.py":
            low=p.read_text(encoding="utf-8").lower()
            for token in forbidden:
                if token in low: hits.append((str(p.relative_to(ROOT)),token))
assert not hits,hits
print("V4-29 authority and security boundaries passed")
