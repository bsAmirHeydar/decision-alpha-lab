from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
def test_generated_hash_binding(output):
 s=(ROOT/'mql5/Include/StrategyFactory/SAED/V4_38/SAEDV438CompiledRuntime.mqh').read_text(); assert output['runtime_bundle']['bundle_hash'] in s
def test_generated_no_trade_api():
 files=list((ROOT/'mql5/Include/StrategyFactory/SAED/V4_38').rglob('*'))+list((ROOT/'mql5/Experts/StrategyFactory/SAED/V4_38').rglob('*'))
 text='\n'.join(p.read_text() for p in files if p.is_file())
 for token in ['OrderSend(','CTrade','trade.Buy','trade.Sell','PositionOpen(','WebRequest(','ShellExecute']:assert token not in text
def test_generated_feature_count():
 s=(ROOT/'mql5/Include/StrategyFactory/SAED/V4_38/SAEDV438CompiledRuntime.mqh').read_text(); assert '#define SAED_V4_38_FEATURE_COUNT 12' in s
def test_harness_non_executable():
 s=(ROOT/'mql5/Experts/StrategyFactory/SAED/V4_38/SAEDV438ParityHarness.mq5').read_text(); assert 'no order' in s.lower()
