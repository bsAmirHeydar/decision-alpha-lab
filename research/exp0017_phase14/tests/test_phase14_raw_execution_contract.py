from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
EA = ROOT / "mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Raw_Execution_Backtest.mq5"
MOD = ROOT / "mql5/Include/IntermarketDivergenceExecution/CG/Execution"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_default_profile_is_protected_cg3_atr_fixed_money_and_hedged():
    source = text(EA)
    assert "InpTradeLeg = CGX_TRADE_PROTECTED_SYMBOL" in source
    assert "InpTargetModel = CGX_TARGET_ATR_MULTIPLE" in source
    assert "InpATRPeriod = 14" in source
    assert "InpATRMultiplier = 1.0" in source
    assert "InpVolumeModel = CGX_VOLUME_FIXED_RISK_MONEY" in source
    assert "InpFixedRiskMoney = 100.0" in source
    assert "InpEnableHedging = true" in source
    assert "InpRequireHedgingAccount = true" in source
    assert "InpDrawExecutedCGSignals = true" in source
    assert "InpTrade_cg_3m   = true" in source
    disabled = re.findall(r"input bool InpTrade_cg_(?!3m)[^=]+?= false;", source)
    assert len(disabled) == 20


def test_closed_candle_is_half_open_and_exact():
    source = text(MOD / "CGX_ClosedCandle.mqh")
    assert "expected_open=(datetime)(close_time_broker-seconds)" in source
    assert "CopyRates(symbol,timeframe,expected_open,close_time_broker-1,rates)" in source
    assert "copied!=1" in source
    assert "rates[0].time!=expected_open" in source


def test_sell_stop_adds_current_spread_and_buy_stop_does_not():
    source = text(MOD / "CGX_StopModel.mqh")
    assert "stop_loss=candle.low-(buffer_points*point)" in source
    assert "config.add_spread_to_sell_stop" in source
    assert "stop_loss=candle.high+(buffer_points*point)+sell_spread" in source
    planner = text(MOD / "CGX_TradePlanner.mqh")
    assert "plan.spread_price=MathMax(0.0,tick.ask-tick.bid)" in planner
    assert "m_stop_model.Build(m_config,candle,signal.direction,plan.planned_entry_price,plan.spread_price" in planner


def test_target_dispatch_supports_atr_and_stop_risk_multiple():
    atr = text(MOD / "CGX_TargetModelATR.mqh")
    risk = text(MOD / "CGX_TargetModelRiskMultiple.mqh")
    dispatcher = text(MOD / "CGX_TargetModel.mqh")
    assert "value=((value*(period-1))+tr)/period" in atr
    assert "atr_value*config.atr_multiplier" in atr
    assert "stop_distance*config.risk_reward_multiple" in risk
    assert "CGX_TARGET_ATR_MULTIPLE" in dispatcher
    assert "CGX_TARGET_RISK_MULTIPLE" in dispatcher


def test_fixed_money_risk_uses_largest_volume_not_exceeding_budget():
    source = text(MOD / "CGX_VolumeModel.mqh")
    assert "CGX_VOLUME_FIXED_RISK_MONEY" in source
    assert "raw_volume=risk_budget/risk_per_lot" in source
    assert "volume=CGX_NormalizeVolumeDown(raw_volume,step)" in source
    assert "planned_loss=risk_per_lot*volume" in source
    assert "planned_loss>risk_budget+tolerance" in source
    assert "planned_loss_exceeds_risk_budget" in source
    assert "risk_capped_volume_below_broker_minimum" in source


def test_hedging_switch_is_enforced_by_router():
    router = text(MOD / "CGX_OrderRouter.mqh")
    engine = text(MOD / "CGX_Engine.mqh")
    assert "HasOwnOppositePosition" in router
    assert "!m_config.enable_hedging" in router
    assert "hedging_disabled_opposite_position_exists" in router
    assert "m_execution_config.enable_hedging && m_execution_config.require_hedging_account" in engine


def test_execution_visuals_only_draw_accepted_trades_and_use_owned_prefix():
    visuals = text(MOD / "CGX_ExecutionVisuals.mqh")
    engine = text(MOD / "CGX_Engine.mqh")
    assert 'CGX_EXECUTION_OBJECT_PREFIX "EXP0017_P14_"' in visuals
    assert "if(!result.sent && !result.paper_only)" in visuals
    assert "DrawDivergenceLeg(signal,m_config.symbol_a)" in visuals
    assert "DrawTradeLevels(plan)" in visuals
    assert "m_visuals.DrawAcceptedExecution(signals[i],plan,result)" in engine


def test_signal_source_reuses_confirmation_authority():
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
