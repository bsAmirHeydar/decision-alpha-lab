#property strict
#property version   "1.00"
#property description "Decision Alpha Lab - EXEC001 STC SMT Cycles - Level 01 skeleton"
#property description "Level 01 creates the modular execution shell only: inputs, validation, journal, timer, lock. No signals. No orders."

#include <IntermarketDivergenceExecution/STC/DAL_STC_Engine.mqh>

input group "DAL / STC Level 01 Runtime"
input STC_RuntimeMode InpRuntimeMode = STC_MODE_RESEARCH_BACKTEST;
input string InpRunId = "EXEC001_STC_LEVEL01";
input int InpTimerSeconds = 10;
input bool InpWriteHeartbeat = true;
input int InpHeartbeatSeconds = 60;
input string InpOutputRootCommon = "dal/stc/EXEC001_STC_SMT_Cycles";

input group "STC Symbols"
input string InpSymbol1 = "SPXUSD";
input string InpSymbol2 = "NDXUSD";
input bool InpStrictSymbolValidation = false;

input group "STC Strategy Switches"
input bool InpEntrySTC = true;
input bool InpPartial = true;
input bool InpHedging = false;
input bool InpEnableDrawing = true;

input group "STC Locked Risk Inputs"
input double InpFinalRewardR = 10.0;
input double InpRiskPercent = 0.50;
input STC_CandleCheckTf InpCandleCheck = STC_CHECK_M5;
input double InpContractSize = 10.0;
input double InpBrokerUtcOffsetHours = 0.0;
input long InpMagicNumber = 16001001;

input group "STC Reporting Costs"
input bool InpUseBrokerCostsForReporting = true;
input double InpFallbackSpreadPoints = 0.0;
input double InpFallbackCommissionPerLot = 0.0;

input group "STC Safety"
input bool InpUseDuplicateInstanceLock = true;
input int InpInstanceLockStaleSeconds = 120;
input int InpHardCloseRetrySeconds = 5;

CSTC_Engine g_stc_engine;

void STC_LoadInputsIntoConfig(STC_Config &cfg)
{
   STC_ResetConfig(cfg);
   cfg.strategy_id = "EXEC001_STC_SMT_Cycles";
   cfg.run_id = InpRunId;
   cfg.runtime_mode = InpRuntimeMode;
   cfg.symbol1 = InpSymbol1;
   cfg.symbol2 = InpSymbol2;
   cfg.entry_stc_enabled = InpEntrySTC;
   cfg.partial_enabled = InpPartial;
   cfg.hedging_enabled = InpHedging;
   cfg.final_reward_r = InpFinalRewardR;
   cfg.risk_percent = InpRiskPercent;
   cfg.check_tf = InpCandleCheck;
   cfg.check_minutes = (int)InpCandleCheck;
   cfg.contract_size = InpContractSize;
   cfg.broker_utc_offset_hours = InpBrokerUtcOffsetHours;
   cfg.timer_seconds = InpTimerSeconds;
   cfg.magic_number = InpMagicNumber;
   cfg.output_root_common = InpOutputRootCommon;
   cfg.use_instance_lock = InpUseDuplicateInstanceLock;
   cfg.instance_lock_stale_seconds = InpInstanceLockStaleSeconds;
   cfg.strict_symbol_validation = InpStrictSymbolValidation;
   cfg.enable_drawing = InpEnableDrawing;
   cfg.write_heartbeat = InpWriteHeartbeat;
   cfg.heartbeat_seconds = InpHeartbeatSeconds;
   cfg.hard_close_retry_seconds = InpHardCloseRetrySeconds;
   cfg.use_broker_costs_for_reporting = InpUseBrokerCostsForReporting;
   cfg.fallback_spread_points = InpFallbackSpreadPoints;
   cfg.fallback_commission_per_lot = InpFallbackCommissionPerLot;
}

int OnInit()
{
   STC_Config cfg;
   STC_LoadInputsIntoConfig(cfg);
   g_stc_engine.Configure(cfg);

   if(!g_stc_engine.Init())
      return INIT_FAILED;

   int seconds = InpTimerSeconds;
   if(seconds < 1) seconds = 1;
   EventSetTimer(seconds);
   return INIT_SUCCEEDED;
}

void OnTimer()
{
   g_stc_engine.Pulse(TimeCurrent());
}

void OnTick()
{
   // Level 01 is intentionally timer-driven and does not inspect ticks.
   // Later levels will add STC day/cycle logic, check-candle aggregation, SMT, paper execution, and auto-trading.
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   g_stc_engine.Deinit(reason);
}
