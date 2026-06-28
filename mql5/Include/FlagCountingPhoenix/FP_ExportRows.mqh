#ifndef __FP_EXPORT_ROWS_MQH__
#define __FP_EXPORT_ROWS_MQH__
#property strict

#include "FP_ExportTypes.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 11.5 CSV row builders
// ============================================================================

string FP_ExportBool(const bool v)
{
   return (v ? "true" : "false");
}

string FP_ExportInt(const int v)
{
   return IntegerToString(v);
}

string FP_ExportDouble(const double v)
{
   return DoubleToString(v, 8);
}

string FP_ExportTime(const datetime t)
{
   if(t <= 0) return "";
   return TimeToString(t, TIME_DATE|TIME_SECONDS);
}

string FP_ExportCsvCell(const string raw)
{
   string s = raw;
   StringReplace(s, "\r", " ");
   StringReplace(s, "\n", " ");
   StringReplace(s, "\"", "\"\"");
   return "\"" + s + "\"";
}

void FP_ExportCsvAppend(string &line, const string cell)
{
   if(line != "") line += ",";
   line += FP_ExportCsvCell(cell);
}

string FP_ExportSafeName(const string raw)
{
   string s = raw;
   StringReplace(s, " ", "_");
   StringReplace(s, ":", "-");
   StringReplace(s, "/", "-");
   StringReplace(s, "\\", "-");
   StringReplace(s, "*", "_");
   StringReplace(s, "?", "_");
   StringReplace(s, "\"", "_");
   StringReplace(s, "<", "_");
   StringReplace(s, ">", "_");
   StringReplace(s, "|", "_");
   StringReplace(s, ",", "_");
   StringReplace(s, ";", "_");
   return s;
}

string FP_ExportRunId(const string symbol, const ENUM_TIMEFRAMES period, const FP_ExportConfig &cfg)
{
   if(cfg.run_tag != "") return FP_ExportSafeName(cfg.run_tag);
   string stamp = TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS);
   return FP_ExportSafeName(symbol + "_" + EnumToString(period) + "_" + stamp);
}

string FP_ExportFileName(const string run_id, const string suffix, const FP_ExportConfig &cfg)
{
   if(cfg.overwrite_latest) return "latest_" + suffix + ".csv";
   return run_id + "_" + suffix + ".csv";
}

string FP_ExportJoinPath(const string folder, const string file_name)
{
   if(folder == "") return file_name;
   return folder + "\\" + file_name;
}

bool FP_ExportEnsureFolder(const string folder)
{
   if(folder == "") return true;
   FolderCreate(folder);
   return true;
}

void FP_ExportAppendNodeColumns(string &line, const FP_Node &n)
{
   FP_ExportCsvAppend(line, FP_ExportInt(n.id));
   FP_ExportCsvAppend(line, FP_NodeKindName(n.kind));
   FP_ExportCsvAppend(line, FP_ExportInt(n.L));
   FP_ExportCsvAppend(line, FP_ExportInt(n.index_anchor));
   FP_ExportCsvAppend(line, FP_ExportTime(n.time_anchor));
   FP_ExportCsvAppend(line, FP_ExportDouble(n.price));
   FP_ExportCsvAppend(line, FP_ExportBool(n.confirmed));
   FP_ExportCsvAppend(line, n.structural_id);
   FP_ExportCsvAppend(line, n.visual_id);
}

string FP_ExportNodeHeader(const string prefix)
{
   string h = "";
   FP_ExportCsvAppend(h, prefix + "_id");
   FP_ExportCsvAppend(h, prefix + "_kind");
   FP_ExportCsvAppend(h, prefix + "_L");
   FP_ExportCsvAppend(h, prefix + "_anchor_index");
   FP_ExportCsvAppend(h, prefix + "_anchor_time");
   FP_ExportCsvAppend(h, prefix + "_price");
   FP_ExportCsvAppend(h, prefix + "_confirmed");
   FP_ExportCsvAppend(h, prefix + "_structural_id");
   FP_ExportCsvAppend(h, prefix + "_visual_id");
   return h;
}

void FP_ExportAppendHeaderChunk(string &line, const string chunk)
{
   if(chunk == "") return;
   if(line != "") line += ",";
   line += chunk;
}

