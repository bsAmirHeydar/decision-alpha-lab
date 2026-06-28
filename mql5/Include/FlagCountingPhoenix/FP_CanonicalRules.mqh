#ifndef __FP_CANONICAL_RULES_MQH__
#define __FP_CANONICAL_RULES_MQH__
#property strict

#include "FP_Identity.mqh"
#include "FP_CanonicalTypes.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 11 / Canonicalization Rules
// ----------------------------------------------------------------------------
// Pure helpers for final stream consistency.  These rules do not scan price and
// do not create new F events. They only classify and rank already-emitted events.
// ============================================================================

bool FP_CanonicalHasRequiredBody(const FP_FlagEvent &e)
{
   if(e.level != FP_LEVEL_F1 && e.level != FP_LEVEL_F2 && e.level != FP_LEVEL_F3) return true;
   if(!e.has_origin || !e.has_leg1) return false;
   if(e.status == FP_STATUS_LIVE_LEG || e.status == FP_STATUS_SEED) return true;
   if(!e.has_waist || !e.has_leg2) return false;
   if(e.origin.index_anchor < 0 || e.leg1.index_anchor < 0) return false;
   if(e.has_waist && e.waist.index_anchor < 0) return false;
   if(e.has_leg2 && e.leg2.index_anchor < 0) return false;
   return true;
}

bool FP_CanonicalIsInvalidVisible(const FP_FlagEvent &e, const FP_Config &cfg)
{
   return (e.visible_main && e.status == FP_STATUS_INVALIDATED && !cfg.show_invalidated_in_audit);
}

bool FP_CanonicalShouldHideRenderNone(const FP_FlagEvent &e)
{
   return (e.visible_main && e.render_kind == FP_RENDER_NONE);
}

bool FP_CanonicalIdentityMissing(const FP_FlagEvent &e)
{
   if(e.structural_id == "") return true;
   if(e.visual_id == "") return true;
   if(e.phase_id == "") return true;
   if(e.chain_id == "") return true;
   if(e.audit_id == "") return true;
   return false;
}

bool FP_CanonicalHiddenReasonMissing(const FP_FlagEvent &e)
{
   return (!e.visible_main && e.hidden_reason == "");
}

bool FP_CanonicalParentRequired(const FP_FlagEvent &e)
{
   return (e.level == FP_LEVEL_F2 || e.level == FP_LEVEL_F3 || e.chain_index > 1);
}

int FP_CanonicalFindParentIndex(const FP_FlagEvent &events[], const int n, const FP_FlagEvent &child)
{
   int wanted_chain = child.chain_index - 1;
   if(wanted_chain < 1) return -1;

   int best = -1;
   for(int i=0; i<n; i++)
   {
      if(events[i].sequence_id != child.sequence_id) continue;
      if(events[i].chain_index != wanted_chain) continue;
      if(events[i].direction != child.direction) continue;
      if(events[i].origin.index_anchor > child.origin.index_anchor) continue;
      if(best < 0 || events[i].origin.index_anchor > events[best].origin.index_anchor) best = i;
   }
   return best;
}

bool FP_CanonicalParentVisible(const FP_FlagEvent &events[], const int n, const FP_FlagEvent &child)
{
   int p = FP_CanonicalFindParentIndex(events, n, child);
   if(p < 0) return false;
   return events[p].visible_main;
}

bool FP_CanonicalIsVisibleOrphan(const FP_FlagEvent &events[], const int n, const FP_FlagEvent &e)
{
   if(!e.visible_main) return false;
   if(!FP_CanonicalParentRequired(e)) return false;
   return !FP_CanonicalParentVisible(events, n, e);
}

int FP_CanonicalSemanticRank(const FP_FlagEvent &events[], const int n, const FP_FlagEvent &e)
{
   int score = 0;
   score += FP_EventBaseCanonicalRank(e);
   score += e.owner_rank_score;
   if(e.level == FP_LEVEL_F3 && e.f3_locked) score += 1200;
   if(e.level == FP_LEVEL_F3 && e.f3_terminal_complete) score += 900;
   if(e.level == FP_LEVEL_F2 && e.f2_can_spawn_f3) score += 600;
   if(e.level == FP_LEVEL_F1 && e.lifecycle_can_spawn_f2) score += 300;
   if(e.from_phase_boundary) score += 80;
   if(!e.from_fail_open) score += 25;
   bool has_child = false;
   for(int ci=0; ci<n; ci++)
   {
      if(!events[ci].visible_main) continue;
      if(events[ci].sequence_id != e.sequence_id) continue;
      if(events[ci].chain_index > e.chain_index)
      {
         has_child = true;
         break;
      }
   }
   if(has_child) score += 60;
   score -= MathMax(0, e.scale_L);
   return score;
}

bool FP_CanonicalSameVisibleConflict(const FP_FlagEvent &a, const FP_FlagEvent &b)
{
   if(a.level != b.level) return false;
   if(a.direction != b.direction) return false;
   if(!FP_SamePhaseForMerge(a, b)) return false;
   if(a.visual_id != "" && b.visual_id != "" && a.visual_id == b.visual_id) return true;
   if(FP_SameBodyVisualIdentity(a, b)) return true;
   return false;
}

string FP_CanonicalConflictGroupId(const FP_FlagEvent &e)
{
   if(e.visual_id != "") return e.visual_id;
   return "CG:" + FP_LevelKey(e.level) + "|" + FP_DirectionKey(e.direction) + "|" + FP_BodyNodeVisualKey(e);
}

void FP_CanonicalSetState(FP_FlagEvent &e, const int state, const string reason)
{
   e.canonical_state = state;
   if(reason != "") e.canonical_reason = reason;
   if(!e.visible_main)
   {
      if(e.hidden_reason == "") e.hidden_reason = FP_CanonicalStateName(state);
      if(StringFind(e.reason, e.hidden_reason) < 0) e.reason = e.reason + ";" + e.hidden_reason;
   }
}

#endif // __FP_CANONICAL_RULES_MQH__
