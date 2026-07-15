#property strict
#property version   "1.00"
#property description "No-order contract diagnostic for NDS Hook 86.4 Cycle R1"

#include <FlagCountingPhoenix/FP_NDSHookTradeRules.mqh>

bool AssertCondition(const bool condition,const string code)
{
   if(condition)
      return true;
   Print("NDS_HOOK_864_SELFTEST_FAIL code=",code);
   return false;
}

int OnInit()
{
   FP_NDSHookTradeConfig cfg;
   FP_ResetNDSHookTradeConfig(cfg);
   cfg.profile=FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1;

   FP_HookPhase02Sequence seq;
   FP_ResetHookPhase02Sequence(seq);
   seq.sequence_id=55;
   seq.direction=FP_HOOK_P02_DIRECTION_POSITIVE;
   seq.state=FP_HOOK_P02_STATE_MATURE;
   seq.origin_node_id=1;
   seq.origin_time=(datetime)1000;
   seq.origin_price=100.0;
   seq.x_count=3;
   seq.cycle_crown_node_id=2;
   seq.cycle_crown_time=(datetime)1100;
   seq.cycle_crown_price=200.0;
   seq.cycle_crown_valid=true;
   seq.resolve_node_id=3;
   seq.resolve_time=(datetime)1200;
   seq.resolve_price=130.0;
   seq.resolve_confirmed=true;
   seq.retracement_ratio=0.70;
   seq.death_boundary_price=100.0;
   seq.valid_after_hook=true;
   seq.valid_hook_family=true;
   seq.valid=true;
   seq.hook_failed=false;

   string reason;
   if(!AssertCondition(FP_NDSHook864CycleR1SequenceEligible(seq,cfg,reason),
                       "golden_x3_should_be_eligible:"+reason))
      return INIT_FAILED;

   double entry=FP_NDSHook864CycleR1RawEntry(seq,cfg.hook_entry_ratio);
   if(!AssertCondition(MathAbs(entry-113.6)<1e-9,"positive_projection_should_equal_113_6"))
      return INIT_FAILED;

   seq.x_count=2;
   if(!AssertCondition(!FP_NDSHook864CycleR1SequenceEligible(seq,cfg,reason),
                       "x2_should_be_rejected"))
      return INIT_FAILED;

   seq.x_count=3;
   seq.retracement_ratio=FP_NDS_HOOK_864_ENTRY_RATIO;
   if(!AssertCondition(!FP_NDSHook864CycleR1SequenceEligible(seq,cfg,reason),
                       "already_touched_level_should_be_rejected"))
      return INIT_FAILED;

   seq.direction=FP_HOOK_P02_DIRECTION_NEGATIVE;
   seq.state=FP_HOOK_P02_STATE_CAPPED;
   seq.origin_price=200.0;
   seq.cycle_crown_price=100.0;
   seq.resolve_price=170.0;
   seq.retracement_ratio=0.70;
   seq.death_boundary_price=200.0;
   seq.x_count=4;
   if(!AssertCondition(FP_NDSHook864CycleR1SequenceEligible(seq,cfg,reason),
                       "golden_negative_x4_should_be_eligible:"+reason))
      return INIT_FAILED;
   entry=FP_NDSHook864CycleR1RawEntry(seq,cfg.hook_entry_ratio);
   if(!AssertCondition(MathAbs(entry-186.4)<1e-9,"negative_projection_should_equal_186_4"))
      return INIT_FAILED;

   cfg.hook_entry_ratio=0.860;
   if(!AssertCondition(!FP_NDSHook864CycleR1SequenceEligible(seq,cfg,reason),
                       "noncanonical_ratio_should_be_rejected"))
      return INIT_FAILED;
   cfg.hook_entry_ratio=FP_NDS_HOOK_864_ENTRY_RATIO;

   FP_NDSHookTradeProfile recovered_profile;
   if(!AssertCondition(FP_NDSHookTradeProfileFromBrokerComment(cfg,"NDSH|S55|HH",
                                                               recovered_profile,reason) &&
                       recovered_profile==FP_NDS_HOOK_TRADE_PROFILE_TERMINAL_F123,
                       "legacy_phase52_comment_should_recover_terminal_profile"))
      return INIT_FAILED;

   if(!AssertCondition(FP_NDSHookTradeProfileFromBrokerComment(cfg,"NDSH|864R1|S55|HH",
                                                               recovered_profile,reason) &&
                       recovered_profile==FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1,
                       "phase55_comment_should_recover_fixed_r_profile"))
      return INIT_FAILED;

   if(!AssertCondition(!FP_NDSHookTradeProfileFromBrokerComment(cfg,"NDSH|UNKNOWN|S55|HH",
                                                                recovered_profile,reason),
                       "unknown_profile_comment_should_fail_closed"))
      return INIT_FAILED;

   Print("NDS_HOOK_864_SELFTEST_PASS authority_order=false ratio=",
         DoubleToString(FP_NDS_HOOK_864_ENTRY_RATIO,3),
         " nodes=3_or_4 reward_r=",
         DoubleToString(FP_NDS_HOOK_864_REWARD_R,1));
   return INIT_SUCCEEDED;
}

void OnTick()
{
   // Diagnostic only. No order, position, file, network, or chart authority.
}
