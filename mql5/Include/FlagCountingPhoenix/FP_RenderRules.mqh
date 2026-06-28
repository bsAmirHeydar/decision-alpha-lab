#ifndef __FP_RENDER_RULES_MQH__
#define __FP_RENDER_RULES_MQH__
#property strict

#include "FP_RenderTypes.mqh"

// ============================================================================
// Phoenix Level 12 - Render Rules
// ----------------------------------------------------------------------------
// Pure renderer-side rules. These functions filter and name chart objects only;
// they never infer structure and never mutate events or hooks.
// ============================================================================

string FP_RenderSafeId(string raw, const int max_len=56)
{
   if(StringLen(raw) <= 0) raw = "na";
   string out = "";
   int n = StringLen(raw);
   for(int i=0; i<n; i++)
   {
      ushort ch = StringGetCharacter(raw, i);
      bool ok = ((ch >= '0' && ch <= '9') ||
                 (ch >= 'A' && ch <= 'Z') ||
                 (ch >= 'a' && ch <= 'z') ||
                 ch == '_' || ch == '-' || ch == '.');
      out += (ok ? StringSubstr(raw, i, 1) : "_");
      if(StringLen(out) >= max_len) break;
   }
   return out;
}

string FP_RenderEventObjectStem(const FP_FlagEvent &e, const FP_RenderConfig &cfg)
{
   string id = "";
   if(cfg.use_canonical_object_names && StringLen(e.canonical_id) > 0) id = e.canonical_id;
   else if(cfg.use_canonical_object_names && StringLen(e.visual_id) > 0) id = e.visual_id;
   else id = "Q" + IntegerToString(e.event_id);
   return cfg.prefix + "EV_" + FP_RenderSafeId(id, 64) + "_";
}

string FP_RenderHookObjectStem(const FP_HookBranch &h, const FP_RenderConfig &cfg)
{
   string id = "";
   if(cfg.use_canonical_object_names && StringLen(h.visual_id) > 0) id = h.visual_id;
   else if(cfg.use_canonical_object_names && StringLen(h.structural_id) > 0) id = h.structural_id;
   else id = "H" + IntegerToString(h.branch_id);
   return cfg.prefix + "HK_" + FP_RenderSafeId(id, 64) + "_";
}

bool FP_RenderEventHasDrawableGeometry(const FP_FlagEvent &e)
{
   if(e.render_kind == FP_RENDER_NONE) return false;
   if(e.render_kind == FP_RENDER_PROBABLE)
      return (e.has_origin && e.has_leg1 && e.origin.id >= 0 && e.leg1.id >= 0);
   if(e.render_kind == FP_RENDER_FLAG_BODY)
      return (e.has_origin && e.has_leg1 && e.origin.id >= 0 && e.leg1.id >= 0);
   if(e.render_kind == FP_RENDER_LABEL_ONLY)
      return (e.has_leg2 || e.has_leg1 || e.has_origin);
   return true;
}

bool FP_RenderHookHasDrawableGeometry(const FP_HookBranch &h)
{
   if(!h.is_nd) return false;
   if(h.resolve_node.id < 0) return false;
   if(h.extreme_node.id < 0) return false;
   if(!h.has_cycle_start && h.start_node.id < 0) return false;
   return true;
}

bool FP_RenderStatusAllowed(const int status, const FP_RenderConfig &cfg)
{
   if(status == FP_STATUS_INVALIDATED) return cfg.draw_invalidated;
   if(status == FP_STATUS_CONFIRMED) return cfg.draw_confirmed;
   if(status == FP_STATUS_COMPLETED || status == FP_STATUS_LOCKED) return cfg.draw_locked;
   if(status == FP_STATUS_SEED || status == FP_STATUS_LIVE_LEG || status == FP_STATUS_LIVE_BODY || status == FP_STATUS_POST_FLAG || status == FP_STATUS_QUALIFIED) return cfg.draw_candidates;
   return cfg.draw_candidates;
}

bool FP_RenderLevelAllowed(const int level, const FP_RenderConfig &cfg)
{
   if(level == FP_LEVEL_F1) return cfg.draw_f1;
   if(level == FP_LEVEL_F2) return cfg.draw_f2;
   if(level == FP_LEVEL_F3) return cfg.draw_f3;
   return false;
}

bool FP_RenderDirectionAllowed(const int direction, const FP_RenderConfig &cfg)
{
   if(direction == FP_DIR_BULLISH) return cfg.draw_bull;
   if(direction == FP_DIR_BEARISH) return cfg.draw_bear;
   return false;
}

bool FP_ShouldRenderEvent(const FP_FlagEvent &e, const FP_RenderConfig &cfg, FP_RenderReport &report)
{
   if(cfg.strict_visibility && !e.visible_main)
   {
      report.event_filter_visibility++;
      return false;
   }
   if(!FP_RenderLevelAllowed(e.level, cfg))
   {
      report.event_filter_level++;
      return false;
   }
   if(!FP_RenderDirectionAllowed(e.direction, cfg))
   {
      report.event_filter_direction++;
      return false;
   }
   if(!FP_RenderStatusAllowed(e.status, cfg))
   {
      report.event_filter_status++;
      return false;
   }
   if(e.render_kind == FP_RENDER_NONE)
   {
      report.event_filter_render_kind++;
      return false;
   }
   if(!FP_RenderEventHasDrawableGeometry(e))
   {
      report.event_filter_malformed++;
      return false;
   }
   return true;
}

bool FP_ShouldRenderHook(const FP_HookBranch &h, const bool seeds_visible_f1, const FP_RenderConfig &cfg, FP_RenderReport &report)
{
   if(!cfg.draw_hooks) return false;
   if(cfg.strict_visibility && !h.visible_main)
   {
      report.hook_filter_visibility++;
      return false;
   }
   if(!h.is_nd)
   {
      report.hook_filter_nd++;
      return false;
   }
   if(cfg.draw_only_flag_seed_hooks && !seeds_visible_f1)
   {
      report.hook_filter_seed++;
      return false;
   }
   if(!FP_RenderHookHasDrawableGeometry(h))
   {
      report.hook_filter_malformed++;
      return false;
   }
   return true;
}

void FP_RenderAddSample(FP_RenderReport &report, const string sample, const int sample_limit)
{
   if(sample_limit <= 0) return;
   int existing = 0;
   for(int i=0; i<StringLen(report.samples); i++)
      if(StringGetCharacter(report.samples, i) == '|') existing++;
   if(existing >= sample_limit) return;
   if(StringLen(report.samples) > 0) report.samples += "|";
   report.samples += sample;
}

#endif // __FP_RENDER_RULES_MQH__