string FP_ExportEventsHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "run_id");
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "bars");
   FP_ExportCsvAppend(h, "event_id");
   FP_ExportCsvAppend(h, "canonical_id");
   FP_ExportCsvAppend(h, "structural_id");
   FP_ExportCsvAppend(h, "visual_id");
   FP_ExportCsvAppend(h, "phase_id");
   FP_ExportCsvAppend(h, "chain_id");
   FP_ExportCsvAppend(h, "audit_id");
   FP_ExportCsvAppend(h, "sequence_id");
   FP_ExportCsvAppend(h, "parent_event_id");
   FP_ExportCsvAppend(h, "parent_sequence_id");
   FP_ExportCsvAppend(h, "chain_index");
   FP_ExportCsvAppend(h, "scale_L");
   FP_ExportCsvAppend(h, "direction");
   FP_ExportCsvAppend(h, "level");
   FP_ExportCsvAppend(h, "status");
   FP_ExportCsvAppend(h, "branch_kind");
   FP_ExportCsvAppend(h, "render_kind");
   FP_ExportCsvAppend(h, "visible_main");
   FP_ExportCsvAppend(h, "hidden_reason");
   FP_ExportCsvAppend(h, "from_phase_boundary");
   FP_ExportCsvAppend(h, "from_fail_open");
   FP_ExportCsvAppend(h, "source_mode");
   FP_ExportCsvAppend(h, "flag_size");
   FP_ExportCsvAppend(h, "parent_flag_size");
   FP_ExportCsvAppend(h, "size_ratio");
   FP_ExportCsvAppend(h, "leg1_L");
   FP_ExportCsvAppend(h, "parent_leg1_L");
   FP_ExportCsvAppend(h, "body_id");
   FP_ExportCsvAppend(h, "body_status");
   FP_ExportCsvAppend(h, "body_reason");
   FP_ExportCsvAppend(h, "internal_pack_id");
   FP_ExportCsvAppend(h, "internal_count");
   FP_ExportCsvAppend(h, "internal_valid12");
   FP_ExportCsvAppend(h, "internal_status");
   FP_ExportCsvAppend(h, "internal_reason");
   FP_ExportCsvAppend(h, "f1_lifecycle_status");
   FP_ExportCsvAppend(h, "f1_can_spawn_f2");
   FP_ExportCsvAppend(h, "f1_lifecycle_reason");
   FP_ExportCsvAppend(h, "f2_lifecycle_status");
   FP_ExportCsvAppend(h, "f2_size_gate_passed");
   FP_ExportCsvAppend(h, "f2_can_spawn_f3");
   FP_ExportCsvAppend(h, "f2_parent_size_ratio");
   FP_ExportCsvAppend(h, "f2_lifecycle_reason");
   FP_ExportCsvAppend(h, "f3_lifecycle_status");
   FP_ExportCsvAppend(h, "f3_or_gate_passed");
   FP_ExportCsvAppend(h, "f3_locked");
   FP_ExportCsvAppend(h, "f3_lock_event_id");
   FP_ExportCsvAppend(h, "f3_lock_reason");
   FP_ExportCsvAppend(h, "f3_lifecycle_reason");
   FP_ExportCsvAppend(h, "phase_direction");
   FP_ExportCsvAppend(h, "phase_owner_root_id");
   FP_ExportCsvAppend(h, "chain_state");
   FP_ExportCsvAppend(h, "next_expected_f_level");
   FP_ExportCsvAppend(h, "phase_reset_reason");
   FP_ExportCsvAppend(h, "owner_rank_score");
   FP_ExportCsvAppend(h, "canonical_state");
   FP_ExportCsvAppend(h, "canonical_rank_final");
   FP_ExportCsvAppend(h, "canonical_conflict_group_id");
   FP_ExportCsvAppend(h, "canonical_invariant_flags");
   FP_ExportCsvAppend(h, "canonical_reason");
   FP_ExportAppendHeaderChunk(h, FP_ExportNodeHeader("origin"));
   FP_ExportAppendHeaderChunk(h, FP_ExportNodeHeader("leg1"));
   FP_ExportAppendHeaderChunk(h, FP_ExportNodeHeader("waist"));
   FP_ExportAppendHeaderChunk(h, FP_ExportNodeHeader("leg2"));
   FP_ExportAppendHeaderChunk(h, FP_ExportNodeHeader("confirm"));
   FP_ExportAppendHeaderChunk(h, FP_ExportNodeHeader("invalid"));
   FP_ExportAppendHeaderChunk(h, FP_ExportNodeHeader("extension_end"));
   FP_ExportCsvAppend(h, "reason");
   return h;
}

