#property strict
#property version   "2.18"
#property description "Decision Alpha Lab - EXEC001 STC SMT Cycles - Level 22 offline license gate"
#property description "Level 22 hidden-input offline license fix keeps strategy, signal, risk, and transport logic unchanged."

#include <IntermarketDivergenceExecution/STC/DAL_STC_Engine.mqh>
#include <IntermarketDivergenceExecution/STC/DAL_STC_LicenseEngine.mqh>

input group "DAL / STC Level 21 Runtime"
input STC_RuntimeMode InpRuntimeMode = STC_MODE_RESEARCH_BACKTEST;
input string InpRunId = "EXEC001_STC_LEVEL21";
input int InpTimerSeconds = 10;
input bool InpWriteHeartbeat = true;
input int InpHeartbeatSeconds = 60;
input bool InpWriteTimeAudit = true;
input int InpTimeAuditSeconds = 60;
input bool InpWriteCheckCandleAudit = true;
input int InpMaxCheckBackfillOnInit = 12;
input int InpMaxCheckCatchupPerPulse = 32;
input bool InpWriteWLevelAudit = true;
input int InpMaxWLevelBackfillOnInit = 12;
input int InpMaxWLevelCatchupPerPulse = 12;
input bool InpWriteHuntAudit = true;
input int InpMaxHuntBackfillOnInit = 24;
input int InpMaxHuntCatchupPerPulse = 48;
input bool InpWriteSMTCandidateAudit = true;
input int InpMaxSMTBackfillOnInit = 24;
input int InpMaxSMTCatchupPerPulse = 48;
input bool InpWriteSignalRegistryAudit = true;
input int InpMaxSignalBackfillOnInit = 24;
input int InpMaxSignalCatchupPerPulse = 48;
input bool InpWritePaperEntryAudit = true;
input int InpMaxPaperEntryBackfillOnInit = 24;
input int InpMaxPaperEntryCatchupPerPulse = 48;
input bool InpWritePaperOutcomeAudit = true;
input int InpMaxPaperOutcomeBackfillOnInit = 24;
input int InpMaxPaperOutcomeCatchupPerPulse = 24;
input int InpMaxPaperOutcomeForwardChecks = 288;
input bool InpWritePartialAudit = true;
input int InpMaxPartialBackfillOnInit = 24;
input int InpMaxPartialCatchupPerPulse = 24;
input bool InpWriteHardCloseAudit = true;
input int InpMaxHardCloseBackfillOnInit = 24;
input int InpMaxHardCloseCatchupPerPulse = 24;
input bool InpRestorePersistenceOnInit = true;
input bool InpWritePersistenceSnapshot = true;
input int InpPersistenceSnapshotSeconds = 30;
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

input group "STC Cycle Model Runtime Profile"
input string InpCycleModelProfile = "";
input string InpCycleOperatorMemo = "";
input long InpCycleReferenceSeed = 0;
input long InpCycleDivergenceSeed = 0;
input long InpCycleExecutionSeed = 0;
input long InpCycleReleaseSeed = 0;
input int InpCycleCacheDepthMinutes = 15;

input group "STC Level 13 Drawing"
input bool InpWriteDrawingAudit = true;
input int InpDrawingRefreshSeconds = 15;
input int InpDrawingHistoryChecks = 96;
input int InpDrawingHistoryWLevels = 12;
input bool InpDrawingClearOnDeinit = true;
input string InpDrawingObjectPrefix = "DAL_STC_EXEC001";

input group "STC Level 14 Paper Live Alerts"
input bool InpEnablePaperLiveAlerts = true;
input bool InpWriteAlertAudit = true;
input bool InpAlertPopup = true;
input bool InpAlertPush = false;
input bool InpAlertSound = false;
input bool InpAlertPrint = true;
input string InpAlertSoundFile = "alert.wav";
input int InpAlertDebounceSeconds = 2;
input bool InpAlertOnSignal = true;
input bool InpAlertOnPaperEntry = true;
input bool InpAlertOnOutcome = true;
input bool InpAlertOnPartial = true;
input bool InpAlertOnHardClose = true;
input bool InpAlertOnAmbiguous = true;
input bool InpAlertOnHardCloseDue = true;
input bool InpAlertReplayOnInit = false;


