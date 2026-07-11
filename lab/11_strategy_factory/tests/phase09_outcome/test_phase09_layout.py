from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def test_mql5_outcome_files_exist():
    b=ROOT/"mql5/Include/AlphaLab/StrategyFactory/Outcome";required=["SF09_AllOutcome.mqh","SF09_OutcomeEngine.mqh","SF09_OutcomeRecord.mqh","SF09_CostModel.mqh","SF09_PathTracker.mqh"]
    assert all((b/x).exists() for x in required)
def test_no_execution_authority():
    paths=list((ROOT/"mql5/Include/AlphaLab/StrategyFactory/Outcome").rglob("*.mqh"))+list((ROOT/"mql5/Experts/StrategyFactory").glob("SF09_*.mq5"))+list((ROOT/"mql5/Experts/StrategyFactoryTests").glob("SF09_*.mq5"))
    text="\n".join(p.read_text(encoding="utf-8") for p in paths);assert not any(x in text for x in ["OrderSend(","OrderCheck(","CTrade","PositionOpen(","CopyRates(","LongToString("])
def test_schemas_exist():
    b=ROOT/"lab/11_strategy_factory/schemas/v1";assert all((b/x).exists() for x in ["price_observation.schema.json","simulation_policy.schema.json","cost_model_descriptor.schema.json","outcome_record.schema.json","outcome_run_manifest.schema.json"])
