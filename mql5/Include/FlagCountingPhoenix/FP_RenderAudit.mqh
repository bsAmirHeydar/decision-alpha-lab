#ifndef __FP_RENDER_AUDIT_MQH__
#define __FP_RENDER_AUDIT_MQH__
#property strict

#include "FP_RenderRules.mqh"

// ============================================================================
// Phoenix Level 12 - Render Audit
// ============================================================================

void FP_PrintRenderReport(const string tag, const FP_RenderReport &r)
{
   string msg = tag;
   msg += " status=" + r.status;
   msg += " ok=" + FP_BoolName(r.ok);
   msg += " reason=" + r.reason;
   msg += " prefix=" + r.prefix;
   msg += " events_in=" + IntegerToString(r.input_events);
   msg += " hooks_in=" + IntegerToString(r.input_hooks);
   msg += " visible_events=" + IntegerToString(r.visible_events_seen);
   msg += " visible_hooks=" + IntegerToString(r.visible_hooks_seen);
   msg += " drawn_events=" + IntegerToString(r.drawn_events);
   msg += " drawn_hooks=" + IntegerToString(r.drawn_hooks);
   msg += " drawn_total=" + IntegerToString(r.drawn_total);
   msg += " objects_requested=" + IntegerToString(r.objects_requested);
   msg += " objects_created=" + IntegerToString(r.objects_created);
   msg += " object_errors=" + IntegerToString(r.object_create_failures);
   msg += " objects_deleted=" + IntegerToString(r.objects_deleted_by_prefix);
   msg += " duplicate_names=" + IntegerToString(r.duplicate_object_names);
   msg += " fallback_curves=" + IntegerToString(r.fallback_curves);
   msg += " ev_body=" + IntegerToString(r.event_body_drawn);
   msg += " ev_probable=" + IntegerToString(r.event_probable_drawn);
   msg += " ev_labels=" + IntegerToString(r.event_label_drawn);
   msg += " hk_arcs=" + IntegerToString(r.hook_arcs_drawn);
   msg += " hk_labels=" + IntegerToString(r.hook_labels_drawn);
   msg += " ev_filter_level=" + IntegerToString(r.event_filter_level);
   msg += " ev_filter_dir=" + IntegerToString(r.event_filter_direction);
   msg += " ev_filter_status=" + IntegerToString(r.event_filter_status);
   msg += " ev_filter_visible=" + IntegerToString(r.event_filter_visibility);
   msg += " ev_filter_kind=" + IntegerToString(r.event_filter_render_kind);
   msg += " ev_filter_limit=" + IntegerToString(r.event_filter_limit);
   msg += " ev_filter_malformed=" + IntegerToString(r.event_filter_malformed);
   msg += " hk_filter_visible=" + IntegerToString(r.hook_filter_visibility);
   msg += " hk_filter_nd=" + IntegerToString(r.hook_filter_nd);
   msg += " hk_filter_seed=" + IntegerToString(r.hook_filter_seed);
   msg += " hk_filter_limit=" + IntegerToString(r.hook_filter_limit);
   msg += " hk_filter_malformed=" + IntegerToString(r.hook_filter_malformed);
   msg += " first_event=" + IntegerToString(r.first_drawn_event_id);
   msg += " last_event=" + IntegerToString(r.last_drawn_event_id);
   msg += " first_hook=" + IntegerToString(r.first_drawn_hook_id);
   msg += " last_hook=" + IntegerToString(r.last_drawn_hook_id);
   Print(msg);
}

void FP_PrintRenderSamples(const string tag, const FP_RenderReport &r)
{
   if(StringLen(r.samples) <= 0)
   {
      Print(tag, " samples=none");
      return;
   }
   Print(tag, " samples=", r.samples);
}

#endif // __FP_RENDER_AUDIT_MQH__
