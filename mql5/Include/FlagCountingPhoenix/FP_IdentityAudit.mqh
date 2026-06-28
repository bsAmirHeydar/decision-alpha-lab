#ifndef __FP_IDENTITY_AUDIT_MQH__
#define __FP_IDENTITY_AUDIT_MQH__
#property strict

#include "FP_Identity.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 03 / Identity Audit
// ============================================================================

struct FP_IdentityReport
{
   int events_total;
   int events_with_structural_id;
   int events_with_visual_id;
   int events_with_phase_id;
   int events_with_chain_id;
   int events_with_audit_id;
   int hidden_events;
   int hidden_with_reason;
   int hooks_total;
   int hooks_with_identity;
   int duplicate_visible_event_ids;
   string status;
   string reason;
};

void FP_ResetIdentityReport(FP_IdentityReport &r)
{
   r.events_total = 0;
   r.events_with_structural_id = 0;
   r.events_with_visual_id = 0;
   r.events_with_phase_id = 0;
   r.events_with_chain_id = 0;
   r.events_with_audit_id = 0;
   r.hidden_events = 0;
   r.hidden_with_reason = 0;
   r.hooks_total = 0;
   r.hooks_with_identity = 0;
   r.duplicate_visible_event_ids = 0;
   r.status = "reset";
   r.reason = "reset";
}

bool FP_VisibleEventVisualDuplicateExists(const FP_FlagEvent &events[], const int n, const int idx)
{
   if(idx < 0 || idx >= n) return false;
   if(!events[idx].visible_main) return false;
   if(events[idx].visual_id == "") return false;
   for(int j=0; j<n; j++)
   {
      if(j == idx) continue;
      if(!events[j].visible_main) continue;
      if(events[j].visual_id == events[idx].visual_id && FP_SamePhaseForMerge(events[j], events[idx])) return true;
   }
   return false;
}

void FP_BuildIdentityReport(const FP_FlagEvent &events[],
                            const FP_HookBranch &hooks[],
                            FP_IdentityReport &r)
{
   FP_ResetIdentityReport(r);
   int n = ArraySize(events);
   r.events_total = n;
   for(int i=0; i<n; i++)
   {
      if(events[i].structural_id != "") r.events_with_structural_id++;
      if(events[i].visual_id != "") r.events_with_visual_id++;
      if(events[i].phase_id != "") r.events_with_phase_id++;
      if(events[i].chain_id != "") r.events_with_chain_id++;
      if(events[i].audit_id != "") r.events_with_audit_id++;
      if(!events[i].visible_main)
      {
         r.hidden_events++;
         if(events[i].hidden_reason != "") r.hidden_with_reason++;
      }
      if(FP_VisibleEventVisualDuplicateExists(events, n, i)) r.duplicate_visible_event_ids++;
   }

   r.hooks_total = ArraySize(hooks);
   for(int h=0; h<ArraySize(hooks); h++)
   {
      if(hooks[h].structural_id != "" && hooks[h].visual_id != "" && hooks[h].phase_id != "" && hooks[h].audit_id != "")
         r.hooks_with_identity++;
   }

   bool ok_events = (r.events_total == 0 ||
                     (r.events_with_structural_id == r.events_total &&
                      r.events_with_visual_id == r.events_total &&
                      r.events_with_phase_id == r.events_total &&
                      r.events_with_chain_id == r.events_total &&
                      r.events_with_audit_id == r.events_total));
   bool ok_hidden = (r.hidden_events == r.hidden_with_reason);
   bool ok_hooks = (r.hooks_total == r.hooks_with_identity);
   bool ok_dupes = (r.duplicate_visible_event_ids == 0);

   if(ok_events && ok_hidden && ok_hooks && ok_dupes)
   {
      r.status = "ok";
      r.reason = "level03_identity_ready";
   }
   else
   {
      r.status = "failed";
      r.reason = "identity_contract_violation";
   }
}

void FP_PrintIdentityReport(const string tag, const FP_IdentityReport &r)
{
   Print(tag,
         " status=", r.status,
         " reason=", r.reason,
         " events=", r.events_total,
         " structural=", r.events_with_structural_id,
         " visual=", r.events_with_visual_id,
         " phase=", r.events_with_phase_id,
         " chain=", r.events_with_chain_id,
         " audit=", r.events_with_audit_id,
         " hidden=", r.hidden_events,
         " hidden_with_reason=", r.hidden_with_reason,
         " hooks=", r.hooks_total,
         " hooks_with_identity=", r.hooks_with_identity,
         " duplicate_visible_visual_ids=", r.duplicate_visible_event_ids);
}

void FP_PrintIdentitySamples(const string tag,
                             const FP_FlagEvent &events[],
                             const FP_HookBranch &hooks[],
                             const int sample_limit)
{
   int limit = MathMax(0, sample_limit);
   int printed = 0;
   for(int i=0; i<ArraySize(events) && printed < limit; i++)
   {
      Print(tag,
            " EVENT_SAMPLE id=", events[i].event_id,
            " visible=", FP_BoolName(events[i].visible_main),
            " structural_id=", events[i].structural_id,
            " visual_id=", events[i].visual_id,
            " phase_id=", events[i].phase_id,
            " chain_id=", events[i].chain_id,
            " audit_id=", events[i].audit_id,
            " hidden_reason=", events[i].hidden_reason);
      printed++;
   }

   printed = 0;
   for(int h=0; h<ArraySize(hooks) && printed < limit; h++)
   {
      Print(tag,
            " HOOK_SAMPLE id=", hooks[h].branch_id,
            " structural_id=", hooks[h].structural_id,
            " visual_id=", hooks[h].visual_id,
            " phase_id=", hooks[h].phase_id,
            " audit_id=", hooks[h].audit_id);
      printed++;
   }
}

void FP_PrintIdentitySummary(const string tag,
                             const FP_FlagEvent &events[],
                             const FP_HookBranch &hooks[],
                             const FP_Config &cfg)
{
   FP_IdentityReport r;
   FP_BuildIdentityReport(events, hooks, r);
   FP_PrintIdentityReport(tag, r);
   if(cfg.print_identity_samples)
      FP_PrintIdentitySamples(tag, events, hooks, cfg.identity_sample_limit);
}

#endif // __FP_IDENTITY_AUDIT_MQH__
