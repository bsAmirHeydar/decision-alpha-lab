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
      + "*drawingAudit=" + STC_BoolText(cfg.write_drawing_audit)
      + "*drawingRefreshSeconds=" + IntegerToString(cfg.drawing_refresh_seconds)
      + "*drawingHistoryChecks=" + IntegerToString(cfg.drawing_history_checks)
      + "*drawingHistoryWLevels=" + IntegerToString(cfg.drawing_history_w_levels)
      + "*drawingClearOnDeinit=" + STC_BoolText(cfg.drawing_clear_on_deinit)
      + "*drawingObjectPrefix=" + cfg.drawing_object_prefix
      + "*paperLiveAlerts=" + STC_BoolText(cfg.enable_paper_live_alerts)
      + "*alertAudit=" + STC_BoolText(cfg.write_alert_audit)
      + "*alertPopup=" + STC_BoolText(cfg.alert_popup)
      + "*alertPush=" + STC_BoolText(cfg.alert_push)
      + "*alertSound=" + STC_BoolText(cfg.alert_sound)
      + "*alertPrint=" + STC_BoolText(cfg.alert_print)
      + "*alertSoundFile=" + cfg.alert_sound_file
      + "*alertDebounceSeconds=" + IntegerToString(cfg.alert_debounce_seconds)
      + "*alertOnSignal=" + STC_BoolText(cfg.alert_on_signal)
      + "*alertOnPaperEntry=" + STC_BoolText(cfg.alert_on_paper_entry)
      + "*alertOnOutcome=" + STC_BoolText(cfg.alert_on_outcome)
      + "*alertOnPartial=" + STC_BoolText(cfg.alert_on_partial)
      + "*alertOnHardClose=" + STC_BoolText(cfg.alert_on_hard_close)
      + "*alertOnAmbiguous=" + STC_BoolText(cfg.alert_on_ambiguous)
      + "*alertOnHardCloseDue=" + STC_BoolText(cfg.alert_on_hard_close_due)
      + "*alertReplayOnInit=" + STC_BoolText(cfg.alert_replay_on_init)
      + "*brokerPositionManager=" + STC_BoolText(cfg.enable_broker_position_manager)
      + "*brokerPositionAudit=" + STC_BoolText(cfg.write_broker_position_audit)
      + "*brokerPositionScanSeconds=" + IntegerToString(cfg.broker_position_scan_seconds)
      + "*realHardClose=" + STC_BoolText(cfg.enable_real_hard_close)
      + "*allowRealCloseInPaperLive=" + STC_BoolText(cfg.allow_real_close_in_paper_live)
      + "*brokerCloseDeviationPoints=" + IntegerToString(cfg.broker_close_deviation_points)
      + "*auditForeignPairPositions=" + STC_BoolText(cfg.audit_foreign_pair_positions)
      + "*enableRealAutoEntry=" + STC_BoolText(cfg.enable_real_auto_entry)
      + "*autoEntryAudit=" + STC_BoolText(cfg.write_auto_entry_audit)
      + "*autoEntryGraceSeconds=" + IntegerToString(cfg.auto_entry_grace_seconds)
      + "*autoEntryDeviationPoints=" + IntegerToString(cfg.auto_entry_deviation_points)
      + "*maxAutoSplitOrders=" + IntegerToString(cfg.max_auto_split_orders)
      + "*allowAutoEntryInPaperLive=" + STC_BoolText(cfg.allow_auto_entry_in_paper_live)
      + "*autoEntryRequiresBrokerManager=" + STC_BoolText(cfg.auto_entry_requires_broker_manager)
      + "*autoEntryOrderCommentPrefix=" + cfg.auto_entry_order_comment_prefix
      + "*enableRealPartialClose=" + STC_BoolText(cfg.enable_real_partial_close)
      + "*realPartialAudit=" + STC_BoolText(cfg.write_real_partial_audit)
      + "*realPartialScanSeconds=" + IntegerToString(cfg.real_partial_scan_seconds)
      + "*realPartialDeviationPoints=" + IntegerToString(cfg.real_partial_deviation_points)
      + "*allowRealPartialInPaperLive=" + STC_BoolText(cfg.allow_real_partial_in_paper_live)
      + "*realPartialRequiresBrokerManager=" + STC_BoolText(cfg.real_partial_requires_broker_manager)
      + "*costsForReporting=" + STC_BoolText(cfg.use_broker_costs_for_reporting)
      + "*timeAudit=" + STC_BoolText(cfg.write_time_audit)
      + "*timeAuditSeconds=" + IntegerToString(cfg.time_audit_seconds)
      + "*checkCandleAudit=" + STC_BoolText(cfg.write_check_candle_audit)
      + "*maxCheckBackfillOnInit=" + IntegerToString(cfg.max_check_backfill_on_init)
      + "*maxCheckCatchupPerPulse=" + IntegerToString(cfg.max_check_catchup_per_pulse)
      + "*wLevelAudit=" + STC_BoolText(cfg.write_w_level_audit)
      + "*maxWLevelBackfillOnInit=" + IntegerToString(cfg.max_w_level_backfill_on_init)
      + "*maxWLevelCatchupPerPulse=" + IntegerToString(cfg.max_w_level_catchup_per_pulse)
      + "*huntAudit=" + STC_BoolText(cfg.write_hunt_audit)
      + "*maxHuntBackfillOnInit=" + IntegerToString(cfg.max_hunt_backfill_on_init)
      + "*maxHuntCatchupPerPulse=" + IntegerToString(cfg.max_hunt_catchup_per_pulse)
      + "*smtCandidateAudit=" + STC_BoolText(cfg.write_smt_candidate_audit)
      + "*maxSmtBackfillOnInit=" + IntegerToString(cfg.max_smt_backfill_on_init)
      + "*maxSmtCatchupPerPulse=" + IntegerToString(cfg.max_smt_catchup_per_pulse)
      + "*signalRegistryAudit=" + STC_BoolText(cfg.write_signal_registry_audit)
      + "*maxSignalBackfillOnInit=" + IntegerToString(cfg.max_signal_backfill_on_init)
      + "*maxSignalCatchupPerPulse=" + IntegerToString(cfg.max_signal_catchup_per_pulse)
      + "*paperEntryAudit=" + STC_BoolText(cfg.write_paper_entry_audit)
      + "*maxPaperEntryBackfillOnInit=" + IntegerToString(cfg.max_paper_entry_backfill_on_init)
      + "*maxPaperEntryCatchupPerPulse=" + IntegerToString(cfg.max_paper_entry_catchup_per_pulse)
      + "*paperOutcomeAudit=" + STC_BoolText(cfg.write_paper_outcome_audit)
      + "*maxPaperOutcomeBackfillOnInit=" + IntegerToString(cfg.max_paper_outcome_backfill_on_init)
      + "*maxPaperOutcomeCatchupPerPulse=" + IntegerToString(cfg.max_paper_outcome_catchup_per_pulse)
      + "*maxPaperOutcomeForwardChecks=" + IntegerToString(cfg.max_paper_outcome_forward_checks)
      + "*partialAudit=" + STC_BoolText(cfg.write_partial_audit)
      + "*maxPartialBackfillOnInit=" + IntegerToString(cfg.max_partial_backfill_on_init)
      + "*maxPartialCatchupPerPulse=" + IntegerToString(cfg.max_partial_catchup_per_pulse)
      + "*hardCloseAudit=" + STC_BoolText(cfg.write_hard_close_audit)
      + "*maxHardCloseBackfillOnInit=" + IntegerToString(cfg.max_hard_close_backfill_on_init)
      + "*maxHardCloseCatchupPerPulse=" + IntegerToString(cfg.max_hard_close_catchup_per_pulse)
      + "*restorePersistenceOnInit=" + STC_BoolText(cfg.restore_persistence_on_init)
      + "*writePersistenceSnapshot=" + STC_BoolText(cfg.write_persistence_snapshot)
      + "*persistenceSnapshotSeconds=" + IntegerToString(cfg.persistence_snapshot_seconds);
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
      + "*m1Aggregation=from_symbol_M1"
      + "*pairCompleteness=both_symbols_required"
      + "*gapCheckCandles=no_data_extraction"
      + "*finalCheck=audited_but_no_entry"
      + "*wLevels=closed_90m_levels_from_symbol_M1_per_symbol*W1_level_built_but_no_signal*W2_refs=W1*W3_refs=W2_W1*W4_refs=W3_W2_W1"
      + "*rawHunts=touch_only_equality_valid*referenceMatrix=previous_W_only_same_M*W1_no_reference*W2_ref_W1*W3_ref_W2_then_W1*W4_ref_W3_then_W2_then_W1"
      + "*huntLayer=raw_audit_only*SMTLevel=convert_exactly_one_hunts_to_candidates*highCandidate=sell_clean_symbol*lowCandidate=buy_clean_symbol*sameCheckBuySell=forget_no_trade_consumed_no_carry*referenceSelection=largest_stop_distance_on_clean_symbol_using_check_close_proxy*signalRegistry=confirm_closed_check_candidates_consume_audit_only*entryOff=confirmed_signal_consumed_no_late_entry*missedEntry=never_enter_late*orderAttempt=level16_real_auto_entry_gated*paperEntry=next_check_open_no_order*riskPlan=SL_reference_TP_FinalRewardR*volume=theoretical_tick_value_or_contract_size*maxTrades=paper_counter_3_per_M*paperOutcome=simulate_check_stream_SL_TP_ambiguous_same_check*partialSimulator=W4_end_M1_M2_only_50pct_ceil_step_delayed_recovery*M3_partial=disabled_by_hard_close*hardCloseSimulator=1530_NY_force_close_open_paper_remainder_delayed_recovery*persistence=level12_snapshot_restore_current_day_cursors_counters_locks*drawing=level13_audit_only_chart_objects_no_decision_effect*brokerPositionManager=level15_magic_only_scan_optional_hard_close*autoEntry=level16_gated_real_order_router_disabled_by_default*realPartial=level17_magic_only_W4_M1_M2_50pct_ceil_step_marker_dedup_disabled_by_default";
}


void STC_PrintConfig(STC_Config &cfg)
{
   Print("DAL_STC_LEVEL17_CONFIG *** ", STC_ConfigOneLine(cfg));
   Print("DAL_STC_LEVEL17_LOCKED_RULES *** ", STC_LockedRulesOneLine());
}

#endif
