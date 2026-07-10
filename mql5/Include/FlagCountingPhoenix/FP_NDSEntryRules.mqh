#ifndef __FP_NDS_ENTRY_RULES_MQH__
#define __FP_NDS_ENTRY_RULES_MQH__
#property strict

#include "FP_NDSEntryTypes.mqh"
#include "FP_HookPhase02Rules.mqh"

string FP_NDSEntryBool(const bool v){ return (v ? "true" : "false"); }
string FP_NDSEntryTime(const datetime t){ if(t <= 0) return ""; return TimeToString(t, TIME_DATE|TIME_SECONDS); }
string FP_NDSEntryTf(const ENUM_TIMEFRAMES tf){ return EnumToString(tf); }
double FP_NDSEntryAbs(const double v){ return (v < 0.0 ? -v : v); }

string FP_NDSEntryProfileName(const FP_NDSEntryContractProfile p)
{
   if(p == FP_NDS_ENTRY_PROFILE_PRE_CANON_BLOCKED) return "PRE_CANON_BLOCKED";
   if(p == FP_NDS_ENTRY_PROFILE_DIAGNOSTIC_MANUAL_GEOMETRY) return "DIAGNOSTIC_MANUAL_GEOMETRY";
   if(p == FP_NDS_ENTRY_PROFILE_CANONICAL_ZONE_ADAPTER) return "CANONICAL_ZONE_ADAPTER";
   return "UNKNOWN_PROFILE";
}

string FP_NDSTradeDirectionPolicyName(const FP_NDSTradeDirectionPolicy p)
{
   if(p == FP_NDS_TRADE_DIRECTION_UNRESOLVED) return "UNRESOLVED";
   if(p == FP_NDS_TRADE_DIRECTION_FOLLOW_HOOK) return "FOLLOW_HOOK";
   if(p == FP_NDS_TRADE_DIRECTION_REVERSE_HOOK) return "REVERSE_HOOK";
   return "UNKNOWN_DIRECTION_POLICY";
}

string FP_NDSEntryOrderModelName(const FP_NDSEntryOrderModel m)
{
   if(m == FP_NDS_ORDER_MODEL_UNRESOLVED) return "UNRESOLVED";
   if(m == FP_NDS_ORDER_MODEL_LIMIT_FIRST_EDGE) return "LIMIT_FIRST_EDGE";
   if(m == FP_NDS_ORDER_MODEL_LIMIT_MID_ZONE) return "LIMIT_MID_ZONE";
   if(m == FP_NDS_ORDER_MODEL_LIMIT_NEAR_DEATH) return "LIMIT_NEAR_DEATH";
   if(m == FP_NDS_ORDER_MODEL_MARKET_AFTER_CONFIRMATION) return "MARKET_AFTER_CONFIRMATION";
   if(m == FP_NDS_ORDER_MODEL_LADDER_LIMIT) return "LADDER_LIMIT";
   return "UNKNOWN_ORDER_MODEL";
}

string FP_NDSStopModelName(const FP_NDSStopModel m)
{
   if(m == FP_NDS_STOP_MODEL_UNRESOLVED) return "UNRESOLVED";
   if(m == FP_NDS_STOP_MODEL_BEYOND_ZONE) return "BEYOND_ZONE";
   if(m == FP_NDS_STOP_MODEL_BEYOND_ORIGIN) return "BEYOND_ORIGIN";
   if(m == FP_NDS_STOP_MODEL_BEYOND_DEATH_BOUNDARY) return "BEYOND_DEATH_BOUNDARY";
   if(m == FP_NDS_STOP_MODEL_MANUAL_DIAGNOSTIC) return "MANUAL_DIAGNOSTIC";
   return "UNKNOWN_STOP_MODEL";
}

