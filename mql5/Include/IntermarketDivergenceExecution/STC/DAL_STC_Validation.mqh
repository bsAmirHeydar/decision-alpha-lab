#ifndef __DAL_STC_VALIDATION_MQH__
#define __DAL_STC_VALIDATION_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_RealHardClose.mqh>

struct STC_ValidationCounters
{
   int checks;
   int passed;
   int failed;
   int warnings;
};

void STC_ResetValidationCounters(STC_ValidationCounters &c)
{
   c.checks = 0;
   c.passed = 0;
   c.failed = 0;
   c.warnings = 0;
}

string STC_ValidationStatusText(const bool passed, const bool warning)
{
   if(warning) return passed ? "WARN_PASS" : "WARN_FAIL";
   return passed ? "PASS" : "FAIL";
}

bool STC_AppendValidationMatrixRow(STC_Config &cfg,
                                   STC_RuntimeState &state,
                                   const string run_reason,
                                   const string suite,
                                   const string test_id,
                                   const string expected,
                                   const string actual,
                                   const bool passed,
                                   const bool warning,
                                   const string rule_note,
                                   STC_ValidationCounters &counters)
{
   counters.checks++;
   if(passed) counters.passed++;
   else counters.failed++;
   if(warning) counters.warnings++;

   if(!cfg.write_validation_reports)
      return true;

   bool exists = FileIsExist(state.validation_matrix_file_common, FILE_COMMON);
   int h = FileOpen(state.validation_matrix_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append validation matrix CSV ", state.validation_matrix_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h, "server_write_time", "strategy_id", "run_id", "runtime_mode", "symbol1", "symbol2", "magic", "stc_day_id", "run_reason", "suite", "test_id", "expected", "actual", "status", "warning", "rule_note");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(TimeCurrent()),
      cfg.strategy_id,
      cfg.run_id,
      STC_RuntimeModeText(cfg.runtime_mode),
      cfg.symbol1,
      cfg.symbol2,
      IntegerToString(cfg.magic_number),
      state.last_check_audit_stc_day_id,
      run_reason,
      suite,
      test_id,
      expected,
      actual,
      STC_ValidationStatusText(passed, warning),
      STC_BoolText(warning),
      rule_note);
   FileClose(h);
   return true;
}

void STC_ValidationCheckBool(STC_Config &cfg,
                             STC_RuntimeState &state,
                             const string run_reason,
                             const string suite,
                             const string test_id,
                             const bool condition,
                             const string expected,
                             const string actual,
                             const bool warning,
                             const string rule_note,
                             STC_ValidationCounters &counters)
{
   STC_AppendValidationMatrixRow(cfg, state, run_reason, suite, test_id, expected, actual, condition, warning, rule_note, counters);
}

void STC_RunValidation_Config(STC_Config &cfg, STC_RuntimeState &state, const string run_reason, STC_ValidationCounters &counters)
{
   STC_ValidationCheckBool(cfg, state, run_reason, "CONFIG", "strategy_id_locked", cfg.strategy_id == "EXEC001_STC_SMT_Cycles", "EXEC001_STC_SMT_Cycles", cfg.strategy_id, false, "strategy id must remain stable for persistence and magic-only management", counters);
   STC_ValidationCheckBool(cfg, state, run_reason, "CONFIG", "symbols_are_distinct", cfg.symbol1 != "" && cfg.symbol2 != "" && cfg.symbol1 != cfg.symbol2, "non-empty distinct Symbol1/Symbol2", cfg.symbol1 + "/" + cfg.symbol2, false, "STC SMT is a two-symbol structural divergence strategy", counters);
   STC_ValidationCheckBool(cfg, state, run_reason, "CONFIG", "check_tf_allowed", STC_IsAllowedCheckMinutes(cfg.check_minutes), "1/3/5/10/15/30", IntegerToString(cfg.check_minutes), false, "check candle must be one of the locked SRS choices", counters);
   STC_ValidationCheckBool(cfg, state, run_reason, "CONFIG", "reward_positive", cfg.final_reward_r > 0.0, ">0", DoubleToString(cfg.final_reward_r, 4), false, "Final Reward is an R multiple and must be positive", counters);
   STC_ValidationCheckBool(cfg, state, run_reason, "CONFIG", "risk_positive", cfg.risk_percent > 0.0, ">0", DoubleToString(cfg.risk_percent, 4), false, "Risk Percent must be positive", counters);
   STC_ValidationCheckBool(cfg, state, run_reason, "CONFIG", "magic_positive", cfg.magic_number > 0, ">0", IntegerToString(cfg.magic_number), false, "real management is magic-only", counters);
   STC_ValidationCheckBool(cfg, state, run_reason, "CONFIG", "real_transports_default_gated", (!cfg.enable_real_auto_entry || cfg.runtime_mode == STC_MODE_AUTO_TRADE || cfg.allow_auto_entry_in_paper_live), "real auto-entry gated", STC_BoolText(cfg.enable_real_auto_entry) + "/" + STC_RuntimeModeText(cfg.runtime_mode), true, "warning only: real transport should be explicit and audited", counters);
}

