import json
from pathlib import Path
from strategy_factory_contracts_v3.fixtures import build_cross_language_vectors

def test_checked_in_vectors_equal_implementation():
    root=Path(__file__).resolve().parents[4]
    path=root/"lab/11_strategy_factory/test_vectors/v3/uce_i01_cross_language_vectors.json"
    assert json.loads(path.read_text())==build_cross_language_vectors()

def test_all_v3_schemas_are_parseable_and_closed_objects():
    root=Path(__file__).resolve().parents[4]
    schema_dir=root/"lab/11_strategy_factory/schemas/v3"
    paths=list(schema_dir.glob("*.schema.json"));assert len(paths)>=10
    for path in paths:
        data=json.loads(path.read_text());assert data["$schema"].endswith("2020-12/schema");assert data["additionalProperties"] is False

def test_required_mql5_headers_and_eas_exist():
    root=Path(__file__).resolve().parents[4]
    headers=root/"mql5/Include/AlphaLab/StrategyFactory/Contracts"
    required=["UCE03_AllContracts.mqh","UCE03_Identity.mqh","UCE03_KnownTime.mqh","UCE03_SchemaRegistry.mqh","UCE03_Compatibility.mqh"]
    assert all((headers/name).is_file() for name in required)
    assert (root/"mql5/Experts/StrategyFactoryTests/UCE_I01_ContractsV3SelfTest.mq5").is_file()
