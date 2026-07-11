import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def test_schemas_parse():
    for n in ('run_manifest','runtime_generation','result_envelope'):json.loads((ROOT/'lab/11_strategy_factory/schemas/v1'/f'{n}.schema.json').read_text())
def test_mql5_generation_headers_present():
    p=ROOT/'mql5/Include/AlphaLab/StrategyFactory/Generation';assert len(list(p.glob('*.mqh')))>=12

def test_no_live_authority_in_phase05():
    roots=[ROOT/'mql5/Include/AlphaLab/StrategyFactory/Generation',ROOT/'mql5/Experts/StrategyFactory/SF05_StrategyHost.mq5']
    bad=re.compile(r'(?<![A-Za-z0-9_])(OrderSend|OrderCheck|CTrade|PositionOpen)\s*\(')
    for r in roots:
        files=[r] if r.is_file() else list(r.rglob('*.*'))
        for f in files:
            if f.suffix in {'.mqh','.mq5'}:assert not bad.search(f.read_text()),f

def test_generation_layer_has_no_strategy_specific_tokens():
    text='\n'.join(f.read_text() for f in (ROOT/'mql5/Include/AlphaLab/StrategyFactory/Generation').glob('*.mqh')).lower()
    for token in ('hookafterf3','nds_zone','temporal_divergence','daye_anatomy','ict_anatomy'):assert token not in text