void STC_RunValidation_TimeMatrix(STC_Config &cfg, STC_RuntimeState &state, const string run_reason, STC_ValidationCounters &counters)
{
   int minutes[9] = {0, 355, 360, 420, 775, 780, 810, 1165, 1170};
   string expected_m[9] = {"M1", "M1", "NONE", "M2", "M2", "NONE", "M3", "M3", "NONE"};
   string expected_w[9] = {"W1", "W4", "NONE", "W1", "W4", "NONE", "W1", "W4", "NONE"};
   string expected_phase[9] = {"ACTIVE_M", "ACTIVE_M", "M_GAP_NO_ENTRY_NO_DETECTION", "ACTIVE_M", "ACTIVE_M", "M_GAP_NO_ENTRY_NO_DETECTION", "ACTIVE_M", "ACTIVE_M", "HARD_CLOSE_ZONE"};
   bool expected_final[9] = {false, true, false, false, true, false, false, true, false};

   for(int i=0; i<9; i++)
   {
      STC_TimeSnapshot snap;
      STC_ResetTimeSnapshot(snap);
      snap.stc_day_start_ny = STC_MakeDateTime(2026, 1, 1, 20, 0, 0);
      snap.elapsed_minutes_from_2000 = minutes[i];
      snap.elapsed_seconds_from_2000 = minutes[i] * 60;
      STC_AssignMCycle(snap);
      STC_AssignPhase(snap);
      STC_AssignCheckCandle(snap, cfg.check_minutes);

      string actual_m = STC_MCycleText(snap.m_cycle);
      string actual_w = STC_WCycleText(snap.w_cycle);
      string actual_phase = STC_TimePhaseText(snap.phase);
      string id = "elapsed_" + IntegerToString(minutes[i]);
      STC_ValidationCheckBool(cfg, state, run_reason, "TIME_MATRIX", id + "_m", actual_m == expected_m[i], expected_m[i], actual_m, false, "M cycle boundaries must match locked NY schedule", counters);
      STC_ValidationCheckBool(cfg, state, run_reason, "TIME_MATRIX", id + "_w", actual_w == expected_w[i], expected_w[i], actual_w, false, "W cycle boundaries must be 90-minute children inside each M", counters);
      STC_ValidationCheckBool(cfg, state, run_reason, "TIME_MATRIX", id + "_phase", actual_phase == expected_phase[i], expected_phase[i], actual_phase, false, "gaps must be no-entry/no-detection and 15:30+ must be hard-close zone", counters);
      if(minutes[i] == 355 || minutes[i] == 775 || minutes[i] == 1165)
         STC_ValidationCheckBool(cfg, state, run_reason, "TIME_MATRIX", id + "_final_check", snap.final_check_of_m == expected_final[i] && !snap.check_entry_allowed_at_close, "final_check=true and entry_allowed=false", STC_BoolText(snap.final_check_of_m) + "/" + STC_BoolText(snap.check_entry_allowed_at_close), false, "last check candle of each M is audited but no entry is allowed", counters);
   }
}

void STC_RunValidation_ReferenceMatrix(STC_Config &cfg, STC_RuntimeState &state, const string run_reason, STC_ValidationCounters &counters)
{
   STC_ValidationCheckBool(cfg, state, run_reason, "REFERENCE_MATRIX", "w1_count", STC_HuntReferenceCount(STC_W1) == 0, "0", IntegerToString(STC_HuntReferenceCount(STC_W1)), false, "W1 never produces a signal", counters);
   STC_ValidationCheckBool(cfg, state, run_reason, "REFERENCE_MATRIX", "w2_refs", STC_HuntReferenceCount(STC_W2) == 1 && STC_HuntReferenceByRank(STC_W2,0) == STC_W1, "W1", STC_WCycleText(STC_HuntReferenceByRank(STC_W2,0)), false, "W2 compares only with W1", counters);
   STC_ValidationCheckBool(cfg, state, run_reason, "REFERENCE_MATRIX", "w3_refs", STC_HuntReferenceCount(STC_W3) == 2 && STC_HuntReferenceByRank(STC_W3,0) == STC_W2 && STC_HuntReferenceByRank(STC_W3,1) == STC_W1, "W2,W1", STC_WCycleText(STC_HuntReferenceByRank(STC_W3,0)) + "," + STC_WCycleText(STC_HuntReferenceByRank(STC_W3,1)), false, "W3 compares only with W2 and W1", counters);
   STC_ValidationCheckBool(cfg, state, run_reason, "REFERENCE_MATRIX", "w4_refs", STC_HuntReferenceCount(STC_W4) == 3 && STC_HuntReferenceByRank(STC_W4,0) == STC_W3 && STC_HuntReferenceByRank(STC_W4,1) == STC_W2 && STC_HuntReferenceByRank(STC_W4,2) == STC_W1, "W3,W2,W1", STC_WCycleText(STC_HuntReferenceByRank(STC_W4,0)) + "," + STC_WCycleText(STC_HuntReferenceByRank(STC_W4,1)) + "," + STC_WCycleText(STC_HuntReferenceByRank(STC_W4,2)), false, "W4 compares only with W3, W2, and W1", counters);
}