string FP_NDSTargetModelName(const FP_NDSTargetModel m)
{
   if(m == FP_NDS_TARGET_MODEL_UNRESOLVED) return "UNRESOLVED";
   if(m == FP_NDS_TARGET_MODEL_CROWN) return "CROWN";
   if(m == FP_NDS_TARGET_MODEL_ORIGIN) return "ORIGIN";
   if(m == FP_NDS_TARGET_MODEL_NEXT_STRUCTURE) return "NEXT_STRUCTURE";
   if(m == FP_NDS_TARGET_MODEL_FIXED_R) return "FIXED_R";
   if(m == FP_NDS_TARGET_MODEL_MANUAL_DIAGNOSTIC) return "MANUAL_DIAGNOSTIC";
   return "UNKNOWN_TARGET_MODEL";
}

string FP_NDSEntryStageName(const FP_NDSEntryPipelineStage s)
{
   if(s == FP_NDS_ENTRY_STAGE_RESET) return "RESET";
   if(s == FP_NDS_ENTRY_STAGE_STRUCTURE_CAPTURED) return "STRUCTURE_CAPTURED";
   if(s == FP_NDS_ENTRY_STAGE_SETUP_CANDIDATE) return "SETUP_CANDIDATE";
   if(s == FP_NDS_ENTRY_STAGE_TRADE_PLAN_READY) return "TRADE_PLAN_READY";
   if(s == FP_NDS_ENTRY_STAGE_COMMAND_PREVIEW_READY) return "COMMAND_PREVIEW_READY";
   if(s == FP_NDS_ENTRY_STAGE_BLOCKED) return "BLOCKED";
   return "UNKNOWN_STAGE";
}

string FP_NDSHookDirectionLabel(const int hook_direction)
{
   if(hook_direction > 0) return "HOOK_POSITIVE";
   if(hook_direction < 0) return "HOOK_NEGATIVE";
   return "HOOK_DIRECTION_NONE";
}

string FP_NDSTradeDirectionLabel(const int direction)
{
   if(direction == FP_DIR_BULLISH) return "TRADE_BULLISH";
   if(direction == FP_DIR_BEARISH) return "TRADE_BEARISH";
   return "TRADE_DIRECTION_NONE";
}

int FP_NDSMapTradeDirection(const int hook_direction,
                            const FP_NDSTradeDirectionPolicy policy)
{
   if(policy == FP_NDS_TRADE_DIRECTION_UNRESOLVED)
      return FP_DIR_NONE;

   int base = FP_DIR_NONE;
   if(hook_direction > 0) base = FP_DIR_BULLISH;
   if(hook_direction < 0) base = FP_DIR_BEARISH;

   if(policy == FP_NDS_TRADE_DIRECTION_FOLLOW_HOOK)
      return base;
   if(policy == FP_NDS_TRADE_DIRECTION_REVERSE_HOOK)
      return -base;
   return FP_DIR_NONE;
}

