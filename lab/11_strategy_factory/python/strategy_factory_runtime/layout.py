from __future__ import annotations
from pathlib import Path

REQUIRED_PATHS = (
    "mql5/Include/AlphaLab/StrategyFactory/Contracts",
    "mql5/Include/AlphaLab/StrategyFactory/Core",
    "mql5/Include/AlphaLab/StrategyFactory/Ports",
    "mql5/Include/AlphaLab/StrategyFactory/Runtime",
    "mql5/Include/AlphaLab/StrategyFactory/Adapters/Null",
    "mql5/Include/AlphaLab/StrategyFactory/Testing",
    "mql5/Experts/StrategyFactory/SF02_StrategyHost.mq5",
    "mql5/Experts/StrategyFactoryTests/SF02_RuntimeSelfTest.mq5",
)

def missing_paths(repo_root: Path) -> list[str]:
    return [p for p in REQUIRED_PATHS if not (repo_root / p).exists()]
