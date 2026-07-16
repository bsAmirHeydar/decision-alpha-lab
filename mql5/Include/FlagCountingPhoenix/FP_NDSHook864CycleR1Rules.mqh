#ifndef __FP_NDS_HOOK_864_CYCLE_R1_RULES_MQH__
#define __FP_NDS_HOOK_864_CYCLE_R1_RULES_MQH__
#property strict

#include "FP_NDSHook864CycleR1Evidence.mqh"
#include "FP_HookPhase02Rules.mqh"

// ============================================================================
// NDS Hook 86.4% / 3-or-4-node / Phase04-closed / fixed-1R profile
// ----------------------------------------------------------------------------
// This adapter consumes canonical Hook Phase02 identity plus canonical Phase04
// X-closure evidence. It never detects nodes, rebuilds a Hook, or owns broker
// execution. First-arrival evidence is derived only from closed rates captured
// by the dedicated evidence bridge.
// ============================================================================

string FP_NDSHookTradeProfileName(const FP_NDSHookTradeProfile profile)
{
   if(profile == FP_NDS_HOOK_TRADE_PROFILE_TERMINAL_F123)
      return "TERMINAL_F123";
   if(profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1)
      return "HOOK_864_CYCLE_R1";
   return "UNKNOWN_PROFILE";
}

string FP_NDSHookTradeProfileCode(const FP_NDSHookTradeProfile profile)
{
   if(profile == FP_NDS_HOOK_TRADE_PROFILE_TERMINAL_F123)
      return "TF3";
   if(profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1)
      return "864R1";
   return "UNK";
}

string FP_NDSHookTradeSchemaName(const FP_NDSHookTradeProfile profile)
{
   if(profile == FP_NDS_HOOK_TRADE_PROFILE_TERMINAL_F123)
      return FP_NDS_HOOK_TERMINAL_F123_SCHEMA_VERSION;
   if(profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1)
      return FP_NDS_HOOK_864_CYCLE_R1_SCHEMA_VERSION;
   return FP_NDS_HOOK_TRADE_SCHEMA_VERSION;
}

bool FP_NDSHook864CycleR1ConfigValid(const FP_NDSHookTradeConfig &cfg,
                                     string &reason)
{
   reason = "ok";
   const double epsilon = 1e-10;
   if(MathAbs(cfg.hook_entry_ratio - FP_NDS_HOOK_864_ENTRY_RATIO) > epsilon)
   {
      reason = "approved_hook_entry_ratio_must_be_exactly_0_864";
      return false;
   }
   if(cfg.hook_entry_min_x_count != FP_NDS_HOOK_864_MIN_X_COUNT ||
      cfg.hook_entry_max_x_count != FP_NDS_HOOK_864_MAX_X_COUNT)
   {
      reason = "approved_node_count_window_must_be_exactly_3_to_4";
      return false;
   }
   if(!cfg.hook_entry_require_confirmed_terminal)
   {
      reason = "confirmed_terminal_gate_must_remain_enabled";
      return false;
   }
   if(!cfg.hook_entry_require_phase04_x_closed)
   {
      reason = "phase04_x_closed_gate_must_remain_enabled";
      return false;
   }
   if(MathAbs(cfg.hook_entry_closure_ratio - FP_NDS_HOOK_864_CLOSURE_RATIO) > epsilon)
   {
      reason = "approved_cycle_closure_ratio_must_be_exactly_0_50";
      return false;
   }
   if(!cfg.hook_entry_require_level_untouched)
   {
      reason = "untouched_86_4_gate_must_remain_enabled";
      return false;
   }
   if(MathAbs(cfg.fixed_reward_r - FP_NDS_HOOK_864_REWARD_R) > epsilon)
   {
      reason = "approved_fixed_reward_must_be_exactly_1R";
      return false;
   }
   return true;
}

double FP_NDSHook864CycleR1RawEntry(const FP_HookPhase02Sequence &seq,
                                    const double ratio)
{
   return FP_NDSHook864CycleR1RawEntryFromSequence(seq, ratio);
}

bool FP_NDSHook864CycleR1EntryInsideCycle(const FP_HookPhase02Sequence &seq,
                                         const double entry)
{
   if(seq.direction == FP_HOOK_P02_DIRECTION_POSITIVE)
      return (seq.origin_price < entry && entry < seq.cycle_crown_price);
   if(seq.direction == FP_HOOK_P02_DIRECTION_NEGATIVE)
      return (seq.cycle_crown_price < entry && entry < seq.origin_price);
   return false;
}

