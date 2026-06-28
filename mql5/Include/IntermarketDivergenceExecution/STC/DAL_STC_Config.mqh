#ifndef __DAL_STC_CONFIG_MQH__
#define __DAL_STC_CONFIG_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_Time.mqh>

string STC_ConfigOneLine(STC_Config &cfg)
{
   return "strategy=" + cfg.strategy_id
      + "*run=" + cfg.run_id
      + "*mode=" + STC_RuntimeModeText(cfg.runtime_mode)
      + "*symbol1=" + cfg.symbol1
      + "*symbol2=" + cfg.symbol2
      + "*entrySTC=" + STC_BoolText(cfg.entry_stc_enabled)
      + "*partial=" + STC_BoolText(cfg.partial_enabled)
      + "*hedging=" + STC_BoolText(cfg.hedging_enabled)
      + "*finalRewardR=" + DoubleToString(cfg.final_reward_r, 2)
      + "*riskPercent=" + DoubleToString(cfg.risk_percent, 4)
      + "*checkTf=" + STC_CheckTfText(cfg.check_tf)
      + "*contractSize=" + DoubleToString(cfg.contract_size, 2)
      + "*brokerUtcOffsetHours=" + DoubleToString(cfg.broker_utc_offset_hours, 2)
      + "*timerSeconds=" + IntegerToString(cfg.timer_seconds)
      + "*magic=" + IntegerToString(cfg.magic_number)
      + "*outputRootCommon=" + cfg.output_root_common
      + "*instanceLock=" + STC_BoolText(cfg.use_instance_lock)
      + "*drawing=" + STC_BoolText(cfg.enable_drawing)
      + "*costsForReporting=" + STC_BoolText(cfg.use_broker_costs_for_reporting)
      + "*timeAudit=" + STC_BoolText(cfg.write_time_audit)
      + "*timeAuditSeconds=" + IntegerToString(cfg.time_audit_seconds);
}

string STC_LockedRulesOneLine()
{
   return "touchEquality=true"
      + "*huntTolerance=none"
      + "*dayTimezone=America/New_York"
      + "*nyDst=automatic_US_rules"
      + "*tradingDay=20:00_to_15:30_NY"
      + "*M1=20:00_02:00"
      + "*M2=03:00_09:00"
      + "*M3=09:30_15:30"
      + "*gaps=no_entry_no_detection_but_positions_managed"
      + "*checkCandles=anchored_from_20:00_NY"
      + "*lastCheckOfM=no_entry"
      + "*W1=no_signal"
      + "*W2refs=W1"
      + "*W3refs=W2_W1"
      + "*W4refs=W3_W2_W1"
      + "*comparison=structural_per_symbol"
      + "*highSMT=sell_clean_symbol"
      + "*lowSMT=buy_clean_symbol"
      + "*entryBacktest=next_check_open"
      + "*referenceSelector=largest_stop_on_clean_symbol"
      + "*simultaneousBuySell=forget_no_trade"
      + "*entryOff=audit_only_no_late_entry"
      + "*orderFail=signal_consumed_counter_unchanged"
      + "*maxTrades=3_per_M_across_pair"
      + "*hardClose=15:30_NY_magic_only_retry"
      + "*autoTrade=disabled_in_level02";
}

void STC_PrintConfig(STC_Config &cfg)
{
   Print("DAL_STC_LEVEL02_CONFIG *** ", STC_ConfigOneLine(cfg));
   Print("DAL_STC_LEVEL02_LOCKED_RULES *** ", STC_LockedRulesOneLine());
}

#endif
