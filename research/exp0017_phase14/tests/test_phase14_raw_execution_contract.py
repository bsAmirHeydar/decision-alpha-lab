from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
EA = ROOT / "mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Raw_Execution_Backtest.mq5"
MOD = ROOT / "mql5/Include/IntermarketDivergenceExecution/CG/Execution"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_default_profile_is_protected_cg3_atr_one():
    source = text(EA)
    assert "InpTradeLeg = CGX_TRADE_PROTECTED_SYMBOL" in source
    assert "InpATRPeriod = 14" in source
    assert "InpATRMultiplier = 1.0" in source
    assert "InpRequireHedgingAccount = true" in source
    assert "InpMaxQuoteAgeSeconds = 0" in source
    assert "InpTrade_cg_3m   = true" in source
    disabled = re.findall(r"input bool InpTrade_cg_(?!3m)[^=]+?= false;", source)
    assert len(disabled) == 20


def test_closed_candle_is_half_open_and_exact():
    source = text(MOD / "CGX_ClosedCandle.mqh")
    assert "expected_open=(datetime)(close_time_broker-seconds)" in source
    assert "CopyRates(symbol,timeframe,expected_open,close_time_broker-1,rates)" in source
    assert "copied!=1" in source
    assert "rates[0].time!=expected_open" in source


def test_stop_is_behind_selected_trade_symbol_confirmation_candle():
    source = text(MOD / "CGX_StopModel.mqh")
    assert "stop_loss=candle.low-(buffer_points*point)" in source
    assert "stop_loss=candle.high+(buffer_points*point)" in source
    planner = text(MOD / "CGX_TradePlanner.mqh")
    assert "m_candle_provider.Build(plan.trade_symbol" in planner


def test_atr_target_uses_closed_history_and_wilder_smoothing():
    source = text(MOD / "CGX_TargetModelATR.mqh")
    assert "confirmation_close-1" in source
    assert "value=((value*(period-1))+tr)/period" in source
    assert "take_profit=entry_price+distance" in source
    assert "take_profit=entry_price-distance" in source


def test_signal_source_reuses_hotfix_confirmation_authority():
    source = text(MOD / "CGX_SignalSource.mqh")
    assert "#include <IntermarketDivergenceExecution/CG/CGC_ConfirmationField.mqh>" in source
    assert source.index("CGC_ConfirmationField.mqh") < source.index("class CCGX_SignalSource")
    assert "CCGC_ConfirmationField m_confirmation_field" in source
    assert "BuildFinalSignalsForGroup" in source
    assert "HasM1HistoryBounds(m_confirmation_config.symbol_a" in source
    assert "HasM1HistoryBounds(m_confirmation_config.symbol_b" in source


def test_attempt_is_registered_before_plan_and_router():
    source = text(MOD / "CGX_Engine.mqh")
    registry = source.index("m_registry.RegisterAttempt(signals[i].signal_id")
    planner = source.index("m_planner.Build(signals[i]")
    router = source.index("m_router.Execute(plan,result)")
    assert registry < planner < router


def test_transport_isolated_and_backtest_guarded():
    router = text(MOD / "CGX_OrderRouter.mqh")
    assert "CGX_RUNTIME_BACKTEST_ONLY" in router
    assert "CGX_IsTesterRuntime" in router
    assert "m_trade.Buy" in router
    assert "m_trade.Sell" in router
    for path in MOD.glob("*.mqh"):
        if path.name == "CGX_OrderRouter.mqh":
            continue
        assert "CTrade" not in text(path)
    assert "CTrade" not in text(EA)


def test_ea_is_orchestration_only():
    source = text(EA)
    assert "CopyRates(" not in source
    assert "OrderCalcProfit(" not in source
    assert ".Buy(" not in source
    assert ".Sell(" not in source