void STC_RunValidation_HuntPatterns(STC_Config &cfg, STC_RuntimeState &state, const string run_reason, STC_ValidationCounters &counters)
{
   STC_ValidationCheckBool(cfg, state, run_reason, "HUNT_PATTERN", "none", STC_DeriveHuntPattern(false,false) == STC_HUNT_NONE, "NONE", STC_HuntPatternText(STC_DeriveHuntPattern(false,false)), false, "no symbol touched reference", counters);
   STC_ValidationCheckBool(cfg, state, run_reason, "HUNT_PATTERN", "symbol1_only", STC_DeriveHuntPattern(true,false) == STC_HUNT_SYMBOL1_ONLY, "SYMBOL1_ONLY", STC_HuntPatternText(STC_DeriveHuntPattern(true,false)), false, "exactly one symbol hunted means raw SMT material", counters);
   STC_ValidationCheckBool(cfg, state, run_reason, "HUNT_PATTERN", "symbol2_only", STC_DeriveHuntPattern(false,true) == STC_HUNT_SYMBOL2_ONLY, "SYMBOL2_ONLY", STC_HuntPatternText(STC_DeriveHuntPattern(false,true)), false, "exactly one symbol hunted means raw SMT material", counters);
   STC_ValidationCheckBool(cfg, state, run_reason, "HUNT_PATTERN", "both", STC_DeriveHuntPattern(true,true) == STC_HUNT_BOTH, "BOTH", STC_HuntPatternText(STC_DeriveHuntPattern(true,true)), false, "both symbols hunted means no SMT divergence", counters);
}

void STC_WriteValidationSummary(STC_Config &cfg, STC_RuntimeState &state, const string run_reason, STC_ValidationCounters &counters)
{
   if(!cfg.write_validation_reports)
      return;
   bool exists = FileIsExist(state.validation_summary_file_common, FILE_COMMON);
   int h = FileOpen(state.validation_summary_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append validation summary CSV ", state.validation_summary_file_common, " err=", GetLastError());
      return;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h, "server_write_time", "strategy_id", "run_id", "runtime_mode", "symbol1", "symbol2", "magic", "stc_day_id", "run_reason", "validation_status", "checks", "passed", "failed", "warnings", "strict_mode", "matrix_file", "rule_note");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(TimeCurrent()),
      cfg.strategy_id,
      cfg.run_id,
      STC_RuntimeModeText(cfg.runtime_mode),
      cfg.symbol1,
      cfg.symbol2,
      IntegerToString(cfg.magic_number),
      state.last_check_audit_stc_day_id,
      run_reason,
      state.validation_status,
      counters.checks,
      counters.passed,
      counters.failed,
      counters.warnings,
      STC_BoolText(cfg.validation_strict_mode),
      state.validation_matrix_file_common,
      "Level19 validation is audit-only and does not change strategy decisions or broker transports");
   FileClose(h);
}

void STC_ProcessValidationPack(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, const string run_reason, const bool force)
{
   if(!cfg.enable_validation_pack)
      return;
   if(!force)
   {
      if(!cfg.validation_run_on_pulse)
         return;
      if(state.last_validation_server_time > 0 && TimeCurrent() - state.last_validation_server_time < cfg.validation_run_seconds)
         return;
   }

   STC_ValidationCounters counters;
   STC_ResetValidationCounters(counters);
   state.last_validation_server_time = TimeCurrent();
   state.validation_runs++;
   state.validation_last_reason = run_reason;

   STC_RunValidation_Config(cfg, state, run_reason, counters);
   STC_RunValidation_TimeMatrix(cfg, state, run_reason, counters);
   STC_RunValidation_ReferenceMatrix(cfg, state, run_reason, counters);
   STC_RunValidation_HuntPatterns(cfg, state, run_reason, counters);

   state.validation_checks += counters.checks;
   state.validation_failures += counters.failed;
   if(counters.failed == 0)
      state.validation_status = (counters.warnings > 0 ? "PASS_WITH_WARNINGS" : "PASS");
   else
      state.validation_status = (cfg.validation_strict_mode ? "FAIL_STRICT" : "FAIL_AUDIT_ONLY");

   STC_WriteValidationSummary(cfg, state, run_reason, counters);
   STC_AppendRuntimeEventCsv(cfg, state, "VALIDATION_PACK", "reason=" + run_reason + "; status=" + state.validation_status + "; checks=" + IntegerToString(counters.checks) + "; failed=" + IntegerToString(counters.failed) + "; warnings=" + IntegerToString(counters.warnings) + "; matrix=" + state.validation_matrix_file_common);
}

#endif