input group "STC Level 15 Broker Position Manager"
input bool InpEnableBrokerPositionManager = true;
input bool InpWriteBrokerPositionAudit = true;
input int InpBrokerPositionScanSeconds = 10;
input bool InpEnableRealHardClose = false;
input bool InpAllowRealCloseInPaperLive = false;
input int InpBrokerCloseDeviationPoints = 30;
input bool InpAuditForeignPairPositions = true;

input group "STC Level 16 Real Auto Entry Router"
input bool InpEnableRealAutoEntry = false;
input bool InpWriteAutoEntryAudit = true;
input int InpAutoEntryGraceSeconds = 30;
input int InpAutoEntryDeviationPoints = 30;
input int InpMaxAutoSplitOrders = 20;
input bool InpAllowAutoEntryInPaperLive = false;
input bool InpAutoEntryRequiresBrokerManager = true;
input string InpAutoEntryOrderCommentPrefix = "DAL_STC_EXEC001";


input group "STC Level 17 Real Partial Close Manager"
input bool InpEnableRealPartialClose = false;
input bool InpWriteRealPartialAudit = true;
input int InpRealPartialScanSeconds = 10;
input int InpRealPartialDeviationPoints = 30;
input bool InpAllowRealPartialInPaperLive = false;
input bool InpRealPartialRequiresBrokerManager = true;

input group "STC Level 18 Real Hard Close Finalizer"
input bool InpEnableRealHardCloseFinalizer = false;
input bool InpWriteRealHardCloseFinalizerAudit = true;
input int InpRealHardCloseFinalizerScanSeconds = 5;
input int InpRealHardCloseFinalizerRetrySeconds = 5;
input int InpRealHardCloseFinalizerDeviationPoints = 30;
input int InpRealHardCloseFinalizerMaxAttemptsPerPosition = 200;
input bool InpAllowRealHardCloseFinalizerInPaperLive = false;
input bool InpRealHardCloseFinalizerRequiresBrokerManager = true;
input bool InpRealHardCloseAlertUnclosedPositions = true;


input group "STC Level 21 Validation Pack"
input bool InpEnableValidationPack = true;
input bool InpWriteValidationReports = true;
input bool InpValidationRunOnInit = true;
input bool InpValidationRunOnPulse = false;
input int InpValidationRunSeconds = 300;
input bool InpValidationStrictMode = false;

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

STC_OfflineLicenseConfig g_stc_license_cfg;
STC_OfflineLicenseReport g_stc_license_report;
bool g_stc_license_ok = false;
datetime g_stc_license_next_check = 0;

void STC_LoadOfflineLicenseConfig(STC_OfflineLicenseConfig &cfg)
{
   STC_DefaultOfflineLicenseConfig(cfg);

   // License values intentionally stay behind neutral Cycle Model inputs.
   // Do not add visible license-token inputs here; distribution UX depends on
   // these fields looking like model/runtime metadata.
   cfg.enabled = true;
   cfg.fail_closed = true;
   cfg.bind_account = true;
   cfg.bind_server = true;
   cfg.require_password = true;
   cfg.require_hidden_gates = true;
   cfg.require_expiry = true;
   cfg.product_id = STC_LICENSE_PRODUCT_ID;
   cfg.build_id = "exec001_stc_level22_hidden_fix01";

   cfg.token = InpCycleModelProfile;
   cfg.passphrase = InpCycleOperatorMemo;
   cfg.gate_a = InpCycleReferenceSeed;
   cfg.gate_b = InpCycleDivergenceSeed;
   cfg.gate_c = InpCycleExecutionSeed;
   cfg.gate_d = InpCycleReleaseSeed;

   cfg.check_interval_seconds = InpCycleCacheDepthMinutes * 60;
   if(cfg.check_interval_seconds < 60)
      cfg.check_interval_seconds = 60;

   cfg.print_sanity = true;
   cfg.print_samples = false;
}

