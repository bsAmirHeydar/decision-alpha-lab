#ifndef __FP_HOOK_AUDIT_MQH__
#define __FP_HOOK_AUDIT_MQH__
#property strict

#include "FP_NodeEngine.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 04 / Hook-ND Audit
// ----------------------------------------------------------------------------
// This file owns Hook/ND build reports only.  It does not create hooks and it
// does not draw anything.  The purpose is to make every Hook context decision
// auditable before the renderer is trusted.
// ============================================================================

string FP_HookNodeAuditText(const FP_Node &n)
{
   if(n.id < 0) return "none";
   return FP_NodeKindName(n.kind) + "#" + IntegerToString(n.id) +
          " L" + IntegerToString(n.L) +
          " i" + IntegerToString(n.index_anchor) +
          " p" + DoubleToString(n.price, _Digits);
}

struct FP_HookBuildReport
{
   int    scale_L;
   int    node_count;
   int    same_side_contexts_seen;
   int    contexts_no_boundary;
   int    contexts_too_short;
   int    contexts_cycle_broken;
   int    contexts_overextended;
   int    branch_scans;
   int    branch_len_1;
   int    branch_len_2;
   int    branch_len_3;
   int    branch_len_4;
   int    branch_len_5plus;
   int    nd_candidate_branches;
   int    retrace_rejected;
   int    duplicates_skipped;
   int    same_resolve_replaced;
   int    same_resolve_kept_existing;
   int    hooks_emitted;
   int    nd_emitted;
   int    max_branch_len_seen;
   int    first_resolve_index;
   int    last_resolve_index;
   string status;
   string reason;
};

void FP_ResetHookBuildReport(FP_HookBuildReport &r)
{
   r.scale_L = 0;
   r.node_count = 0;
   r.same_side_contexts_seen = 0;
   r.contexts_no_boundary = 0;
   r.contexts_too_short = 0;
   r.contexts_cycle_broken = 0;
   r.contexts_overextended = 0;
   r.branch_scans = 0;
   r.branch_len_1 = 0;
   r.branch_len_2 = 0;
   r.branch_len_3 = 0;
   r.branch_len_4 = 0;
   r.branch_len_5plus = 0;
   r.nd_candidate_branches = 0;
   r.retrace_rejected = 0;
   r.duplicates_skipped = 0;
   r.same_resolve_replaced = 0;
   r.same_resolve_kept_existing = 0;
   r.hooks_emitted = 0;
   r.nd_emitted = 0;
   r.max_branch_len_seen = 0;
   r.first_resolve_index = -1;
   r.last_resolve_index = -1;
   r.status = "reset";
   r.reason = "reset";
}

void FP_InitHookBuildReport(FP_HookBuildReport &r, const int scale_L, const int node_count)
{
   FP_ResetHookBuildReport(r);
   r.scale_L = scale_L;
   r.node_count = node_count;
   r.status = "ok";
   r.reason = "level04_hook_scan_ready";
}

void FP_HookReportRegisterBranchLength(FP_HookBuildReport &r, const int branch_len)
{
   r.branch_scans++;
   if(branch_len > r.max_branch_len_seen) r.max_branch_len_seen = branch_len;
   if(branch_len <= 0) return;
   if(branch_len == 1) r.branch_len_1++;
   else if(branch_len == 2) r.branch_len_2++;
   else if(branch_len == 3) r.branch_len_3++;
   else if(branch_len == 4) r.branch_len_4++;
   else r.branch_len_5plus++;
}

void FP_HookReportRegisterResolve(FP_HookBuildReport &r, const FP_Node &resolve)
{
   if(resolve.index_anchor < 0) return;
   if(r.first_resolve_index < 0 || resolve.index_anchor < r.first_resolve_index)
      r.first_resolve_index = resolve.index_anchor;
   if(r.last_resolve_index < 0 || resolve.index_anchor > r.last_resolve_index)
      r.last_resolve_index = resolve.index_anchor;
}

