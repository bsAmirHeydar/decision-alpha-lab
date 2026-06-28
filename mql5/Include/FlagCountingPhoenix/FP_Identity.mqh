#ifndef __FP_IDENTITY_MQH__
#define __FP_IDENTITY_MQH__
#property strict

#include "FP_NodeExtractTypes.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 03 / Identity Kernel
// ----------------------------------------------------------------------------
// Owns deterministic semantic, visual, phase, chain, and audit identities.
// Later layers may rank or hide objects, but they must not invent identity.
// ============================================================================

string FP_IdSafe(string s)
{
   if(s == "") return "na";
   StringReplace(s, " ", "_");
   StringReplace(s, ":", "-");
   StringReplace(s, "|", "-");
   StringReplace(s, ";", "-");
   StringReplace(s, ",", "-");
   return s;
}

string FP_PriceKey(const double price)
{
   return DoubleToString(price, _Digits);
}

string FP_NodeSideKey(const int kind)
{
   if(kind == FP_NODE_HIGH) return "H";
   if(kind == FP_NODE_LOW) return "L";
   return "N";
}

string FP_DirectionKey(const int direction)
{
   if(direction == FP_DIR_BULLISH) return "BULL";
   if(direction == FP_DIR_BEARISH) return "BEAR";
   return "NONE";
}

string FP_LevelKey(const int level)
{
   if(level == FP_LEVEL_F1) return "F1";
   if(level == FP_LEVEL_F2) return "F2";
   if(level == FP_LEVEL_F3) return "F3";
   if(level == FP_LEVEL_ND) return "ND";
   return "LX";
}

string FP_StatusKey(const int status)
{
   return FP_StatusName(status);
}

string FP_NodeStructuralId(const FP_Node &n)
{
   if(n.kind == FP_NODE_NONE || n.index_anchor < 0) return "N:none";
   return "N:s=" + FP_NodeSideKey(n.kind) +
          "|L=" + IntegerToString(n.L) +
          "|a=" + IntegerToString(n.index_anchor) +
          "|p=" + FP_PriceKey(n.price) +
          "|pl=" + IntegerToString(n.plateau_start_index) + "-" + IntegerToString(n.plateau_end_index);
}

string FP_NodeVisualId(const FP_Node &n)
{
   if(n.kind == FP_NODE_NONE || n.index_anchor < 0) return "NV:none";
   return "NV:s=" + FP_NodeSideKey(n.kind) +
          "|a=" + IntegerToString(n.index_anchor) +
          "|p=" + FP_PriceKey(n.price);
}

string FP_NodeAuditId(const FP_Node &n, const string generation_pass="L03")
{
   return "A:node|pass=" + FP_IdSafe(generation_pass) + "|" + FP_NodeStructuralId(n) + "|src=" + FP_NodeSourceName(n.source);
}

void FP_AssignNodeIdentity(FP_Node &n, const string generation_pass="L03")
{
   n.structural_id = FP_NodeStructuralId(n);
   n.visual_id = FP_NodeVisualId(n);
   n.phase_id = "";
   n.chain_id = "";
   n.audit_id = FP_NodeAuditId(n, generation_pass);
   n.source_mode = FP_NodeSourceName(n.source);
   n.hidden_reason = "";
   n.visible_main = true;
   n.is_fail_open = false;
   n.canonical_rank_score = 0;
}

void FP_AssignNodeIdentities(FP_Node &nodes[], const string generation_pass="L03")
{
   for(int i=0; i<ArraySize(nodes); i++)
      FP_AssignNodeIdentity(nodes[i], generation_pass);
}

bool FP_NodeVisualIdentityEqual(const FP_Node &a, const FP_Node &b)
{
   if(a.visual_id != "" && b.visual_id != "") return (a.visual_id == b.visual_id);
   return (a.kind == b.kind && a.index_anchor == b.index_anchor && a.price == b.price);
}

bool FP_NodeStructuralIdentityEqual(const FP_Node &a, const FP_Node &b)
{
   if(a.structural_id != "" && b.structural_id != "") return (a.structural_id == b.structural_id);
   return (a.id == b.id && a.L == b.L && a.kind == b.kind && a.index_anchor == b.index_anchor && a.price == b.price);
}

string FP_BodyNodeVisualKey(const FP_FlagEvent &e)
{
   string key = "O=" + FP_NodeVisualId(e.origin) + "|A=" + FP_NodeVisualId(e.leg1);
   if(e.has_waist) key = key + "|W=" + FP_NodeVisualId(e.waist);
   else key = key + "|W=none";
   if(e.has_leg2) key = key + "|B=" + FP_NodeVisualId(e.leg2);
   else key = key + "|B=none";
   return key;
}

string FP_BodyNodeStructuralKey(const FP_FlagEvent &e)
{
   string key = "O=" + FP_NodeStructuralId(e.origin) + "|A=" + FP_NodeStructuralId(e.leg1);
   if(e.has_waist) key = key + "|W=" + FP_NodeStructuralId(e.waist);
   else key = key + "|W=none";
   if(e.has_leg2) key = key + "|B=" + FP_NodeStructuralId(e.leg2);
   else key = key + "|B=none";
   return key;
}