// Kept only for source compatibility with Phase55 v1 callers. The canonical
// first-arrival gate is no longer derived from seq.retracement_ratio because
// that field describes the Phase02 terminal geometry, not post-closure price
// travel. Execution uses FP_NDSHook864CycleR1RuntimeEligible instead.
bool FP_NDSHook864CycleR1LevelUntouched(const FP_HookPhase02Sequence &seq,
                                       const double ratio)
{
   const double epsilon = 1e-10;
   return (seq.retracement_ratio + epsilon < ratio);
}

bool FP_NDSHook864CycleR1SequenceEligible(const FP_HookPhase02Sequence &seq,
                                         const FP_NDSHookTradeConfig &cfg,
                                         string &reason)
{
   reason = "not_evaluated";

   string config_reason;
   if(!FP_NDSHook864CycleR1ConfigValid(cfg, config_reason))
   {
      reason = "profile_config_" + config_reason;
      return false;
   }

   if(!seq.valid || seq.hook_failed || !seq.valid_hook_family)
   {
      reason = "canonical_hook_invalid_or_failed";
      return false;
   }
   bool family_allowed = ((seq.valid_after_hook && cfg.allow_hook_after_hook) ||
                          (seq.valid_after_opposing_f3 && cfg.allow_hook_after_f3));
   if(!family_allowed)
   {
      reason = "canonical_hook_family_not_allowed";
      return false;
   }
   if(seq.origin_price <= 0.0 || seq.resolve_price <= 0.0)
   {
      reason = "canonical_price_missing";
      return false;
   }
   if(!FP_HookP02SequenceCycleClosed(seq))
   {
      reason = "canonical_phase02_terminal_not_available";
      return false;
   }
   if(!seq.resolve_confirmed)
   {
      reason = "canonical_terminal_not_confirmed";
      return false;
   }
   if(!seq.cycle_crown_valid || seq.cycle_crown_price <= 0.0)
   {
      reason = "canonical_cycle_crown_missing";
      return false;
   }
   if(seq.x_count < cfg.hook_entry_min_x_count ||
      seq.x_count > cfg.hook_entry_max_x_count)
   {
      reason = "canonical_x_count_not_3_or_4";
      return false;
   }
   if(seq.state != FP_HOOK_P02_STATE_MATURE &&
      seq.state != FP_HOOK_P02_STATE_CAPPED)
   {
      reason = "canonical_sequence_not_mature_or_capped";
      return false;
   }

   double raw_entry = FP_NDSHook864CycleR1RawEntry(seq, cfg.hook_entry_ratio);
   if(raw_entry <= 0.0 || !FP_NDSHook864CycleR1EntryInsideCycle(seq, raw_entry))
   {
      reason = "hook_864_projection_outside_canonical_cycle";
      return false;
   }

   reason = "canonical_phase02_x3_or_x4_intrinsic_valid";
   return true;
}

bool FP_NDSHook864CycleR1RuntimeEligible(const string symbol,
                                         const ENUM_TIMEFRAMES period,
                                         const FP_HookPhase02Sequence &seq,
                                         const FP_NDSHookTradeConfig &cfg,
                                         FP_NDSHook864CycleR1Evidence &evidence,
                                         string &reason)
{
   FP_ResetNDSHook864CycleR1Evidence(evidence);
   if(!FP_NDSHook864CycleR1SequenceEligible(seq, cfg, reason))
      return false;

   if(!FP_NDSFindHook864CycleR1Evidence(symbol, period, seq, evidence))
   {
      reason = evidence.status;
      return false;
   }
   if(!evidence.phase04_record_valid)
   {
      reason = "phase04_record_invalid";
      return false;
   }
   if(evidence.origin_return_penetrated)
   {
      reason = "cycle_dead_by_origin_return_before_entry";
      return false;
   }
   if(!evidence.x_closure_candidate || !evidence.x_closed)
   {
      reason = "phase04_x_cycle_not_closed";
      return false;
   }
   if(evidence.x_count < cfg.hook_entry_min_x_count ||
      evidence.x_count > cfg.hook_entry_max_x_count)
   {
      reason = "phase04_x_count_not_3_or_4";
      return false;
   }
   if(evidence.level_touched_after_closure)
   {
      reason = "hook_864_first_arrival_already_consumed_after_closure";
      return false;
   }
   if(!evidence.valid)
   {
      reason = evidence.status;
      return false;
   }

   reason = "phase04_x_closed_x3_or_x4_before_first_864_touch";
   return true;
}

