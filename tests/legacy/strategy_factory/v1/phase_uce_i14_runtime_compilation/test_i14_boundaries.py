from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
def test_runtime_package_contains_no_broker_or_network_imports():
    banned=('MetaTrader5','import requests','from requests','import socket','from socket','urllib.request','OrderSend(','trade.PositionOpen')
    for p in (ROOT/'src/engine/packages/strategy_factory_runtime_v3').glob('*.py'):
        text=p.read_text()
        for token in banned:assert token not in text,f'{token} in {p}'
def test_mql5_runtime_has_no_ordersend_outside_isolated_adapter():
    base=ROOT/'mql5/Include/AlphaLab/StrategyFactory/ImmutableRuntime'
    for p in base.glob('*.mqh'):assert 'OrderSend(' not in p.read_text()
def test_pyproject_registers_runtime_cli_and_package():
    text=(ROOT/'src/engine/packages/pyproject.toml').read_text();assert 'strategy-factory-runtime-v3' in text;assert 'strategy_factory_runtime_v3*' in text
