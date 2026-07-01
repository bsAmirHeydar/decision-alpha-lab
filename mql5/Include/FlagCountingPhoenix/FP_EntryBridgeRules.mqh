#ifndef __FP_ENTRY_BRIDGE_RULES_MQH__
#define __FP_ENTRY_BRIDGE_RULES_MQH__
#property strict

#include "FP_EntryBridgeTypes.mqh"

string FP_L20Bool(const bool v){ return (v ? "true" : "false"); }
string FP_L20Time(const datetime t){ if(t <= 0) return ""; return TimeToString(t, TIME_DATE|TIME_SECONDS); }
string FP_L20SafeCsv(string v){ StringReplace(v, "\"", "\"\""); return "\"" + v + "\""; }
string FP_L20TfLabel(const ENUM_TIMEFRAMES tf){ return EnumToString(tf); }
double FP_L20AbsDouble(const double value){ if(value < 0.0) return -value; return value; }

string FP_L20DirectionLabel(const int direction)
{
   if(direction == FP_DIR_BULLISH) return "DIRECTION_BULLISH";
   if(direction == FP_DIR_BEARISH) return "DIRECTION_BEARISH";
   return "DIRECTION_NONE";
}

string FP_L20LevelLabel(const int level)
{
   if(level == FP_LEVEL_F1) return "F1";
   if(level == FP_LEVEL_F2) return "F2";
   if(level == FP_LEVEL_F3) return "F3";
   if(level == FP_LEVEL_ND) return "ND";
   return "LEVEL_UNKNOWN";
}

string FP_L20NodeAnchorId(const FP_Node &node)
{
   if(StringLen(node.structural_id) > 0) return node.structural_id;
   if(StringLen(node.visual_id) > 0) return node.visual_id;
   return "NODE_" + IntegerToString(node.id);
}

bool FP_L20NodeUsable(const FP_Node &node)
{
   if(node.id < 0) return false;
   if(node.price <= 0.0) return false;
   return true;
}

void FP_L20SetAnchor(const FP_Node &node,const string kind,string &anchor_kind,
                     datetime &anchor_time,double &anchor_price,int &anchor_node_id,string &anchor_id)
{
   anchor_kind = kind;
   anchor_time = node.time_anchor;
   anchor_price = node.price;
   anchor_node_id = node.id;
   anchor_id = FP_L20NodeAnchorId(node);
}

bool FP_L20SelectLatestVisibleEvent(const FP_FlagEvent &events[], FP_FlagEvent &selected)
{
   bool found = false;
   int best_index = -1;
   for(int i=0; i<ArraySize(events); i++)
   {
      if(!events[i].visible_main) continue;
      if(events[i].direction == FP_DIR_NONE) continue;
      best_index = i;
      found = true;
   }
   if(found && best_index >= 0) selected = events[best_index];
   return found;
}

bool FP_L20SelectLatestVisibleHook(const FP_HookBranch &hooks[], FP_HookBranch &selected)
{
   bool found = false;
   int best_index = -1;
   for(int i=0; i<ArraySize(hooks); i++)
   {
      if(!hooks[i].visible_main) continue;
      if(hooks[i].direction == FP_DIR_NONE) continue;
      best_index = i;
      found = true;
   }
   if(found && best_index >= 0) selected = hooks[best_index];
   return found;
}

string FP_L20EventSourceId(const FP_FlagEvent &event)
{
   if(StringLen(event.canonical_id) > 0) return event.canonical_id;
   if(StringLen(event.visual_id) > 0) return event.visual_id;
   if(StringLen(event.structural_id) > 0) return event.structural_id;
   return "EVENT_" + IntegerToString(event.event_id);
}

string FP_L20HookSourceId(const FP_HookBranch &hook)
{
   if(StringLen(hook.visual_id) > 0) return hook.visual_id;
   if(StringLen(hook.structural_id) > 0) return hook.structural_id;
   return "HOOK_" + IntegerToString(hook.branch_id);
}

