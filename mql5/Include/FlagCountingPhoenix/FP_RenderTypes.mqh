#ifndef __FP_RENDER_TYPES_MQH__
#define __FP_RENDER_TYPES_MQH__
#property strict

#include "FP_SequenceEngine.mqh"

// ============================================================================
// Phoenix Level 12 - Render Types
// ----------------------------------------------------------------------------
// The renderer is a read-only consumer of the canonical Level 11 stream.  These
// types describe how the stream is drawn and what was actually emitted to chart.
// They do not carry any market-structure authority.
// ============================================================================

struct FP_RenderConfig
{
   string prefix;
   int    max_events_to_draw;
   int    max_hooks_to_draw;

   bool   draw_f1;
   bool   draw_f2;
   bool   draw_f3;
   bool   draw_bull;
   bool   draw_bear;
   bool   draw_candidates;
   bool   draw_confirmed;
   bool   draw_locked;
   bool   draw_invalidated;
   bool   draw_hooks;
   bool   draw_only_flag_seed_hooks;

   bool   show_hook_count_labels;
   bool   detailed_labels;
   bool   show_parent_ids;
   bool   show_origin_labels;
   bool   show_internal_labels;
   bool   use_sequence_color_shades;

   int    fixed_line_width;
   int    curve_segments;
   int    label_font_size;

   color  bull_candidate;
   color  bull_confirmed;
   color  bear_candidate;
   color  bear_confirmed;
   color  f3_locked;
   color  hook_color;

   // Level 12 controls.
   bool   delete_existing_by_prefix;
   bool   strict_visibility;
   bool   use_canonical_object_names;
   bool   draw_hook_back;
   bool   print_sanity;
   bool   print_samples;
   int    sample_limit;
};

struct FP_RenderReport
{
   bool   attempted;
   bool   ok;
   string status;
   string reason;
   string prefix;

   int    input_events;
   int    input_hooks;
   int    visible_events_seen;
   int    visible_hooks_seen;

   int    event_filter_level;
   int    event_filter_direction;
   int    event_filter_status;
   int    event_filter_visibility;
   int    event_filter_render_kind;
   int    event_filter_limit;
   int    event_filter_malformed;

   int    hook_filter_visibility;
   int    hook_filter_nd;
   int    hook_filter_seed;
   int    hook_filter_limit;
   int    hook_filter_malformed;

   int    event_body_drawn;
   int    event_probable_drawn;
   int    event_label_drawn;
   int    event_origin_labels;
   int    event_internal_labels;
   int    hook_arcs_drawn;
   int    hook_labels_drawn;
   int    hook_count_labels;

   int    objects_requested;
   int    objects_created;
   int    object_create_failures;
   int    objects_deleted_by_prefix;
   int    duplicate_object_names;
   int    fallback_curves;

   int    drawn_events;
   int    drawn_hooks;
   int    drawn_total;

   int    first_drawn_event_id;
   int    last_drawn_event_id;
   int    first_drawn_hook_id;
   int    last_drawn_hook_id;

   string samples;
};

void FP_ResetRenderReport(FP_RenderReport &r)
{
   r.attempted = false;
   r.ok = true;
   r.status = "not_run";
   r.reason = "";
   r.prefix = "";
   r.input_events = 0;
   r.input_hooks = 0;
   r.visible_events_seen = 0;
   r.visible_hooks_seen = 0;
   r.event_filter_level = 0;
   r.event_filter_direction = 0;
   r.event_filter_status = 0;
   r.event_filter_visibility = 0;
   r.event_filter_render_kind = 0;
   r.event_filter_limit = 0;
   r.event_filter_malformed = 0;
   r.hook_filter_visibility = 0;
   r.hook_filter_nd = 0;
   r.hook_filter_seed = 0;
   r.hook_filter_limit = 0;
   r.hook_filter_malformed = 0;
   r.event_body_drawn = 0;
   r.event_probable_drawn = 0;
   r.event_label_drawn = 0;
   r.event_origin_labels = 0;
   r.event_internal_labels = 0;
   r.hook_arcs_drawn = 0;
   r.hook_labels_drawn = 0;
   r.hook_count_labels = 0;
   r.objects_requested = 0;
   r.objects_created = 0;
   r.object_create_failures = 0;
   r.objects_deleted_by_prefix = 0;
   r.duplicate_object_names = 0;
   r.fallback_curves = 0;
   r.drawn_events = 0;
   r.drawn_hooks = 0;
   r.drawn_total = 0;
   r.first_drawn_event_id = -1;
   r.last_drawn_event_id = -1;
   r.first_drawn_hook_id = -1;
   r.last_drawn_hook_id = -1;
   r.samples = "";
}

void FP_DefaultRenderConfig(FP_RenderConfig &cfg)
{
   cfg.prefix = "DAL_FCP_";
   cfg.max_events_to_draw = 1200;
   cfg.max_hooks_to_draw = 120;
   cfg.draw_f1 = true;
   cfg.draw_f2 = true;
   cfg.draw_f3 = true;
   cfg.draw_bull = true;
   cfg.draw_bear = true;
   cfg.draw_candidates = true;
   cfg.draw_confirmed = true;
   cfg.draw_locked = true;
   cfg.draw_invalidated = false;
   cfg.draw_hooks = true;
   cfg.draw_only_flag_seed_hooks = false;
   cfg.show_hook_count_labels = false;
   cfg.detailed_labels = false;
   cfg.show_parent_ids = false;
   cfg.show_origin_labels = false;
   cfg.show_internal_labels = false;
   cfg.use_sequence_color_shades = true;
   cfg.fixed_line_width = 1;
   cfg.curve_segments = 32;
   cfg.label_font_size = 8;
   cfg.bull_candidate = clrDeepSkyBlue;
   cfg.bull_confirmed = clrLime;
   cfg.bear_candidate = clrOrange;
   cfg.bear_confirmed = clrTomato;
   cfg.f3_locked = clrMagenta;
   cfg.hook_color = clrGray;
   cfg.delete_existing_by_prefix = true;
   cfg.strict_visibility = true;
   cfg.use_canonical_object_names = true;
   cfg.draw_hook_back = true;
   cfg.print_sanity = true;
   cfg.print_samples = false;
   cfg.sample_limit = 8;
}

void FP_RenderApplyReportToResult(const FP_RenderReport &rr, FP_DetectResult &result)
{
   result.render_attempted_total += (rr.attempted ? 1 : 0);
   result.render_ok_total += (rr.ok ? 1 : 0);
   result.render_objects_total += rr.objects_created;
   result.render_object_errors_total += rr.object_create_failures;
   result.render_deleted_objects_total += rr.objects_deleted_by_prefix;
   result.render_events_drawn_total += rr.drawn_events;
   result.render_hooks_drawn_total += rr.drawn_hooks;
   result.render_event_filtered_total += rr.event_filter_level + rr.event_filter_direction + rr.event_filter_status + rr.event_filter_visibility + rr.event_filter_render_kind + rr.event_filter_limit + rr.event_filter_malformed;
   result.render_hook_filtered_total += rr.hook_filter_visibility + rr.hook_filter_nd + rr.hook_filter_seed + rr.hook_filter_limit + rr.hook_filter_malformed;
   result.render_duplicate_names_total += rr.duplicate_object_names;
   result.render_fallback_curves_total += rr.fallback_curves;
}

#endif // __FP_RENDER_TYPES_MQH__
