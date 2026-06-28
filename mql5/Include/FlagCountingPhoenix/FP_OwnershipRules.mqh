#ifndef __FP_OWNERSHIP_RULES_MQH__
#define __FP_OWNERSHIP_RULES_MQH__
#property strict

#include "FP_OwnershipTypes.mqh"
#include "FP_Identity.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 10 / Ownership Rules
// ============================================================================

string FP_Level10AppendId(const string ids, const int id)
{
   string one = "Q" + IntegerToString(id);
   if(ids == "") return one;
   return ids + "," + one;
}

int FP_Level10EventEndAnchor(const FP_FlagEvent &e)
{
   if(e.has_extension && e.extension_end.index_anchor >= 0) return e.extension_end.index_anchor;
   if(e.has_confirm && e.confirm.index_anchor >= 0) return e.confirm.index_anchor;
   if(e.has_leg2 && e.leg2.index_anchor >= 0) return e.leg2.index_anchor;
   if(e.has_waist && e.waist.index_anchor >= 0) return e.waist.index_anchor;
   if(e.has_leg1 && e.leg1.index_anchor >= 0) return e.leg1.index_anchor;
   if(e.has_origin && e.origin.index_anchor >= 0) return e.origin.index_anchor;
   return -1;
}

int FP_Level10StatusRank(const FP_FlagEvent &e)
{
   if(e.status == FP_STATUS_LOCKED) return 900;
   if(e.status == FP_STATUS_COMPLETED) return 800;
   if(e.status == FP_STATUS_CONFIRMED) return 700;
   if(e.status == FP_STATUS_QUALIFIED) return 600;
   if(e.status == FP_STATUS_POST_FLAG) return 500;
   if(e.status == FP_STATUS_LIVE_BODY) return 400;
   if(e.status == FP_STATUS_LIVE_LEG) return 300;
   if(e.status == FP_STATUS_SEED) return 200;
   if(e.status == FP_STATUS_INVALIDATED) return 50;
   return 0;
}

bool FP_Level10IsRootF1(const FP_FlagEvent &e)
{
   return (e.level == FP_LEVEL_F1 && e.chain_index == 1 && e.has_origin);
}

bool FP_Level10IsVisibleRootF1(const FP_FlagEvent &e)
{
   return (FP_Level10IsRootF1(e) && e.visible_main);
}

bool FP_Level10IsConfirmedF1(const FP_FlagEvent &e)
{
   return (e.level == FP_LEVEL_F1 && e.status == FP_STATUS_CONFIRMED && e.has_confirm);
}

bool FP_Level10IsConfirmedF2(const FP_FlagEvent &e)
{
   return (e.level == FP_LEVEL_F2 && e.status == FP_STATUS_CONFIRMED && e.has_confirm && e.f2_can_spawn_f3);
}

bool FP_Level10IsTerminalF3(const FP_FlagEvent &e)
{
   return (e.level == FP_LEVEL_F3 && (e.status == FP_STATUS_COMPLETED || e.status == FP_STATUS_LOCKED));
}

int FP_Level10ChainStateForSequence(const FP_FlagEvent &events[], const int n, const int sequence_id)
{
   bool has_f1 = false;
   bool has_f2 = false;
   bool has_f3 = false;
   bool locked_f3 = false;
   bool completed_f3 = false;
   bool confirmed_f2 = false;
   bool confirmed_f1 = false;

   for(int i=0; i<n; i++)
   {
      if(events[i].sequence_id != sequence_id) continue;
      if(events[i].level == FP_LEVEL_F1)
      {
         has_f1 = true;
         if(FP_Level10IsConfirmedF1(events[i])) confirmed_f1 = true;
      }
      else if(events[i].level == FP_LEVEL_F2)
      {
         has_f2 = true;
         if(FP_Level10IsConfirmedF2(events[i])) confirmed_f2 = true;
      }
      else if(events[i].level == FP_LEVEL_F3)
      {
         has_f3 = true;
         if(events[i].status == FP_STATUS_LOCKED) locked_f3 = true;
         if(FP_Level10IsTerminalF3(events[i])) completed_f3 = true;
      }
   }

   if(locked_f3) return FP_CHAIN_LOCKED_BY_OP_F1;
   if(completed_f3) return FP_CHAIN_F3_EXTENSION;
   if(has_f3) return FP_CHAIN_F3_OWNER;
   if(confirmed_f2) return FP_CHAIN_F3_SEARCH;
   if(has_f2) return FP_CHAIN_F2_OWNER;
   if(confirmed_f1) return FP_CHAIN_F2_SEARCH;
   if(has_f1) return FP_CHAIN_F1_OWNER;
   return FP_CHAIN_NONE;
}

