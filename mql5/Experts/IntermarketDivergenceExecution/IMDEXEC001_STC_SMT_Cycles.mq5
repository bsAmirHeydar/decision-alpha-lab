#property strict
#property version   "1.20"
#property description "Decision Alpha Lab - EXEC001 STC SMT Cycles - Level 03 check candle aggregator"
#property description "Level 03 adds M1-based check-candle aggregation and pair completeness audit. No SMT signals. No orders."

#include <IntermarketDivergenceExecution/STC/DAL_STC_Engine.mqh>

input group "DAL / STC Level 03 Runtime"
input STC_RuntimeMode InpRuntimeMode = STC_MODE_RESEARCH_BACKTEST;
input string InpRunId = "EXEC001_STC_LEVEL03";
input int InpTimerSeconds = 10;
input bool InpWriteHeartbeat = true;
input int InpHeartbeatSeconds = 60;
input bool InpWriteTimeAudit = true;
input int InpTimeAuditSeconds = 60;
input bool InpWriteCheckCandleAudit = true;
input int InpMaxCheckBackfillOnInit = 12;
input int InpMaxCheckCatchupPerPulse = 32;
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
   cfg.write_time_audit = InpWriteTimeAudit;
   cfg.time_audit_seconds = InpTimeAuditSeconds;
   cfg.write_check_candle_audit = InpWriteCheckCandleAudit;
   cfg.max_check_backfill_on_init = InpMaxCheckBackfillOnInit;
   cfg.max_check_catchup_per_pulse = InpMaxCheckCatchupPerPulse;
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
   // Level 03 remains timer-driven for audit and does not inspect ticks for signal decisions.
   // Later levels will add W level construction, SMT, paper execution, drawing, and auto-trading.
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   g_stc_engine.Deinit(reason);
}