void FP_FinalizeHookBuildReport(FP_HookBuildReport &r)
{
   if(r.contexts_cycle_broken > 0 || r.contexts_overextended > 0 || r.retrace_rejected > 0)
   {
      r.status = "ok_with_rejections";
      r.reason = "level04_hook_scan_rejections_audited";
   }
   else
   {
      r.status = "ok";
      r.reason = "level04_hook_scan_complete";
   }
}

void FP_PrintHookBuildReport(const string tag, const FP_HookBuildReport &r)
{
   Print(tag,
         " status=", r.status,
         " reason=", r.reason,
         " L=", r.scale_L,
         " nodes=", r.node_count,
         " contexts=", r.same_side_contexts_seen,
         " no_boundary=", r.contexts_no_boundary,
         " too_short=", r.contexts_too_short,
         " cycle_broken=", r.contexts_cycle_broken,
         " overextended=", r.contexts_overextended,
         " branch_scans=", r.branch_scans,
         " len1=", r.branch_len_1,
         " len2=", r.branch_len_2,
         " len3=", r.branch_len_3,
         " len4=", r.branch_len_4,
         " len5plus=", r.branch_len_5plus,
         " nd_candidates=", r.nd_candidate_branches,
         " retrace_rejected=", r.retrace_rejected,
         " duplicates=", r.duplicates_skipped,
         " same_resolve_replaced=", r.same_resolve_replaced,
         " same_resolve_kept=", r.same_resolve_kept_existing,
         " hooks=", r.hooks_emitted,
         " nd=", r.nd_emitted,
         " max_branch_len=", r.max_branch_len_seen,
         " first_resolve=", r.first_resolve_index,
         " last_resolve=", r.last_resolve_index);
}

void FP_PrintHookSamples(const string tag, const FP_HookBranch &hooks[], const int hook_count, const int sample_limit)
{
   int limit = MathMax(0, sample_limit);
   for(int i=0; i<hook_count && i<limit; i++)
   {
      Print(tag,
            " SAMPLE id=", hooks[i].branch_id,
            " L=", hooks[i].scale_L,
            " dir=", FP_DirectionName(hooks[i].direction),
            " side=", FP_NodeKindName(hooks[i].side_kind),
            " nodes=", hooks[i].node_count,
            " max_branch_len=", hooks[i].max_branch_len,
            " nd=", FP_BoolName(hooks[i].is_nd),
            " nd_qualified=", FP_BoolName(hooks[i].nd_qualified),
            " cycle_broken=", FP_BoolName(hooks[i].is_cycle_start_broken),
            " seeds_visible_f1=", FP_BoolName(hooks[i].seeds_visible_f1),
            " visible=", FP_BoolName(hooks[i].visible_main),
            " hidden_reason=", hooks[i].hidden_reason,
            " retrace=", DoubleToString(hooks[i].retrace_ratio, 4),
            " cycle=", FP_HookNodeAuditText(hooks[i].cycle_start_node),
            " extreme=", FP_HookNodeAuditText(hooks[i].extreme_node),
            " resolve=", FP_HookNodeAuditText(hooks[i].resolve_node),
            " reason=", hooks[i].reason);
   }
}


void FP_PrintHookSeedSummary(const string tag, const FP_HookBranch &hooks[])
{
   int total = ArraySize(hooks);
   int seeded = 0;
   int visible = 0;
   int hidden = 0;
   int hidden_with_reason = 0;
   for(int i=0; i<total; i++)
   {
      if(hooks[i].seeds_visible_f1) seeded++;
      if(hooks[i].visible_main) visible++;
      else
      {
         hidden++;
         if(hooks[i].hidden_reason != "") hidden_with_reason++;
      }
   }
   Print(tag,
         " status=ok",
         " reason=level04_hook_seed_visibility_marked",
         " hooks=", total,
         " seeds_visible_f1=", seeded,
         " visible=", visible,
         " hidden=", hidden,
         " hidden_with_reason=", hidden_with_reason);
}

#endif // __FP_HOOK_AUDIT_MQH__
