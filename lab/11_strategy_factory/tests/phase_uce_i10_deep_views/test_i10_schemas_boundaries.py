from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
def test_i10_schemas_are_closed_objects():
    files=list((ROOT/'schemas/v3').glob('*deep*.schema.json'))+list((ROOT/'schemas/v3').glob('raster_artifact.schema.json'))+list((ROOT/'schemas/v3').glob('graph_artifact.schema.json'))+list((ROOT/'schemas/v3').glob('fusion_prediction.schema.json'))+list((ROOT/'schemas/v3').glob('regime_novelty_prediction.schema.json'))+list((ROOT/'schemas/v3').glob('distillation_report.schema.json'))+list((ROOT/'schemas/v3').glob('quantization_report.schema.json'))
    assert len(files)>=10
    for f in files:
        o=json.loads(f.read_text());assert o['type']=='object';assert o['additionalProperties'] is False
def test_mql5_deep_contracts_have_no_execution_authority():
    root=ROOT.parents[1]/'mql5/Include/AlphaLab/StrategyFactory/DeepViews';text='\n'.join(p.read_text() for p in root.glob('*.mqh'))
    for forbidden in ('OrderSend','OrderCheck','CTrade','PositionOpen'):assert forbidden not in text
    compact=''.join(text.split())
    assert 'Count(){return17;}' in compact
    assert 'NativeCount(){return10;}' in compact
