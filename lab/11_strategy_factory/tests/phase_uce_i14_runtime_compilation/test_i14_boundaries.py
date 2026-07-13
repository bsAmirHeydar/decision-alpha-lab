from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def test_runtime_package_contains_no_broker_or_network_imports():
    banned=('MetaTrader5','import requests','from requests','import socket','from socket','urllib.request','OrderSend(','trade.PositionOpen')
    for p in (ROOT/'lab/11_strategy_factory/python/strategy_factory_runtime_v3').glob('*.py'):
        text=p.read_text()
        for token in banned:assert token not in text,f'{token} in {p}'
def test_mql5_runtime_has_no_ordersend_outside_isolated_adapter():
    base=ROOT/'mql5/Include/AlphaLab/StrategyFactory/ImmutableRuntime'
    for p in base.glob('*.mqh'):assert 'OrderSend(' not in p.read_text()
def test_pyproject_registers_runtime_cli_and_package():
    text=(ROOT/'lab/11_strategy_factory/python/pyproject.toml').read_text();assert 'strategy-factory-runtime-v3' in text;assert 'strategy_factory_runtime_v3*' in text
