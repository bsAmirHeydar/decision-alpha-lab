#ifndef __FP_PAPER_INTENT_RULES_MQH__
#define __FP_PAPER_INTENT_RULES_MQH__
#property strict

#include "FP_PaperIntentTypes.mqh"
#include "FP_EntryBridgeRules.mqh"

string FP_L21Bool(const bool v){ return (v ? "true" : "false"); }
string FP_L21Time(const datetime t){ if(t <= 0) return ""; return TimeToString(t, TIME_DATE|TIME_SECONDS); }
string FP_L21SafeCsv(string v){ StringReplace(v, "\"", "\"\""); return "\"" + v + "\""; }
string FP_L21TfLabel(const ENUM_TIMEFRAMES tf){ return EnumToString(tf); }

string FP_L21DirectionLabel(const int direction)
{
   if(direction == FP_DIR_BULLISH) return "DIRECTION_BULLISH";
   if(direction == FP_DIR_BEARISH) return "DIRECTION_BEARISH";
   return "DIRECTION_NONE";
}

bool FP_L21DirectionalGeometryOk(const int direction,
                                 const double entry_price,
                                 const double stop_price,
                                 const double target_price)
{
   if(direction == FP_DIR_BULLISH)
      return (stop_price < entry_price && target_price > entry_price);
   if(direction == FP_DIR_BEARISH)
      return (stop_price > entry_price && target_price < entry_price);
   return false;
}

string FP_L21GeometryStatus(const int direction,
                            const double entry_price,
                            const double stop_price,
                            const double target_price)
{
   if(direction == FP_DIR_NONE)
      return "GEOMETRY_BLOCKED_NO_DIRECTION";
   if(entry_price <= 0.0)
      return "GEOMETRY_BLOCKED_NO_ENTRY";
   if(stop_price <= 0.0)
      return "GEOMETRY_BLOCKED_NO_STOP";
   if(target_price <= 0.0)
      return "GEOMETRY_BLOCKED_NO_TARGET";

   if(FP_L21DirectionalGeometryOk(direction, entry_price, stop_price, target_price))
      return "GEOMETRY_DIRECTIONAL_OK";

   if(direction == FP_DIR_BULLISH)
      return "GEOMETRY_BLOCKED_BULLISH_REQUIRES_STOP_BELOW_ENTRY_AND_TARGET_ABOVE";
   if(direction == FP_DIR_BEARISH)
      return "GEOMETRY_BLOCKED_BEARISH_REQUIRES_STOP_ABOVE_ENTRY_AND_TARGET_BELOW";

   return "GEOMETRY_BLOCKED_UNKNOWN";
}

string FP_L21BuildIntentId(const FP_Level20EntryBridgeRow &bridge_row)
{
   string id = "PI";
   id += "_" + bridge_row.symbol;
   id += "_" + bridge_row.period_label;
   id += "_" + bridge_row.source_kind;
   id += "_" + bridge_row.source_id;
   id += "_" + FP_L21DirectionLabel(bridge_row.direction);
   id += "_" + DoubleToString(bridge_row.entry_anchor_price, _Digits);
   id += "_" + DoubleToString(bridge_row.invalidation_anchor_price, _Digits);
   id += "_" + DoubleToString(bridge_row.destination_anchor_price, _Digits);
   return id;
}