bool FP_L20FillFromEvent(const FP_FlagEvent &event, FP_Level20EntryBridgeRow &row)
{
   row.source_kind = "EVENT";
   row.source_id = FP_L20EventSourceId(event);
   row.source_level = event.level;
   row.source_L = event.scale_L;
   row.direction = event.direction;
   row.y_state_label = "Y_STATE_VISIBLE_" + FP_L20LevelLabel(event.level);
   row.y_context_label = FP_L20DirectionLabel(event.direction) + "_EVENT_CONTEXT";

   if(event.has_waist && FP_L20NodeUsable(event.waist))
      FP_L20SetAnchor(event.waist, "ENTRY_ANCHOR_EVENT_WAIST", row.entry_anchor_kind, row.entry_anchor_time, row.entry_anchor_price, row.entry_anchor_node_id, row.entry_anchor_id);
   else if(event.has_leg2 && FP_L20NodeUsable(event.leg2))
      FP_L20SetAnchor(event.leg2, "ENTRY_ANCHOR_EVENT_LEG2", row.entry_anchor_kind, row.entry_anchor_time, row.entry_anchor_price, row.entry_anchor_node_id, row.entry_anchor_id);
   else if(event.has_origin && FP_L20NodeUsable(event.origin))
      FP_L20SetAnchor(event.origin, "ENTRY_ANCHOR_EVENT_ORIGIN_FALLBACK", row.entry_anchor_kind, row.entry_anchor_time, row.entry_anchor_price, row.entry_anchor_node_id, row.entry_anchor_id);

   if(event.has_invalid && FP_L20NodeUsable(event.invalid))
      FP_L20SetAnchor(event.invalid, "INVALIDATION_ANCHOR_EVENT_INVALID", row.invalidation_anchor_kind, row.invalidation_anchor_time, row.invalidation_anchor_price, row.invalidation_anchor_node_id, row.invalidation_anchor_id);
   else if(event.has_origin && FP_L20NodeUsable(event.origin))
      FP_L20SetAnchor(event.origin, "INVALIDATION_ANCHOR_EVENT_ORIGIN_FALLBACK", row.invalidation_anchor_kind, row.invalidation_anchor_time, row.invalidation_anchor_price, row.invalidation_anchor_node_id, row.invalidation_anchor_id);

   if(event.has_confirm && FP_L20NodeUsable(event.confirm))
      FP_L20SetAnchor(event.confirm, "DESTINATION_ANCHOR_EVENT_CONFIRM", row.destination_anchor_kind, row.destination_anchor_time, row.destination_anchor_price, row.destination_anchor_node_id, row.destination_anchor_id);
   else if(event.has_leg1 && FP_L20NodeUsable(event.leg1))
      FP_L20SetAnchor(event.leg1, "DESTINATION_ANCHOR_EVENT_LEG1_FALLBACK", row.destination_anchor_kind, row.destination_anchor_time, row.destination_anchor_price, row.destination_anchor_node_id, row.destination_anchor_id);
   else if(event.has_extension && FP_L20NodeUsable(event.extension_end))
      FP_L20SetAnchor(event.extension_end, "DESTINATION_ANCHOR_EVENT_EXTENSION_FALLBACK", row.destination_anchor_kind, row.destination_anchor_time, row.destination_anchor_price, row.destination_anchor_node_id, row.destination_anchor_id);

   return true;
}

bool FP_L20FillFromHook(const FP_HookBranch &hook, FP_Level20EntryBridgeRow &row)
{
   row.source_kind = "HOOK";
   row.source_id = FP_L20HookSourceId(hook);
   row.source_level = FP_LEVEL_ND;
   row.source_L = hook.scale_L;
   row.direction = hook.direction;
   row.y_state_label = (hook.is_nd ? "Y_STATE_VISIBLE_ND_HOOK" : "Y_STATE_VISIBLE_HOOK");
   row.y_context_label = FP_L20DirectionLabel(hook.direction) + "_HOOK_CONTEXT";

   if(FP_L20NodeUsable(hook.extreme_node))
      FP_L20SetAnchor(hook.extreme_node, "ENTRY_ANCHOR_HOOK_EXTREME", row.entry_anchor_kind, row.entry_anchor_time, row.entry_anchor_price, row.entry_anchor_node_id, row.entry_anchor_id);
   if(FP_L20NodeUsable(hook.start_node))
      FP_L20SetAnchor(hook.start_node, "INVALIDATION_ANCHOR_HOOK_START", row.invalidation_anchor_kind, row.invalidation_anchor_time, row.invalidation_anchor_price, row.invalidation_anchor_node_id, row.invalidation_anchor_id);
   else if(hook.has_cycle_start && FP_L20NodeUsable(hook.cycle_start_node))
      FP_L20SetAnchor(hook.cycle_start_node, "INVALIDATION_ANCHOR_HOOK_CYCLE_START", row.invalidation_anchor_kind, row.invalidation_anchor_time, row.invalidation_anchor_price, row.invalidation_anchor_node_id, row.invalidation_anchor_id);
   if(FP_L20NodeUsable(hook.resolve_node))
      FP_L20SetAnchor(hook.resolve_node, "DESTINATION_ANCHOR_HOOK_RESOLVE", row.destination_anchor_kind, row.destination_anchor_time, row.destination_anchor_price, row.destination_anchor_node_id, row.destination_anchor_id);

   return true;
}