string FP_NDSHook864CycleR1FunnelSummary(const FP_NDSHookTradeCandidateFunnel &f)
{
   string s = "total=" + IntegerToString(f.sequences_total);
   s += ";canonical=" + IntegerToString(f.canonical_valid);
   s += ";family=" + IntegerToString(f.valid_family);
   s += ";allowed=" + IntegerToString(f.family_allowed);
   s += ";confirmed=" + IntegerToString(f.confirmed_terminal);
   s += ";crown=" + IntegerToString(f.crown_valid);
   s += ";x34=" + IntegerToString(f.x3_x4);
   s += ";mature=" + IntegerToString(f.mature_or_capped);
   s += ";p04=" + IntegerToString(f.phase04_evidence_found);
   s += ";closed=" + IntegerToString(f.phase04_x_closed);
   s += ";alive=" + IntegerToString(f.alive_after_closure);
   s += ";untouched=" + IntegerToString(f.first_864_untouched);
   s += ";ready=" + IntegerToString(f.execution_ready);
   s += ";blocker=" + f.dominant_blocker;
   return s;
}

void FP_NDSHook864CycleR1AnalyzeCandidates(const string symbol,
                                           const ENUM_TIMEFRAMES period,
                                           const FP_HookPhase02Sequence &sequences[],
                                           const FP_NDSHookTradeConfig &cfg,
                                           FP_NDSHookTradeCandidateFunnel &f)
{
   FP_ResetNDSHookTradeCandidateFunnel(f);
   f.sequences_total = ArraySize(sequences);

   for(int i=0; i<ArraySize(sequences); i++)
   {
      FP_HookPhase02Sequence seq = sequences[i];
      if(!seq.valid || seq.hook_failed)
         continue;
      f.canonical_valid++;
      if(!seq.valid_hook_family)
         continue;
      f.valid_family++;
      if(!((seq.valid_after_hook && cfg.allow_hook_after_hook) ||
           (seq.valid_after_opposing_f3 && cfg.allow_hook_after_f3)))
         continue;
      f.family_allowed++;
      if(!seq.resolve_confirmed)
         continue;
      f.confirmed_terminal++;
      if(!seq.cycle_crown_valid || seq.cycle_crown_price <= 0.0)
         continue;
      f.crown_valid++;
      if(seq.x_count < cfg.hook_entry_min_x_count ||
         seq.x_count > cfg.hook_entry_max_x_count)
         continue;
      f.x3_x4++;
      if(seq.state != FP_HOOK_P02_STATE_MATURE &&
         seq.state != FP_HOOK_P02_STATE_CAPPED)
         continue;
      f.mature_or_capped++;

      FP_NDSHook864CycleR1Evidence evidence;
      if(!FP_NDSFindHook864CycleR1Evidence(symbol, period, seq, evidence))
         continue;
      f.phase04_evidence_found++;
      if(!evidence.x_closed)
         continue;
      f.phase04_x_closed++;
      if(evidence.origin_return_penetrated)
         continue;
      f.alive_after_closure++;
      if(evidence.level_touched_after_closure)
         continue;
      f.first_864_untouched++;

      string reason;
      if(FP_NDSHook864CycleR1RuntimeEligible(symbol, period, seq, cfg,
                                             evidence, reason))
         f.execution_ready++;
   }

   if(f.sequences_total <= 0) f.dominant_blocker = "no_phase02_sequences";
   else if(f.canonical_valid <= 0) f.dominant_blocker = "all_sequences_invalid_or_failed";
   else if(f.valid_family <= 0) f.dominant_blocker = "no_valid_hook_family";
   else if(f.family_allowed <= 0) f.dominant_blocker = "hook_family_disabled_by_config";
   else if(f.confirmed_terminal <= 0) f.dominant_blocker = "no_confirmed_terminal";
   else if(f.crown_valid <= 0) f.dominant_blocker = "no_cycle_crown";
   else if(f.x3_x4 <= 0) f.dominant_blocker = "no_x3_or_x4_sequence";
   else if(f.mature_or_capped <= 0) f.dominant_blocker = "no_mature_or_capped_sequence";
   else if(f.phase04_evidence_found <= 0) f.dominant_blocker = "phase04_evidence_missing";
   else if(f.phase04_x_closed <= 0) f.dominant_blocker = "phase04_x_not_closed";
   else if(f.alive_after_closure <= 0) f.dominant_blocker = "all_closed_cycles_dead_by_origin_return";
   else if(f.first_864_untouched <= 0) f.dominant_blocker = "first_864_arrival_already_consumed";
   else if(f.execution_ready <= 0) f.dominant_blocker = "runtime_contract_rejected";
   else f.dominant_blocker = "ready_candidate_exists";
}

#endif // __FP_NDS_HOOK_864_CYCLE_R1_RULES_MQH__
