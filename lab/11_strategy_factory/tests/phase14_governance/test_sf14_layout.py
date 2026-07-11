from pathlib import Path

def test_phase14_required_layout_exists():
    root=Path(__file__).resolve().parents[4]
    required=[
      "mql5/Include/AlphaLab/StrategyFactory/Governance/SF14_AllGovernance.mqh",
      "mql5/Experts/StrategyFactory/SF14_ModelGovernanceHost.mq5",
      "mql5/Experts/StrategyFactoryTests/SF14_GovernanceSelfTest.mq5",
      "docs/strategy_factory_implementation/phase14/00_PHASE_14_MOC.md",
      "lab/11_strategy_factory/implementation_program/phase_status/PHASE_14_HANDOFF_TO_PHASE_15.json",
    ]
    for rel in required:assert (root/rel).is_file(),rel
