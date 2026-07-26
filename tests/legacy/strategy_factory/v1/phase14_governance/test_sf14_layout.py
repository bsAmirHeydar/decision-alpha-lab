from tools.repository_paths import find_repository_root
from pathlib import Path

def test_phase14_required_layout_exists():
    root=find_repository_root(__file__)
    required=[
      "mql5/Include/AlphaLab/StrategyFactory/Governance/SF14_AllGovernance.mqh",
      "mql5/Experts/StrategyFactory/SF14_ModelGovernanceHost.mq5",
      "mql5/Tests/Experts/StrategyFactory/SF14_GovernanceSelfTest.mq5",
      "docs/history/systems/strategy_factory_implementation/phase14/00_PHASE_14_MOC.md",
      "releases/history/strategy_factory/program/implementation/phase_status/PHASE_14_HANDOFF_TO_PHASE_15.json",
    ]
    for rel in required:assert (root/rel).is_file(),rel
