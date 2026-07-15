#ifndef __FP_NDS_HOOK_864_CYCLE_R1_RULES_MQH__
#define __FP_NDS_HOOK_864_CYCLE_R1_RULES_MQH__
#property strict

#include "FP_NDSHookTradeTypes.mqh"
#include "FP_HookPhase02Rules.mqh"

// ============================================================================
// NDS Hook 86.4% / 3-or-4-node / fixed-1R profile
// ----------------------------------------------------------------------------
// This module is an adapter over the canonical Hook Phase02 object. It does not
// detect nodes, rebuild a Hook, infer validity, or own broker execution.
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
      // The approved setup is exact. This is deliberately not a generic range
      // optimizer because node-count doctrine belongs to Hook Phase02.
      reason = "approved_node_count_window_must_be_exactly_3_to_4";
      return false;
   }
   if(!cfg.hook_entry_require_confirmed_terminal)
   {
      reason = "confirmed_terminal_gate_must_remain_enabled";
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
   // Direction-independent interpolation from crown toward origin:
   // positive: crown high -> origin low
   // negative: crown low -> origin high
   return seq.cycle_crown_price + ratio * (seq.origin_price - seq.cycle_crown_price);
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

bool FP_NDSHook864CycleR1LevelUntouched(const FP_HookPhase02Sequence &seq,
                                       const double ratio)
{
   // Phase02 retracement is measured from crown toward origin. If the current
   // canonical/raw terminal has already reached or passed the requested level,
   // a newly-created limit would be late and is rejected.
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

   // Consume canonical Phase02 state only. No independent node counting.
   // These checks are repeated here intentionally so direct adapter callers
   // cannot bypass the selector's canonical validity and family boundaries.
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
      reason = "canonical_cycle_not_closed";
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
   if(seq.retracement_ratio < 0.0)
   {
      reason = "canonical_retracement_ratio_negative";
      return false;
   }

   double raw_entry = FP_NDSHook864CycleR1RawEntry(seq, cfg.hook_entry_ratio);
   if(raw_entry <= 0.0 || !FP_NDSHook864CycleR1EntryInsideCycle(seq, raw_entry))
   {
      reason = "hook_864_projection_outside_canonical_cycle";
      return false;
   }
   if(!FP_NDSHook864CycleR1LevelUntouched(seq, cfg.hook_entry_ratio))
   {
      reason = "hook_864_level_already_reached_or_crossed";
      return false;
   }

   reason = "canonical_closed_cycle_x3_or_x4_before_864";
   return true;
}

#endif // __FP_NDS_HOOK_864_CYCLE_R1_RULES_MQH__