bool FP_NDSDirectionalGeometryOk(const int direction,
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

bool FP_NDSSequenceBaseEligible(const FP_HookPhase02Sequence &seq,
                                const FP_NDSEntryConfig &cfg)
{
   if(cfg.require_valid_hook_family && !seq.valid_hook_family)
      return false;
   if(!seq.valid)
      return false;
   if(seq.hook_failed)
      return false;
   if(cfg.require_closed_hook && !FP_HookP02SequenceCycleClosed(seq))
      return false;
   return true;
}

datetime FP_NDSSequenceDecisionTime(const FP_HookPhase02Sequence &seq)
{
   if(seq.resolve_time > 0) return seq.resolve_time;
   if(seq.last_x_time > 0) return seq.last_x_time;
   return seq.origin_time;
}

bool FP_NDSSelectLatestEligibleSequence(const FP_HookPhase02Sequence &sequences[],
                                        const FP_NDSEntryConfig &cfg,
                                        FP_HookPhase02Sequence &selected)
{
   bool found = false;
   datetime best_time = 0;
   int best_sequence_id = -1;

   for(int i=0; i<ArraySize(sequences); i++)
   {
      if(!FP_NDSSequenceBaseEligible(sequences[i], cfg))
         continue;

      datetime t = FP_NDSSequenceDecisionTime(sequences[i]);
      if(!found || t > best_time || (t == best_time && sequences[i].sequence_id > best_sequence_id))
      {
         selected = sequences[i];
         best_time = t;
         best_sequence_id = sequences[i].sequence_id;
         found = true;
      }
   }

   return found;
}

void FP_NDSFillStructureRow(const FP_HookPhase02Sequence &seq,
                            const FP_NDSEntryConfig &cfg,
                            FP_NDSStructureRow &row)
{
   FP_ResetNDSStructureRow(row);
   row.available = true;
   row.sequence_id = seq.sequence_id;
   row.scale_l = seq.scale_l;
   row.hook_direction = (int)seq.direction;
   row.hook_direction_label = FP_NDSHookDirectionLabel(row.hook_direction);
   row.validity_family = seq.hook_validity_family;
   row.post_f3_subfamily = seq.post_f3_subfamily;
   row.valid_after_hook = seq.valid_after_hook;
   row.valid_after_opposing_f3 = seq.valid_after_opposing_f3;
   row.valid_hook_family = seq.valid_hook_family;
   row.sequence_valid = seq.valid;
   row.hook_failed = seq.hook_failed;
   row.hook_closed = FP_HookP02SequenceCycleClosed(seq);
   row.near_death_confirmed = seq.near_death_confirmed;
   row.resolve_confirmed = seq.resolve_confirmed;

   row.origin_bar_index = seq.origin_bar_index;
   row.origin_time = seq.origin_time;
   row.origin_price = seq.origin_price;
   row.crown_node_id = seq.cycle_crown_node_id;
   row.crown_time = seq.cycle_crown_time;
   row.crown_price = seq.cycle_crown_price;
   row.terminal_node_id = seq.resolve_node_id;
   row.terminal_time = seq.resolve_time;
   row.terminal_price = seq.resolve_price;
   row.death_boundary_price = seq.death_boundary_price;
   row.completion_pct = seq.post_f3_completion_pct;

   row.parent_hook_sequence_id = seq.previous_hook_sequence_id;
   row.opposing_f3_event_id = seq.opposing_f3_event_id;
   row.opposing_f3_terminal_bar_index = seq.opposing_f3_terminal_bar_index;
   row.opposing_f3_terminal_time = seq.opposing_f3_terminal_time;
   row.opposing_f3_terminal_price = seq.opposing_f3_terminal_price;

   row.eligible = FP_NDSSequenceBaseEligible(seq, cfg);
   row.status = (row.eligible ? "NDS_STRUCTURE_ELIGIBLE" : "NDS_STRUCTURE_NOT_ELIGIBLE");
   row.block_reason = (row.eligible ? "none" : "hook_validity_or_closure_gate_failed");
   row.structure_key = "SEQ=" + IntegerToString(row.sequence_id);
   row.structure_key += "|L=" + IntegerToString(row.scale_l);
   row.structure_key += "|DIR=" + row.hook_direction_label;
   row.structure_key += "|FAMILY=" + row.validity_family;
   row.structure_key += "|SUB=" + row.post_f3_subfamily;
   row.structure_key += "|CLOSED=" + FP_NDSEntryBool(row.hook_closed);
}

// Adapter seam for the final Zone Canon.  It intentionally returns false until
// the questionnaire locks source points, boundaries, lifecycle and entry/stop/
// target semantics.  Future code changes should be localized to this function.
bool FP_NDSBuildCanonicalZoneAdapter(const FP_NDSStructureRow &structure,
                                     const FP_NDSEntryConfig &cfg,
                                     FP_NDSZoneRow &zone)
{
   FP_ResetNDSZoneRow(zone);
   zone.source_mode = "CANONICAL_ZONE_ADAPTER";
   zone.status = "NDS_ZONE_CANON_ADAPTER_PENDING";
   zone.block_reason = "zone_canon_rules_not_implemented";
   zone.zone_id = "ZONE_PENDING_SEQ_" + IntegerToString(structure.sequence_id);
   zone.zone_key = zone.zone_id + "|CANONICAL=false";
   return false;
}

bool FP_NDSBuildDiagnosticManualZone(const FP_NDSStructureRow &structure,
                                     const FP_NDSEntryConfig &cfg,
                                     const int trade_direction,
                                     FP_NDSZoneRow &zone)
{
   FP_ResetNDSZoneRow(zone);
   zone.source_mode = "DIAGNOSTIC_MANUAL_GEOMETRY";
   zone.canonical = false;
   zone.zone_id = "DZ_SEQ_" + IntegerToString(structure.sequence_id);
   zone.lower_price = cfg.manual_zone_lower;
   zone.upper_price = cfg.manual_zone_upper;
   zone.planned_entry_price = cfg.manual_entry_price;
   zone.planned_stop_price = cfg.manual_stop_price;
   zone.planned_target_price = cfg.manual_target_price;

   zone.boundaries_valid = (zone.lower_price > 0.0 && zone.upper_price > zone.lower_price);
   zone.width = (zone.boundaries_valid ? zone.upper_price - zone.lower_price : 0.0);
   zone.entry_edge_price = zone.planned_entry_price;
   zone.death_edge_price = zone.planned_stop_price;
   zone.directional_geometry_valid = FP_NDSDirectionalGeometryOk(trade_direction,
                                                                  zone.planned_entry_price,
                                                                  zone.planned_stop_price,
                                                                  zone.planned_target_price);

   if(!zone.boundaries_valid)
   {
      zone.status = "NDS_DIAGNOSTIC_ZONE_BLOCKED_BOUNDARIES";
      zone.block_reason = "manual_zone_requires_positive_lower_and_upper_above_lower";
   }
   else if(zone.planned_entry_price <= 0.0 || zone.planned_stop_price <= 0.0 || zone.planned_target_price <= 0.0)
   {
      zone.status = "NDS_DIAGNOSTIC_ZONE_BLOCKED_MISSING_PLAN_PRICES";
      zone.block_reason = "manual_entry_stop_target_required";
   }
   else if(zone.planned_entry_price < zone.lower_price || zone.planned_entry_price > zone.upper_price)
   {
      zone.status = "NDS_DIAGNOSTIC_ZONE_BLOCKED_ENTRY_OUTSIDE_ZONE";
      zone.block_reason = "manual_entry_must_be_inside_manual_zone";
   }
   else if(!zone.directional_geometry_valid)
   {
      zone.status = "NDS_DIAGNOSTIC_ZONE_BLOCKED_DIRECTIONAL_GEOMETRY";
      zone.block_reason = "manual_prices_do_not_match_trade_direction";
   }
   else
   {
      zone.available = true;
      zone.status = "NDS_DIAGNOSTIC_ZONE_READY_NON_CANONICAL";
      zone.block_reason = "none";
   }

   zone.zone_key = zone.zone_id;
   zone.zone_key += "|LOW=" + DoubleToString(zone.lower_price, _Digits);
   zone.zone_key += "|HIGH=" + DoubleToString(zone.upper_price, _Digits);
   zone.zone_key += "|CANONICAL=false";
   return zone.available;
}

void FP_NDSBuildZone(const FP_NDSStructureRow &structure,
                     const FP_NDSEntryConfig &cfg,
                     const int trade_direction,
                     FP_NDSZoneRow &zone)
{
   FP_ResetNDSZoneRow(zone);

   if(cfg.contract_profile == FP_NDS_ENTRY_PROFILE_PRE_CANON_BLOCKED)
   {
      zone.status = "NDS_ZONE_BLOCKED_PRE_CANON_PROFILE";
      zone.block_reason = "select_diagnostic_or_canonical_profile_after_explicit_review";
      return;
   }

   if(cfg.contract_profile == FP_NDS_ENTRY_PROFILE_DIAGNOSTIC_MANUAL_GEOMETRY)
   {
      FP_NDSBuildDiagnosticManualZone(structure, cfg, trade_direction, zone);
      return;
   }

   if(cfg.contract_profile == FP_NDS_ENTRY_PROFILE_CANONICAL_ZONE_ADAPTER)
   {
      if(cfg.require_zone_canon_locked && !cfg.zone_canon_locked)
      {
         zone.status = "NDS_ZONE_BLOCKED_CANON_NOT_LOCKED";
         zone.block_reason = "zone_canon_locked_false";
         return;
      }
      FP_NDSBuildCanonicalZoneAdapter(structure, cfg, zone);
      return;
   }

   zone.status = "NDS_ZONE_BLOCKED_UNKNOWN_PROFILE";
   zone.block_reason = "unknown_contract_profile";
}

void FP_NDSBuildSetup(const FP_NDSStructureRow &structure,
                      const FP_NDSZoneRow &zone,
                      const FP_NDSEntryConfig &cfg,
                      const int current_bar_index,
                      const datetime current_time,
                      FP_NDSSetupRow &setup)
{
   FP_ResetNDSSetupRow(setup);
   setup.source_structure_key = structure.structure_key;
   setup.source_zone_key = zone.zone_key;
   setup.trade_direction = FP_NDSMapTradeDirection(structure.hook_direction, cfg.trade_direction_policy);
   setup.trade_direction_label = FP_NDSTradeDirectionLabel(setup.trade_direction);
   setup.order_model = cfg.order_model;
   setup.stop_model = cfg.stop_model;
   setup.target_model = cfg.target_model;
   setup.created_bar_index = current_bar_index;
   setup.created_time = current_time;
   setup.expiry_bars = cfg.expiry_bars;
   setup.expires_bar_index = (cfg.expiry_bars > 0 ? current_bar_index + cfg.expiry_bars : -1);
   setup.setup_family = structure.validity_family;
   setup.setup_id = "NDS_SETUP_SEQ_" + IntegerToString(structure.sequence_id);
   setup.candidate_created = structure.eligible;

   if(!structure.eligible)
   {
      setup.status = "NDS_SETUP_BLOCKED_STRUCTURE";
      setup.block_reason = structure.block_reason;
   }
   else if(setup.trade_direction == FP_DIR_NONE)
   {
      setup.status = "NDS_SETUP_BLOCKED_DIRECTION_POLICY";
      setup.block_reason = "trade_direction_policy_unresolved";
   }
   else if(!zone.available)
   {
      setup.status = "NDS_SETUP_BLOCKED_ZONE";
      setup.block_reason = zone.status + ":" + zone.block_reason;
   }
   else if(cfg.order_model == FP_NDS_ORDER_MODEL_UNRESOLVED)
   {
      setup.status = "NDS_SETUP_BLOCKED_ORDER_MODEL";
      setup.block_reason = "order_model_unresolved";
   }
   else if(cfg.stop_model == FP_NDS_STOP_MODEL_UNRESOLVED)
   {
      setup.status = "NDS_SETUP_BLOCKED_STOP_MODEL";
      setup.block_reason = "stop_model_unresolved";
   }
   else if(cfg.target_model == FP_NDS_TARGET_MODEL_UNRESOLVED)
   {
      setup.status = "NDS_SETUP_BLOCKED_TARGET_MODEL";
      setup.block_reason = "target_model_unresolved";
   }
   else if(cfg.require_trade_contract_locked && !cfg.trade_contract_locked)
   {
      setup.status = "NDS_SETUP_BLOCKED_TRADE_CONTRACT_NOT_LOCKED";
      setup.block_reason = "trade_contract_locked_false";
   }
   else
   {
      setup.ready = true;
      setup.status = (zone.canonical ? "NDS_SETUP_READY_CANONICAL" : "NDS_SETUP_READY_DIAGNOSTIC_NON_CANONICAL");
      setup.block_reason = "none";
   }

   setup.setup_key = setup.setup_id;
   setup.setup_key += "|DIR=" + setup.trade_direction_label;
   setup.setup_key += "|ORDER=" + FP_NDSEntryOrderModelName(setup.order_model);
   setup.setup_key += "|STOP=" + FP_NDSStopModelName(setup.stop_model);
   setup.setup_key += "|TARGET=" + FP_NDSTargetModelName(setup.target_model);
   setup.setup_key += "|READY=" + FP_NDSEntryBool(setup.ready);
}

void FP_NDSBuildTradePlan(const FP_NDSSetupRow &setup,
                          const FP_NDSZoneRow &zone,
                          const FP_NDSEntryConfig &cfg,
                          FP_NDSTradePlanRow &plan)
{
   FP_ResetNDSTradePlanRow(plan);
   plan.source_setup_id = setup.setup_id;
   plan.trade_direction = setup.trade_direction;
   plan.trade_direction_label = setup.trade_direction_label;
   plan.entry_price = zone.planned_entry_price;
   plan.stop_price = zone.planned_stop_price;
   plan.target_price = zone.planned_target_price;
   plan.risk_distance = FP_NDSEntryAbs(plan.entry_price - plan.stop_price);
   plan.reward_distance = FP_NDSEntryAbs(plan.target_price - plan.entry_price);
   plan.rr = (plan.risk_distance > 0.0 ? plan.reward_distance / plan.risk_distance : 0.0);
   plan.min_rr_required = cfg.min_rr;
   plan.requested_risk_fraction = 0.0;
   plan.requested_volume = 0.0;
   plan.plan_id = "NDS_PLAN_" + setup.setup_id;

   if(!setup.ready)
   {
      plan.status = "NDS_TRADE_PLAN_BLOCKED_SETUP";
      plan.block_reason = setup.status + ":" + setup.block_reason;
   }
   else if(plan.entry_price <= 0.0 || plan.stop_price <= 0.0 || plan.target_price <= 0.0)
   {
      plan.status = "NDS_TRADE_PLAN_BLOCKED_MISSING_PRICES";
      plan.block_reason = "entry_stop_target_required";
   }
   else if(!FP_NDSDirectionalGeometryOk(plan.trade_direction, plan.entry_price, plan.stop_price, plan.target_price))
   {
      plan.status = "NDS_TRADE_PLAN_BLOCKED_DIRECTIONAL_GEOMETRY";
      plan.block_reason = "entry_stop_target_direction_mismatch";
   }
   else if(plan.risk_distance <= 0.0)
   {
      plan.status = "NDS_TRADE_PLAN_BLOCKED_ZERO_RISK";
      plan.block_reason = "risk_distance_zero";
   }
   else if(plan.reward_distance <= 0.0)
   {
      plan.status = "NDS_TRADE_PLAN_BLOCKED_ZERO_REWARD";
      plan.block_reason = "reward_distance_zero";
   }
   else if(cfg.min_rr > 0.0 && plan.rr < cfg.min_rr)
   {
      plan.status = "NDS_TRADE_PLAN_BLOCKED_MIN_RR";
      plan.block_reason = "rr_below_configured_minimum";
   }
   else
   {
      plan.ready = true;
      plan.status = (zone.canonical ? "NDS_TRADE_PLAN_READY_CANONICAL_NO_SIZING" : "NDS_TRADE_PLAN_READY_DIAGNOSTIC_NO_SIZING");
      plan.block_reason = "none";
   }

   plan.plan_key = plan.plan_id;
   plan.plan_key += "|DIR=" + plan.trade_direction_label;
   plan.plan_key += "|ENTRY=" + DoubleToString(plan.entry_price, _Digits);
   plan.plan_key += "|STOP=" + DoubleToString(plan.stop_price, _Digits);
   plan.plan_key += "|TARGET=" + DoubleToString(plan.target_price, _Digits);
   plan.plan_key += "|RR=" + DoubleToString(plan.rr, 3);
   plan.plan_key += "|VOLUME=0";
}

string FP_NDSOrderTypePreview(const int direction,
                              const FP_NDSEntryOrderModel model)
{
   string side = (direction == FP_DIR_BULLISH ? "BUY" : (direction == FP_DIR_BEARISH ? "SELL" : "NONE"));
   if(model == FP_NDS_ORDER_MODEL_MARKET_AFTER_CONFIRMATION)
      return side + "_MARKET_PREVIEW";
   if(model == FP_NDS_ORDER_MODEL_LADDER_LIMIT)
      return side + "_LIMIT_LADDER_PREVIEW";
   if(model == FP_NDS_ORDER_MODEL_LIMIT_FIRST_EDGE)
      return side + "_LIMIT_FIRST_EDGE_PREVIEW";
   if(model == FP_NDS_ORDER_MODEL_LIMIT_MID_ZONE)
      return side + "_LIMIT_MID_ZONE_PREVIEW";
   if(model == FP_NDS_ORDER_MODEL_LIMIT_NEAR_DEATH)
      return side + "_LIMIT_NEAR_DEATH_PREVIEW";
   return "ORDER_TYPE_UNRESOLVED";
}

void FP_NDSBuildCommandPreview(const string symbol,
                               const FP_NDSSetupRow &setup,
                               const FP_NDSTradePlanRow &plan,
                               const FP_NDSEntryConfig &cfg,
                               FP_NDSCommandPreviewRow &command)
{
   FP_ResetNDSCommandPreviewRow(command);
   command.source_plan_id = plan.plan_id;
   command.symbol = symbol;
   command.trade_direction = plan.trade_direction;
   command.trade_direction_label = plan.trade_direction_label;
   command.price = plan.entry_price;
   command.sl = plan.stop_price;
   command.tp = plan.target_price;
   command.volume = 0.0;
   command.expiry_bars = setup.expiry_bars;
   command.magic = cfg.preview_magic;
   command.comment = cfg.preview_comment;
   command.order_type_preview = FP_NDSOrderTypePreview(command.trade_direction, setup.order_model);
   command.command_action = "PREVIEW_ONLY_NO_SEND";
   command.command_id = "NDS_CMD_" + plan.plan_id;

   if(!plan.ready)
   {
      command.status = "NDS_COMMAND_BLOCKED_TRADE_PLAN";
      command.block_reason = plan.status + ":" + plan.block_reason;
   }
   else if(!cfg.command_preview_only)
   {
      command.status = "NDS_COMMAND_BLOCKED_PREVIEW_LOCK_DISABLED";
      command.block_reason = "this_module_requires_command_preview_only_true";
   }
   else if(command.order_type_preview == "ORDER_TYPE_UNRESOLVED")
   {
      command.status = "NDS_COMMAND_BLOCKED_ORDER_TYPE";
      command.block_reason = "order_model_unresolved";
   }
   else
   {
      command.built = true;
      command.send_allowed = false;
      command.status = "NDS_COMMAND_PREVIEW_READY_NO_SEND_ZERO_VOLUME";
      command.block_reason = "none";
   }

   command.command_key = command.command_id;
   command.command_key += "|TYPE=" + command.order_type_preview;
   command.command_key += "|PRICE=" + DoubleToString(command.price, _Digits);
   command.command_key += "|SL=" + DoubleToString(command.sl, _Digits);
   command.command_key += "|TP=" + DoubleToString(command.tp, _Digits);
   command.command_key += "|VOLUME=0|SEND_ALLOWED=false";
}

void FP_NDSFinalizePipeline(FP_NDSEntryPipelineRow &row)
{
   // Stage means the highest downstream object that is materially available.
   // A Setup object populated only with an upstream block is not promoted to
   // SETUP_CANDIDATE.  This keeps PRE_CANON output truthful.
   if(row.command.built)
      row.stage = FP_NDS_ENTRY_STAGE_COMMAND_PREVIEW_READY;
   else if(row.plan.ready)
      row.stage = FP_NDS_ENTRY_STAGE_TRADE_PLAN_READY;
   else if(row.setup.candidate_created && row.zone.available)
      row.stage = FP_NDS_ENTRY_STAGE_SETUP_CANDIDATE;
   else if(row.structure.available)
      row.stage = FP_NDS_ENTRY_STAGE_STRUCTURE_CAPTURED;
   else
      row.stage = FP_NDS_ENTRY_STAGE_BLOCKED;

   row.stage_label = FP_NDSEntryStageName(row.stage);

   // Surface the earliest failing authority boundary, not the cascade of
   // downstream objects that were necessarily blocked by it.
   if(!row.structure.available || !row.structure.eligible)
   {
      row.status = row.structure.status;
      row.block_reason = row.structure.block_reason;
   }
   else if(!row.zone.available)
   {
      row.status = row.zone.status;
      row.block_reason = row.zone.block_reason;
   }
   else if(!row.setup.ready)
   {
      row.status = row.setup.status;
      row.block_reason = row.setup.block_reason;
   }
   else if(!row.plan.ready)
   {
      row.status = row.plan.status;
      row.block_reason = row.plan.block_reason;
   }
   else if(!row.command.built)
   {
      row.status = row.command.status;
      row.block_reason = row.command.block_reason;
   }
   else
   {
      row.status = row.command.status;
      row.block_reason = "none";
   }

   row.pipeline_key = row.symbol;
   row.pipeline_key += "|TF=" + row.period_label;
   row.pipeline_key += "|STAGE=" + row.stage_label;
   row.pipeline_key += "|STATUS=" + row.status;
   row.pipeline_key += "|PROFILE=" + row.zone.source_mode;
   row.pipeline_key += "|SEND_ALLOWED=false";
}

void FP_NDSBuildEntryPipelineRow(const string symbol,
                                 const ENUM_TIMEFRAMES period,
                                 const MqlRates &rates[],
                                 const int bars,
                                 const FP_NDSEntryConfig &cfg,
                                 FP_NDSEntryPipelineRow &row)
{
   FP_ResetNDSEntryPipelineRow(row);
   row.generated_at = TimeCurrent();
   row.symbol = symbol;
   row.period = period;
   row.period_label = FP_NDSEntryTf(period);
   row.attempted = cfg.enabled;

   if(!FP_NDSStructureSnapshotMatches(symbol, period))
   {
      row.structure.status = "NDS_STRUCTURE_BLOCKED_NO_MATCHING_SNAPSHOT";
      row.structure.block_reason = "hook_phase02_snapshot_not_ready_for_symbol_timeframe";
      FP_NDSFinalizePipeline(row);
      return;
   }

   FP_HookPhase02Sequence sequences[];
   FP_NDSCopyStructureSnapshot(sequences);
   FP_HookPhase02Sequence selected;
   if(!FP_NDSSelectLatestEligibleSequence(sequences, cfg, selected))
   {
      row.structure.status = "NDS_STRUCTURE_BLOCKED_NO_ELIGIBLE_VALID_HOOK";
      row.structure.block_reason = "no_sequence_passed_validity_closure_failure_gates";
      FP_NDSFinalizePipeline(row);
      return;
   }

   FP_NDSFillStructureRow(selected, cfg, row.structure);
   int trade_direction = FP_NDSMapTradeDirection(row.structure.hook_direction, cfg.trade_direction_policy);
   FP_NDSBuildZone(row.structure, cfg, trade_direction, row.zone);

   int current_bar_index = (bars > 0 ? bars - 1 : -1);
   datetime current_time = (bars > 0 ? rates[bars-1].time : TimeCurrent());
   FP_NDSBuildSetup(row.structure, row.zone, cfg, current_bar_index, current_time, row.setup);
   FP_NDSBuildTradePlan(row.setup, row.zone, cfg, row.plan);
   FP_NDSBuildCommandPreview(symbol, row.setup, row.plan, cfg, row.command);
   FP_NDSFinalizePipeline(row);
}

#endif // __FP_NDS_ENTRY_RULES_MQH__