void FP_L20FinalizeReadiness(const FP_Level20EntryBridgeConfig &cfg, FP_Level20EntryBridgeRow &row)
{
   row.risk_distance = FP_L20AbsDouble(row.entry_anchor_price - row.invalidation_anchor_price);
   row.reward_distance = FP_L20AbsDouble(row.destination_anchor_price - row.entry_anchor_price);
   row.rr_like = (row.risk_distance > 0.0 ? row.reward_distance / row.risk_distance : 0.0);
   row.min_rr_required = cfg.min_rr;

   if(!row.timebase_ok){ row.readiness_status="ENTRY_BRIDGE_BLOCKED_TIMEBASE"; row.block_reason="timebase_not_ok"; }
   else if(!row.render_health_ok){ row.readiness_status="ENTRY_BRIDGE_BLOCKED_RENDER_HEALTH"; row.block_reason="render_report_not_ok"; }
   else if(!row.validation_health_ok){ row.readiness_status="ENTRY_BRIDGE_BLOCKED_VALIDATION_HEALTH"; row.block_reason="validation_report_not_ok"; }
   else if(row.source_kind=="NONE"){ row.readiness_status="ENTRY_BRIDGE_BLOCKED_NO_SOURCE"; row.block_reason="no_visible_event_or_hook_source"; }
   else if(row.direction==FP_DIR_NONE){ row.readiness_status="ENTRY_BRIDGE_BLOCKED_NO_DIRECTION"; row.block_reason="direction_missing"; }
   else if(row.entry_anchor_price<=0.0){ row.readiness_status="ENTRY_BRIDGE_BLOCKED_NO_ENTRY_ANCHOR"; row.block_reason="entry_anchor_missing"; }
   else if(row.invalidation_anchor_price<=0.0){ row.readiness_status="ENTRY_BRIDGE_BLOCKED_NO_INVALIDATION_ANCHOR"; row.block_reason="invalidation_anchor_missing"; }
   else if(row.destination_anchor_price<=0.0){ row.readiness_status="ENTRY_BRIDGE_BLOCKED_NO_DESTINATION_ANCHOR"; row.block_reason="destination_anchor_missing"; }
   else if(row.risk_distance<=0.0){ row.readiness_status="ENTRY_BRIDGE_BLOCKED_ZERO_RISK_DISTANCE"; row.block_reason="risk_distance_zero"; }
   else if(row.reward_distance<=0.0){ row.readiness_status="ENTRY_BRIDGE_BLOCKED_ZERO_REWARD_DISTANCE"; row.block_reason="reward_distance_zero"; }
   else if(row.rr_like<cfg.min_rr){ row.readiness_status="ENTRY_BRIDGE_BLOCKED_BAD_RR"; row.block_reason="rr_like_below_required_minimum"; }
   else { row.ready=true; row.readiness_status="ENTRY_RESEARCH_READY_NO_ORDER"; row.block_reason="none"; }

   row.bridge_status = row.readiness_status;
   row.bridge_key = row.symbol+"|TF="+row.period_label+"|SRC="+row.source_kind+"|ID="+row.source_id+"|DIR="+FP_L20DirectionLabel(row.direction)+"|READY="+FP_L20Bool(row.ready)+"|RR="+DoubleToString(row.rr_like,2)+"|EXEC=NO";
}

void FP_L20BuildEntryBridgeRow(const string symbol,const ENUM_TIMEFRAMES period,const MqlRates &rates[],
                               const int bars,const FP_FlagEvent &events[],const FP_HookBranch &hooks[],
                               const FP_TimebaseReport &timebase_report,const FP_RenderReport &render_report,
                               const FP_ValidationReport &validation_report,const FP_Level20EntryBridgeConfig &cfg,
                               FP_Level20EntryBridgeRow &row)
{
   FP_ResetLevel20EntryBridgeRow(row);
   row.generated_at = TimeCurrent();
   row.symbol = symbol;
   row.period = period;
   row.period_label = FP_L20TfLabel(period);
   row.attempted = cfg.enabled;
   row.timebase_ok = timebase_report.ok;
   row.render_health_ok = (!render_report.attempted || render_report.ok);
   row.validation_health_ok = (!validation_report.attempted || validation_report.ok);
   if(bars > 0) row.current_close = rates[bars-1].close;

   FP_FlagEvent selected_event;
   FP_HookBranch selected_hook;
   bool has_event = false;
   bool has_hook = false;

   if(cfg.prefer_latest_visible_event) has_event = FP_L20SelectLatestVisibleEvent(events, selected_event);
   if(!has_event && cfg.allow_hook_fallback) has_hook = FP_L20SelectLatestVisibleHook(hooks, selected_hook);

   if(has_event) FP_L20FillFromEvent(selected_event, row);
   else if(has_hook) FP_L20FillFromHook(selected_hook, row);

   FP_L20FinalizeReadiness(cfg, row);
}

#endif // __FP_ENTRY_BRIDGE_RULES_MQH__