string FP_ExportEventRow(const string run_id,
                         const string symbol,
                         const ENUM_TIMEFRAMES period,
                         const int bars,
                         const FP_FlagEvent &e)
{
   string line = "";
   FP_ExportCsvAppend(line, run_id);
   FP_ExportCsvAppend(line, symbol);
   FP_ExportCsvAppend(line, EnumToString(period));
   FP_ExportCsvAppend(line, FP_ExportInt(bars));
   FP_ExportCsvAppend(line, FP_ExportInt(e.event_id));
   FP_ExportCsvAppend(line, e.canonical_id);
   FP_ExportCsvAppend(line, e.structural_id);
   FP_ExportCsvAppend(line, e.visual_id);
   FP_ExportCsvAppend(line, e.phase_id);
   FP_ExportCsvAppend(line, e.chain_id);
   FP_ExportCsvAppend(line, e.audit_id);
   FP_ExportCsvAppend(line, FP_ExportInt(e.sequence_id));
   FP_ExportCsvAppend(line, FP_ExportInt(e.parent_event_id));
   FP_ExportCsvAppend(line, FP_ExportInt(e.parent_sequence_id));
   FP_ExportCsvAppend(line, FP_ExportInt(e.chain_index));
   FP_ExportCsvAppend(line, FP_ExportInt(e.scale_L));
   FP_ExportCsvAppend(line, FP_DirectionName(e.direction));
   FP_ExportCsvAppend(line, FP_LevelName(e.level));
   FP_ExportCsvAppend(line, FP_StatusName(e.status));
   FP_ExportCsvAppend(line, FP_ExportInt(e.branch_kind));
   FP_ExportCsvAppend(line, FP_ExportInt(e.render_kind));
   FP_ExportCsvAppend(line, FP_ExportBool(e.visible_main));
   FP_ExportCsvAppend(line, e.hidden_reason);
   FP_ExportCsvAppend(line, FP_ExportBool(e.from_phase_boundary));
   FP_ExportCsvAppend(line, FP_ExportBool(e.from_fail_open));
   FP_ExportCsvAppend(line, e.source_mode);
   FP_ExportCsvAppend(line, FP_ExportDouble(e.flag_size));
   FP_ExportCsvAppend(line, FP_ExportDouble(e.parent_flag_size));
   FP_ExportCsvAppend(line, FP_ExportDouble(e.size_ratio));
   FP_ExportCsvAppend(line, FP_ExportInt(e.leg1_L));
   FP_ExportCsvAppend(line, FP_ExportInt(e.parent_leg1_L));
   FP_ExportCsvAppend(line, e.body_id);
   FP_ExportCsvAppend(line, FP_BodyStatusName(e.body_status));
   FP_ExportCsvAppend(line, e.body_reason);
   FP_ExportCsvAppend(line, e.internal_pack.internal_pack_id);
   FP_ExportCsvAppend(line, FP_ExportInt(e.internal_pack.count));
   FP_ExportCsvAppend(line, FP_ExportBool(e.internal_pack.valid12));
   FP_ExportCsvAppend(line, e.internal_pack.status);
   FP_ExportCsvAppend(line, e.internal_pack.reason);
   FP_ExportCsvAppend(line, FP_F1LifecycleStatusName(e.lifecycle_status));
   FP_ExportCsvAppend(line, FP_ExportBool(e.lifecycle_can_spawn_f2));
   FP_ExportCsvAppend(line, e.lifecycle_reason);
   FP_ExportCsvAppend(line, FP_F2LifecycleStatusName(e.f2_lifecycle_status));
   FP_ExportCsvAppend(line, FP_ExportBool(e.f2_size_gate_passed));
   FP_ExportCsvAppend(line, FP_ExportBool(e.f2_can_spawn_f3));
   FP_ExportCsvAppend(line, FP_ExportDouble(e.f2_parent_size_ratio));
   FP_ExportCsvAppend(line, e.f2_lifecycle_reason);
   FP_ExportCsvAppend(line, FP_F3LifecycleStatusName(e.f3_lifecycle_status));
   FP_ExportCsvAppend(line, FP_ExportBool(e.f3_or_gate_passed));
   FP_ExportCsvAppend(line, FP_ExportBool(e.f3_locked));
   FP_ExportCsvAppend(line, FP_ExportInt(e.f3_lock_event_id));
   FP_ExportCsvAppend(line, e.f3_lock_reason);
   FP_ExportCsvAppend(line, e.f3_lifecycle_reason);
   FP_ExportCsvAppend(line, FP_DirectionName(e.phase_direction));
   FP_ExportCsvAppend(line, FP_ExportInt(e.phase_owner_root_id));
   FP_ExportCsvAppend(line, FP_OwnershipChainStateName(e.chain_state));
   FP_ExportCsvAppend(line, FP_LevelName(e.next_expected_f_level));
   FP_ExportCsvAppend(line, e.phase_reset_reason);
   FP_ExportCsvAppend(line, FP_ExportInt(e.owner_rank_score));
   FP_ExportCsvAppend(line, FP_ExportInt(e.canonical_state));
   FP_ExportCsvAppend(line, FP_ExportInt(e.canonical_rank_final));
   FP_ExportCsvAppend(line, e.canonical_conflict_group_id);
   FP_ExportCsvAppend(line, FP_ExportInt(e.canonical_invariant_flags));
   FP_ExportCsvAppend(line, e.canonical_reason);
   FP_ExportAppendNodeColumns(line, e.origin);
   FP_ExportAppendNodeColumns(line, e.leg1);
   FP_ExportAppendNodeColumns(line, e.waist);
   FP_ExportAppendNodeColumns(line, e.leg2);
   FP_ExportAppendNodeColumns(line, e.confirm);
   FP_ExportAppendNodeColumns(line, e.invalid);
   FP_ExportAppendNodeColumns(line, e.extension_end);
   FP_ExportCsvAppend(line, e.reason);
   return line;
}

