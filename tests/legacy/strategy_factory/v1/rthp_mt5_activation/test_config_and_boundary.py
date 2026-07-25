from pathlib import Path
import pytest
from strategy_factory_rthp_mt5_activation_v1.config import load_mt5_activation_config

def test_config_enforces_m1_floor(config_path:Path):
    c=load_mt5_activation_config(config_path); assert c.quality.reject_sub_m1 is True; assert c.primary_symbol!=c.secondary_symbol

def test_no_trade_calls_exist(repo_root:Path):
    root=repo_root/'src/engine/packages/strategy_factory_rthp_mt5_activation_v1'
    text='\n'.join(p.read_text(encoding='utf-8') for p in root.glob('*.py'))
    for forbidden in ('order_send(', 'CTrade', 'positions_get(', 'orders_get('): assert forbidden not in text


def test_symbol_selection_config_uses_m1_floor(tmp_path):
    from strategy_factory_rthp_mt5_activation_v1.config import build_symbol_selection_config
    config = build_symbol_selection_config("A", "B", tmp_path / "run", lookback_days=60, minimum_common_days=30)
    assert config.primary_symbol == "A" and config.secondary_symbol == "B"
    assert config.quality.reject_sub_m1 is True
    assert config.history.mode == "AUTO_COMMON_HISTORY"
    assert config.output_root == (tmp_path / "run").resolve()

def test_symbol_only_cli_is_registered():
    from strategy_factory_rthp_mt5_activation_v1.cli import parser
    args = parser().parse_args(["run-symbols", "--primary", "A", "--secondary", "B", "--no-train"])
    assert args.command == "run-symbols" and args.primary == "A" and args.secondary == "B"


def test_provider_surface_is_read_only():
    from strategy_factory_rthp_mt5_activation_v1.provider import MetaTrader5Provider, MT5Provider
    forbidden = {"order_send", "positions_get", "orders_get", "history_deals_get"}
    assert forbidden.isdisjoint(set(dir(MetaTrader5Provider)))
    assert forbidden.isdisjoint(set(getattr(MT5Provider, "__annotations__", {})))