string FP_EventSourceMode(const FP_FlagEvent &e)
{
   if(e.from_phase_boundary) return "phase_boundary";
   if(e.from_fail_open) return "fail_open";
   return "raw";
}

int FP_IdentityStatusRank(const int status)
{
   if(status == FP_STATUS_LOCKED) return 800;
   if(status == FP_STATUS_COMPLETED) return 700;
   if(status == FP_STATUS_CONFIRMED) return 600;
   if(status == FP_STATUS_QUALIFIED) return 500;
   if(status == FP_STATUS_POST_FLAG) return 400;
   if(status == FP_STATUS_LIVE_BODY) return 300;
   if(status == FP_STATUS_LIVE_LEG) return 200;
   if(status == FP_STATUS_SEED) return 100;
   if(status == FP_STATUS_INVALIDATED) return 50;
   return 0;
}


string FP_EventLifecycleKey(const FP_FlagEvent &e)
{
   if(e.level == FP_LEVEL_F3) return "f3=" + FP_F3LifecycleStatusName(e.f3_lifecycle_status);
   if(e.level == FP_LEVEL_F2) return "f2=" + FP_F2LifecycleStatusName(e.f2_lifecycle_status);
   if(e.level == FP_LEVEL_F1) return "f1=" + FP_F1LifecycleStatusName(e.lifecycle_status);
   return "st=" + FP_StatusName(e.status);
}

int FP_EventBaseCanonicalRank(const FP_FlagEvent &e)
{
   int score = FP_IdentityStatusRank(e.status);
   if(e.level == FP_LEVEL_F3 && (e.status == FP_STATUS_COMPLETED || e.status == FP_STATUS_LOCKED)) score += 500;
   if(e.level == FP_LEVEL_F2 && e.status == FP_STATUS_CONFIRMED) score += 250;
   if(e.from_phase_boundary) score += 200;
   if(!e.from_fail_open) score += 40;
   score -= MathMax(0, e.scale_L);
   return score;
}

string FP_EventPhaseId(const FP_FlagEvent &e, const FP_Config &cfg)
{
   int phase_start = (e.has_origin ? e.origin.index_anchor : -1);
   int boundary = phase_start;
   if(e.from_phase_boundary && e.has_origin) boundary = e.origin.index_anchor;
   return "PH:sym=" + FP_IdSafe(cfg.context_symbol) +
          "|tf=" + FP_IdSafe(cfg.context_timeframe) +
          "|dir=" + FP_DirectionKey(e.direction) +
          "|start=" + IntegerToString(phase_start) +
          "|boundary=" + IntegerToString(boundary);
}

string FP_EventChainId(const FP_FlagEvent &e, const string phase_id)
{
   return "CH:" + phase_id + "|seq=" + IntegerToString(e.sequence_id);
}

string FP_EventStructuralId(const FP_FlagEvent &e)
{
   return "EV:lv=" + FP_LevelKey(e.level) +
          "|dir=" + FP_DirectionKey(e.direction) +
          "|L=" + IntegerToString(e.scale_L) +
          "|chain=" + IntegerToString(e.chain_index) +
          "|lc=" + FP_EventLifecycleKey(e) +
          "|own=" + FP_OwnershipChainStateName(e.chain_state) +
          "|owner=" + IntegerToString(e.phase_owner_root_id) +
          "|" + FP_BodyNodeStructuralKey(e);
}

string FP_EventVisualId(const FP_FlagEvent &e)
{
   return "EVV:lv=" + FP_LevelKey(e.level) +
          "|dir=" + FP_DirectionKey(e.direction) +
          "|chain=" + IntegerToString(e.chain_index) +
          "|lc=" + FP_EventLifecycleKey(e) +
          "|own=" + FP_OwnershipChainStateName(e.chain_state) +
          "|owner=" + IntegerToString(e.phase_owner_root_id) +
          "|" + FP_BodyNodeVisualKey(e);
}

string FP_EventAuditId(const FP_FlagEvent &e, const FP_Config &cfg)
{
   return "A:event|pass=" + FP_IdSafe(cfg.identity_generation_pass) +
          "|src=" + FP_EventSourceMode(e) +
          "|lc=" + FP_EventLifecycleKey(e) +
          "|own=" + FP_OwnershipChainStateName(e.chain_state) +
          "|owner=" + IntegerToString(e.phase_owner_root_id) +
          "|cfg=" + FP_IdSafe(cfg.identity_config_hash) +
          "|" + e.structural_id;
}

void FP_AssignEventIdentity(FP_FlagEvent &e, const FP_Config &cfg)
{
   e.source_L = e.scale_L;
   e.source_mode = FP_EventSourceMode(e);
   e.is_fail_open = e.from_fail_open;
   e.canonical_rank_score = FP_EventBaseCanonicalRank(e);
   e.structural_id = FP_EventStructuralId(e);
   e.visual_id = FP_EventVisualId(e);
   e.phase_id = FP_EventPhaseId(e, cfg);
   e.chain_id = FP_EventChainId(e, e.phase_id);
   e.audit_id = FP_EventAuditId(e, cfg);
   if(e.visible_main) e.hidden_reason = "";
   else if(e.hidden_reason == "") e.hidden_reason = e.reason;
}