string FP_ExportHooksHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "run_id");
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "branch_id");
   FP_ExportCsvAppend(h, "scale_L");
   FP_ExportCsvAppend(h, "direction");
   FP_ExportCsvAppend(h, "status");
   FP_ExportCsvAppend(h, "node_count");
   FP_ExportCsvAppend(h, "side_kind");
   FP_ExportCsvAppend(h, "is_nd");
   FP_ExportCsvAppend(h, "nd_qualified");
   FP_ExportCsvAppend(h, "seeds_visible_f1");
   FP_ExportCsvAppend(h, "visible_main");
   FP_ExportCsvAppend(h, "hidden_reason");
   FP_ExportCsvAppend(h, "retrace_ratio");
   FP_ExportCsvAppend(h, "max_branch_len");
   FP_ExportCsvAppend(h, "cycle_start_broken");
   FP_ExportCsvAppend(h, "structural_id");
   FP_ExportCsvAppend(h, "visual_id");
   FP_ExportCsvAppend(h, "phase_id");
   FP_ExportCsvAppend(h, "chain_id");
   FP_ExportCsvAppend(h, "audit_id");
   FP_ExportAppendHeaderChunk(h, FP_ExportNodeHeader("start"));
   FP_ExportAppendHeaderChunk(h, FP_ExportNodeHeader("cycle_start"));
   FP_ExportAppendHeaderChunk(h, FP_ExportNodeHeader("extreme"));
   FP_ExportAppendHeaderChunk(h, FP_ExportNodeHeader("resolve"));
   FP_ExportAppendHeaderChunk(h, FP_ExportNodeHeader("n1"));
   FP_ExportAppendHeaderChunk(h, FP_ExportNodeHeader("n2"));
   FP_ExportAppendHeaderChunk(h, FP_ExportNodeHeader("n3"));
   FP_ExportAppendHeaderChunk(h, FP_ExportNodeHeader("n4"));
   FP_ExportCsvAppend(h, "reason");
   return h;
}