void FP_L21FillFromEntryBridge(const FP_Level21PaperIntentConfig &cfg,
                               const FP_Level20EntryBridgeRow &bridge_row,
                               FP_Level21PaperIntentRow &row)
{
   FP_ResetLevel21PaperIntentRow(row);

   row.generated_at = TimeCurrent();
   row.symbol = bridge_row.symbol;
   row.period = bridge_row.period;
   row.period_label = bridge_row.period_label;
   row.attempted = cfg.enabled;

   row.source_bridge_key = bridge_row.bridge_key;
   row.source_kind = bridge_row.source_kind;
   row.source_id = bridge_row.source_id;
   row.source_level = bridge_row.source_level;
   row.source_L = bridge_row.source_L;

   row.direction = bridge_row.direction;
   row.direction_label = FP_L21DirectionLabel(bridge_row.direction);

   row.entry_price = bridge_row.entry_anchor_price;
   row.stop_price = bridge_row.invalidation_anchor_price;
   row.target_price = bridge_row.destination_anchor_price;
   row.risk_distance = bridge_row.risk_distance;
   row.reward_distance = bridge_row.reward_distance;
   row.rr_like = bridge_row.rr_like;

   row.entry_anchor_time = bridge_row.entry_anchor_time;
   row.stop_anchor_time = bridge_row.invalidation_anchor_time;
   row.target_anchor_time = bridge_row.destination_anchor_time;

   row.entry_anchor_id = bridge_row.entry_anchor_id;
   row.stop_anchor_id = bridge_row.invalidation_anchor_id;
   row.target_anchor_id = bridge_row.destination_anchor_id;

   row.entry_anchor_kind = bridge_row.entry_anchor_kind;
   row.stop_anchor_kind = bridge_row.invalidation_anchor_kind;
   row.target_anchor_kind = bridge_row.destination_anchor_kind;

   row.expiry_bars = cfg.expiry_bars;
   row.intent_id = FP_L21BuildIntentId(bridge_row);
   row.geometry_status = FP_L21GeometryStatus(row.direction, row.entry_price, row.stop_price, row.target_price);

   if(cfg.require_entry_bridge_ready && !bridge_row.ready)
   {
      row.allowed = false;
      row.intent_status = "PAPER_INTENT_BLOCKED_ENTRY_BRIDGE_NOT_READY";
      row.block_reason = bridge_row.readiness_status + ":" + bridge_row.block_reason;
   }
   else if(row.direction == FP_DIR_NONE)
   {
      row.allowed = false;
      row.intent_status = "PAPER_INTENT_BLOCKED_NO_DIRECTION";
      row.block_reason = "direction_missing";
   }
   else if(row.entry_price <= 0.0)
   {
      row.allowed = false;
      row.intent_status = "PAPER_INTENT_BLOCKED_NO_ENTRY_PRICE";
      row.block_reason = "entry_price_missing";
   }
   else if(row.stop_price <= 0.0)
   {
      row.allowed = false;
      row.intent_status = "PAPER_INTENT_BLOCKED_NO_STOP_PRICE";
      row.block_reason = "stop_price_missing";
   }
   else if(row.target_price <= 0.0)
   {
      row.allowed = false;
      row.intent_status = "PAPER_INTENT_BLOCKED_NO_TARGET_PRICE";
      row.block_reason = "target_price_missing";
   }
   else if(row.risk_distance <= 0.0)
   {
      row.allowed = false;
      row.intent_status = "PAPER_INTENT_BLOCKED_ZERO_RISK";
      row.block_reason = "risk_distance_zero";
   }
   else if(row.reward_distance <= 0.0)
   {
      row.allowed = false;
      row.intent_status = "PAPER_INTENT_BLOCKED_ZERO_REWARD";
      row.block_reason = "reward_distance_zero";
   }
   else if(cfg.require_directional_geometry && !FP_L21DirectionalGeometryOk(row.direction, row.entry_price, row.stop_price, row.target_price))
   {
      row.allowed = false;
      row.intent_status = "PAPER_INTENT_BLOCKED_DIRECTIONAL_GEOMETRY";
      row.block_reason = row.geometry_status;
   }
   else
   {
      row.allowed = true;
      row.intent_status = "PAPER_INTENT_ALLOWED_RESEARCH_ONLY";
      row.block_reason = "none";
   }

   row.lifecycle_seed_status = (row.allowed ? "PAPER_INTENT_SEEDED_NOT_EXECUTED" : "PAPER_INTENT_BLOCKED_NOT_SEEDED");

   row.intent_key = row.symbol;
   row.intent_key += "|TF=" + row.period_label;
   row.intent_key += "|ID=" + row.intent_id;
   row.intent_key += "|DIR=" + row.direction_label;
   row.intent_key += "|ALLOWED=" + FP_L21Bool(row.allowed);
   row.intent_key += "|RR=" + DoubleToString(row.rr_like, 2);
   row.intent_key += "|EXEC=NO";
}

#endif // __FP_PAPER_INTENT_RULES_MQH__