void FP_AssignEventIdentities(FP_FlagEvent &events[], const FP_Config &cfg)
{
   for(int i=0; i<ArraySize(events); i++)
      FP_AssignEventIdentity(events[i], cfg);
}

string FP_HookSourceMode(const FP_HookBranch &h)
{
   if(h.is_cycle_start_broken) return "hook_invalid_cycle_broken";
   if(h.is_nd) return "nd_hook";
   return "hook";
}

string FP_HookStructuralId(const FP_HookBranch &h)
{
   return "HK:dir=" + FP_DirectionKey(h.direction) +
          "|side=" + FP_NodeSideKey(h.side_kind) +
          "|L=" + IntegerToString(h.scale_L) +
          "|start=" + FP_NodeStructuralId(h.start_node) +
          "|cycle=" + FP_NodeStructuralId(h.cycle_start_node) +
          "|extreme=" + FP_NodeStructuralId(h.extreme_node) +
          "|resolve=" + FP_NodeStructuralId(h.resolve_node) +
          "|count=" + IntegerToString(h.node_count) +
          "|max=" + IntegerToString(h.max_branch_len) +
          "|nd=" + FP_BoolName(h.nd_qualified);
}

string FP_HookVisualId(const FP_HookBranch &h)
{
   FP_Node start;
   if(h.has_cycle_start) start = h.cycle_start_node;
   else start = h.start_node;
   return "HKV:dir=" + FP_DirectionKey(h.direction) +
          "|cycle=" + FP_NodeVisualId(start) +
          "|extreme=" + FP_NodeVisualId(h.extreme_node) +
          "|resolve=" + FP_NodeVisualId(h.resolve_node);
}

string FP_HookPhaseId(const FP_HookBranch &h, const FP_Config &cfg)
{
   int phase_start = (h.has_cycle_start ? h.cycle_start_node.index_anchor : h.start_node.index_anchor);
   int boundary = h.resolve_node.index_anchor;
   return "PH:sym=" + FP_IdSafe(cfg.context_symbol) +
          "|tf=" + FP_IdSafe(cfg.context_timeframe) +
          "|dir=" + FP_DirectionKey(h.direction) +
          "|start=" + IntegerToString(phase_start) +
          "|boundary=" + IntegerToString(boundary);
}

void FP_AssignHookIdentity(FP_HookBranch &h, const FP_Config &cfg)
{
   h.source_L = h.scale_L;
   h.source_mode = FP_HookSourceMode(h);
   h.is_fail_open = false;
   h.canonical_rank_score = (h.is_nd ? 200 : 100) + h.node_count + (h.seeds_visible_f1 ? 75 : 0) - MathMax(0, h.scale_L);
   h.structural_id = FP_HookStructuralId(h);
   h.visual_id = FP_HookVisualId(h);
   h.phase_id = FP_HookPhaseId(h, cfg);
   h.chain_id = "";
   h.audit_id = "A:hook|pass=" + FP_IdSafe(cfg.identity_generation_pass) +
                "|cfg=" + FP_IdSafe(cfg.identity_config_hash) +
                "|" + h.structural_id;
   if(h.visible_main)
      h.hidden_reason = "";
   else if(h.hidden_reason == "")
      h.hidden_reason = "hidden_hook_without_reason";
}

void FP_AssignHookIdentities(FP_HookBranch &hooks[], const FP_Config &cfg)
{
   for(int i=0; i<ArraySize(hooks); i++)
      FP_AssignHookIdentity(hooks[i], cfg);
}

bool FP_SamePhaseForMerge(const FP_FlagEvent &a, const FP_FlagEvent &b)
{
   if(a.phase_id == "" || b.phase_id == "") return true;
   return (a.phase_id == b.phase_id);
}

bool FP_SameEventVisualId(const FP_FlagEvent &a, const FP_FlagEvent &b)
{
   if(a.visual_id != "" && b.visual_id != "") return (a.visual_id == b.visual_id);
   return false;
}

void FP_SetHiddenReason(FP_FlagEvent &e, const string hidden_reason)
{
   e.visible_main = false;
   if(hidden_reason != "")
   {
      e.hidden_reason = hidden_reason;
      e.reason = e.reason + ";" + hidden_reason;
   }
   else if(e.hidden_reason == "")
   {
      e.hidden_reason = "hidden_without_reason";
      e.reason = e.reason + ";hidden_without_reason";
   }
}

void FP_NormalizeHiddenReasons(FP_FlagEvent &events[])
{
   for(int i=0; i<ArraySize(events); i++)
   {
      if(events[i].visible_main)
      {
         events[i].hidden_reason = "";
         continue;
      }
      if(events[i].hidden_reason == "")
      {
         if(events[i].reason != "") events[i].hidden_reason = events[i].reason;
         else events[i].hidden_reason = "hidden_without_reason";
      }
   }
}

#endif // __FP_IDENTITY_MQH__