string FP_ExportHookRow(const string run_id,
                        const string symbol,
                        const ENUM_TIMEFRAMES period,
                        const FP_HookBranch &h)
{
   string line = "";
   FP_ExportCsvAppend(line, run_id);
   FP_ExportCsvAppend(line, symbol);
   FP_ExportCsvAppend(line, EnumToString(period));
   FP_ExportCsvAppend(line, FP_ExportInt(h.branch_id));
   FP_ExportCsvAppend(line, FP_ExportInt(h.scale_L));
   FP_ExportCsvAppend(line, FP_DirectionName(h.direction));
   FP_ExportCsvAppend(line, FP_StatusName(h.status));
   FP_ExportCsvAppend(line, FP_ExportInt(h.node_count));
   FP_ExportCsvAppend(line, FP_NodeKindName(h.side_kind));
   FP_ExportCsvAppend(line, FP_ExportBool(h.is_nd));
   FP_ExportCsvAppend(line, FP_ExportBool(h.nd_qualified));
   FP_ExportCsvAppend(line, FP_ExportBool(h.seeds_visible_f1));
   FP_ExportCsvAppend(line, FP_ExportBool(h.visible_main));
   FP_ExportCsvAppend(line, h.hidden_reason);
   FP_ExportCsvAppend(line, FP_ExportDouble(h.retrace_ratio));
   FP_ExportCsvAppend(line, FP_ExportInt(h.max_branch_len));
   FP_ExportCsvAppend(line, FP_ExportBool(h.is_cycle_start_broken));
   FP_ExportCsvAppend(line, h.structural_id);
   FP_ExportCsvAppend(line, h.visual_id);
   FP_ExportCsvAppend(line, h.phase_id);
   FP_ExportCsvAppend(line, h.chain_id);
   FP_ExportCsvAppend(line, h.audit_id);
   FP_ExportAppendNodeColumns(line, h.start_node);
   FP_ExportAppendNodeColumns(line, h.cycle_start_node);
   FP_ExportAppendNodeColumns(line, h.extreme_node);
   FP_ExportAppendNodeColumns(line, h.resolve_node);
   FP_ExportAppendNodeColumns(line, h.n1);
   FP_ExportAppendNodeColumns(line, h.n2);
   FP_ExportAppendNodeColumns(line, h.n3);
   FP_ExportAppendNodeColumns(line, h.n4);
   FP_ExportCsvAppend(line, h.reason);
   return line;
}

string FP_ExportSummaryHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "run_id");
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "bars");
   FP_ExportCsvAppend(h, "scale_count");
   FP_ExportCsvAppend(h, "raw_nodes");
   FP_ExportCsvAppend(h, "canonical_nodes");
   FP_ExportCsvAppend(h, "hooks");
   FP_ExportCsvAppend(h, "nd");
   FP_ExportCsvAppend(h, "events");
   FP_ExportCsvAppend(h, "visible_events");
   FP_ExportCsvAppend(h, "hidden_events");
   FP_ExportCsvAppend(h, "f1");
   FP_ExportCsvAppend(h, "f2");
   FP_ExportCsvAppend(h, "f3");
   FP_ExportCsvAppend(h, "confirmed_f1");
   FP_ExportCsvAppend(h, "confirmed_f2");
   FP_ExportCsvAppend(h, "completed_f3");
   FP_ExportCsvAppend(h, "locked_f3");
   FP_ExportCsvAppend(h, "canonical_invariant_failures");
   FP_ExportCsvAppend(h, "canonical_visible_duplicate_after");
   FP_ExportCsvAppend(h, "canonical_parent_missing_after");
   FP_ExportCsvAppend(h, "export_events_written");
   FP_ExportCsvAppend(h, "export_hooks_written");
   FP_ExportCsvAppend(h, "export_files_written");
   FP_ExportCsvAppend(h, "export_file_errors");
   return h;
}

string FP_ExportSummaryRow(const string run_id,
                           const string symbol,
                           const ENUM_TIMEFRAMES period,
                           const int bars,
                           const int scale_count,
                           const FP_DetectResult &r)
{
   string line = "";
   FP_ExportCsvAppend(line, run_id);
   FP_ExportCsvAppend(line, symbol);
   FP_ExportCsvAppend(line, EnumToString(period));
   FP_ExportCsvAppend(line, FP_ExportInt(bars));
   FP_ExportCsvAppend(line, FP_ExportInt(scale_count));
   FP_ExportCsvAppend(line, FP_ExportInt(r.raw_nodes_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.nodes_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.hooks_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.nd_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.events_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.visible_events_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.hidden_events_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.f1_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.f2_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.f3_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.f1_lifecycle_confirmed_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.f2_lifecycle_confirmed_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.f3_lifecycle_completed_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.f3_lifecycle_locked_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.canonical_invariant_failures_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.canonical_visible_duplicate_after_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.canonical_parent_missing_after_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.export_events_written_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.export_hooks_written_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.export_files_written_total));
   FP_ExportCsvAppend(line, FP_ExportInt(r.export_file_errors_total));
   return line;
}

#endif // __FP_EXPORT_ROWS_MQH__