bool STC_EnsureOfflineLicense(const bool force_check=false)
{
   datetime now = TimeCurrent();
   if(now <= 0)
      now = TimeTradeServer();
   if(!force_check && g_stc_license_ok && g_stc_license_next_check > 0 && now > 0 && now < g_stc_license_next_check)
      return true;

   STC_LoadOfflineLicenseConfig(g_stc_license_cfg);
   g_stc_license_ok = STC_CheckOfflineLicenseWithReport(g_stc_license_cfg, g_stc_license_report);
   if(g_stc_license_cfg.print_sanity || !g_stc_license_ok)
      STC_PrintOfflineLicenseReport("STC_LICENSE", g_stc_license_report);
   if(g_stc_license_cfg.print_samples && g_stc_license_ok)
      STC_PrintOfflineLicenseSamples("STC_LICENSE", g_stc_license_report);

   datetime checked = g_stc_license_report.checked_at;
   if(checked <= 0)
      checked = now;
   if(checked > 0)
   {
      int recheck_sec = g_stc_license_cfg.check_interval_seconds;
      if(recheck_sec < 60)
         recheck_sec = 60;
      g_stc_license_next_check = checked + recheck_sec;
   }
   else
   {
      g_stc_license_next_check = 0;
   }

   if(!g_stc_license_ok)
      Comment("STC SMT Cycles runtime inactive. Contact issuer.");
   else
      Comment("");
   return g_stc_license_ok;
}

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
   cfg.write_drawing_audit = InpWriteDrawingAudit;
   cfg.drawing_refresh_seconds = InpDrawingRefreshSeconds;
   cfg.drawing_history_checks = InpDrawingHistoryChecks;
   cfg.drawing_history_w_levels = InpDrawingHistoryWLevels;
   cfg.drawing_clear_on_deinit = InpDrawingClearOnDeinit;
   cfg.drawing_object_prefix = InpDrawingObjectPrefix;
   cfg.enable_paper_live_alerts = InpEnablePaperLiveAlerts;
   cfg.write_alert_audit = InpWriteAlertAudit;
   cfg.alert_popup = InpAlertPopup;
   cfg.alert_push = InpAlertPush;
   cfg.alert_sound = InpAlertSound;
   cfg.alert_print = InpAlertPrint;
   cfg.alert_sound_file = InpAlertSoundFile;
   cfg.alert_debounce_seconds = InpAlertDebounceSeconds;
   cfg.alert_on_signal = InpAlertOnSignal;
   cfg.alert_on_paper_entry = InpAlertOnPaperEntry;
   cfg.alert_on_outcome = InpAlertOnOutcome;
   cfg.alert_on_partial = InpAlertOnPartial;
   cfg.alert_on_hard_close = InpAlertOnHardClose;
   cfg.alert_on_ambiguous = InpAlertOnAmbiguous;
   cfg.alert_on_hard_close_due = InpAlertOnHardCloseDue;
   cfg.alert_replay_on_init = InpAlertReplayOnInit;
   cfg.enable_broker_position_manager = InpEnableBrokerPositionManager;
   cfg.write_broker_position_audit = InpWriteBrokerPositionAudit;
   cfg.broker_position_scan_seconds = InpBrokerPositionScanSeconds;
   cfg.enable_real_hard_close = InpEnableRealHardClose;
   cfg.allow_real_close_in_paper_live = InpAllowRealCloseInPaperLive;
   cfg.broker_close_deviation_points = InpBrokerCloseDeviationPoints;
   cfg.audit_foreign_pair_positions = InpAuditForeignPairPositions;
   cfg.enable_real_auto_entry = InpEnableRealAutoEntry;
   cfg.write_auto_entry_audit = InpWriteAutoEntryAudit;
   cfg.auto_entry_grace_seconds = InpAutoEntryGraceSeconds;
   cfg.auto_entry_deviation_points = InpAutoEntryDeviationPoints;
   cfg.max_auto_split_orders = InpMaxAutoSplitOrders;
   cfg.allow_auto_entry_in_paper_live = InpAllowAutoEntryInPaperLive;
   cfg.auto_entry_requires_broker_manager = InpAutoEntryRequiresBrokerManager;
   cfg.auto_entry_order_comment_prefix = InpAutoEntryOrderCommentPrefix;
   cfg.enable_real_partial_close = InpEnableRealPartialClose;
   cfg.write_real_partial_audit = InpWriteRealPartialAudit;
   cfg.real_partial_scan_seconds = InpRealPartialScanSeconds;
   cfg.real_partial_deviation_points = InpRealPartialDeviationPoints;
   cfg.allow_real_partial_in_paper_live = InpAllowRealPartialInPaperLive;
   cfg.real_partial_requires_broker_manager = InpRealPartialRequiresBrokerManager;
   cfg.enable_real_hard_close_finalizer = InpEnableRealHardCloseFinalizer;
   cfg.write_real_hard_close_finalizer_audit = InpWriteRealHardCloseFinalizerAudit;
   cfg.real_hard_close_finalizer_scan_seconds = InpRealHardCloseFinalizerScanSeconds;
   cfg.real_hard_close_finalizer_retry_seconds = InpRealHardCloseFinalizerRetrySeconds;
   cfg.real_hard_close_finalizer_deviation_points = InpRealHardCloseFinalizerDeviationPoints;
   cfg.real_hard_close_finalizer_max_attempts_per_position = InpRealHardCloseFinalizerMaxAttemptsPerPosition;
   cfg.allow_real_hard_close_finalizer_in_paper_live = InpAllowRealHardCloseFinalizerInPaperLive;
   cfg.real_hard_close_finalizer_requires_broker_manager = InpRealHardCloseFinalizerRequiresBrokerManager;
   cfg.real_hard_close_alert_unclosed_positions = InpRealHardCloseAlertUnclosedPositions;
   cfg.enable_validation_pack = InpEnableValidationPack;
   cfg.write_validation_reports = InpWriteValidationReports;
   cfg.validation_run_on_init = InpValidationRunOnInit;
   cfg.validation_run_on_pulse = InpValidationRunOnPulse;
   cfg.validation_run_seconds = InpValidationRunSeconds;
   cfg.validation_strict_mode = InpValidationStrictMode;
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
   cfg.write_w_level_audit = InpWriteWLevelAudit;
   cfg.max_w_level_backfill_on_init = InpMaxWLevelBackfillOnInit;
   cfg.max_w_level_catchup_per_pulse = InpMaxWLevelCatchupPerPulse;
   cfg.write_hunt_audit = InpWriteHuntAudit;
   cfg.max_hunt_backfill_on_init = InpMaxHuntBackfillOnInit;
   cfg.max_hunt_catchup_per_pulse = InpMaxHuntCatchupPerPulse;
   cfg.write_smt_candidate_audit = InpWriteSMTCandidateAudit;
   cfg.max_smt_backfill_on_init = InpMaxSMTBackfillOnInit;
   cfg.max_smt_catchup_per_pulse = InpMaxSMTCatchupPerPulse;
   cfg.write_signal_registry_audit = InpWriteSignalRegistryAudit;
   cfg.max_signal_backfill_on_init = InpMaxSignalBackfillOnInit;
   cfg.max_signal_catchup_per_pulse = InpMaxSignalCatchupPerPulse;
   cfg.write_paper_entry_audit = InpWritePaperEntryAudit;
   cfg.max_paper_entry_backfill_on_init = InpMaxPaperEntryBackfillOnInit;
   cfg.max_paper_entry_catchup_per_pulse = InpMaxPaperEntryCatchupPerPulse;
   cfg.write_paper_outcome_audit = InpWritePaperOutcomeAudit;
   cfg.max_paper_outcome_backfill_on_init = InpMaxPaperOutcomeBackfillOnInit;
   cfg.max_paper_outcome_catchup_per_pulse = InpMaxPaperOutcomeCatchupPerPulse;
   cfg.max_paper_outcome_forward_checks = InpMaxPaperOutcomeForwardChecks;
   cfg.write_partial_audit = InpWritePartialAudit;
   cfg.max_partial_backfill_on_init = InpMaxPartialBackfillOnInit;
   cfg.max_partial_catchup_per_pulse = InpMaxPartialCatchupPerPulse;
   cfg.write_hard_close_audit = InpWriteHardCloseAudit;
   cfg.max_hard_close_backfill_on_init = InpMaxHardCloseBackfillOnInit;
   cfg.max_hard_close_catchup_per_pulse = InpMaxHardCloseCatchupPerPulse;
   cfg.restore_persistence_on_init = InpRestorePersistenceOnInit;
   cfg.write_persistence_snapshot = InpWritePersistenceSnapshot;
   cfg.persistence_snapshot_seconds = InpPersistenceSnapshotSeconds;
}

int OnInit()
{
   if(!STC_EnsureOfflineLicense(true))
      return INIT_FAILED;

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
   if(!STC_EnsureOfflineLicense(false))
      return;
   g_stc_engine.Pulse(TimeCurrent());
}

void OnTick()
{
   // Level 22 remains timer-driven. Validation is audit-only; real auto-entry, real partial close, and real hard close finalizer are gated by explicit safety inputs and AUTO_TRADE mode.
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   g_stc_engine.Deinit(reason);
}