int FP_Level10NextExpectedLevel(const int chain_state)
{
   if(chain_state == FP_CHAIN_F1_OWNER || chain_state == FP_CHAIN_F2_SEARCH) return FP_LEVEL_F2;
   if(chain_state == FP_CHAIN_F2_OWNER || chain_state == FP_CHAIN_F3_SEARCH) return FP_LEVEL_F3;
   if(chain_state == FP_CHAIN_F3_OWNER || chain_state == FP_CHAIN_F3_EXTENSION) return FP_LEVEL_NONE;
   if(chain_state == FP_CHAIN_LOCKED_BY_OP_F1 || chain_state == FP_CHAIN_RESET_ALLOWED) return FP_LEVEL_F1;
   return FP_LEVEL_F1;
}

int FP_Level10ChainMaturityScore(const FP_FlagEvent &events[], const int n, const FP_FlagEvent &root)
{
   int score = FP_Level10StatusRank(root);

   // Canonical semantic ranking from the Level 10 contract.
   for(int i=0; i<n; i++)
   {
      if(events[i].sequence_id != root.sequence_id) continue;

      if(events[i].level == FP_LEVEL_F3 && events[i].status == FP_STATUS_LOCKED)
         score += 12000 + FP_Level10StatusRank(events[i]);
      else if(events[i].level == FP_LEVEL_F3 && events[i].status == FP_STATUS_COMPLETED)
         score += 9000 + FP_Level10StatusRank(events[i]);
      else if(FP_Level10IsConfirmedF2(events[i]))
         score += 6000 + FP_Level10StatusRank(events[i]);
      else if(FP_Level10IsConfirmedF1(events[i]))
         score += 3000 + FP_Level10StatusRank(events[i]);
      else if(events[i].level == FP_LEVEL_F2)
         score += 1000 + FP_Level10StatusRank(events[i]);
   }

   if(root.from_phase_boundary) score += 500;
   if(!root.from_fail_open) score += 150;

   // Prefer local/lower-L only after semantic maturity and source quality.
   score -= MathMax(0, root.scale_L) * 5;

   // Deterministic tie-break: earlier valid root wins if all semantic quality is equal.
   score -= MathMax(0, root.origin.index_anchor) / 100000;
   return score;
}

bool FP_Level10HasOppositeF3ResetBetweenRoots(const FP_FlagEvent &events[],
                                              const int n,
                                              const int direction,
                                              const int from_anchor,
                                              const int to_anchor,
                                              int &reset_event_index)
{
   reset_event_index = -1;
   if(to_anchor <= from_anchor) return false;
   for(int i=0; i<n; i++)
   {
      if(events[i].direction == direction) continue;
      if(!FP_Level10IsTerminalF3(events[i])) continue;
      int t = FP_Level10EventEndAnchor(events[i]);
      if(t > from_anchor && t < to_anchor)
      {
         reset_event_index = i;
         return true;
      }
   }
   return false;
}

bool FP_Level10PhaseRootCoversFailOpenRoot(const FP_FlagEvent &phase_root, const FP_FlagEvent &fail_root)
{
   if(!phase_root.visible_main) return false;
   if(!FP_Level10IsRootF1(phase_root)) return false;
   if(!phase_root.from_phase_boundary) return false;
   if(phase_root.direction != fail_root.direction) return false;
   if(phase_root.scale_L != fail_root.scale_L) return false;
   if(!phase_root.has_leg2 || !fail_root.has_origin) return false;
   return (phase_root.origin.index_anchor <= fail_root.origin.index_anchor &&
           phase_root.leg2.index_anchor >= fail_root.origin.index_anchor);
}

#endif // __FP_OWNERSHIP_RULES_MQH__
