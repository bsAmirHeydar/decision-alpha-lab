#ifndef __FP_NODE_EXTRACT_TYPES_MQH__
#define __FP_NODE_EXTRACT_TYPES_MQH__
#property strict

#include "FP_Types.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 02 / Node Extraction Types
// ----------------------------------------------------------------------------
// This module owns the standalone audit structs for canonical node extraction.
// Higher layers should receive FP_Node arrays plus these reports; renderer state
// must never be used to justify node existence.
// ============================================================================

enum FP_NodeSource
{
   FP_NODE_SOURCE_NONE              = 0,
   FP_NODE_SOURCE_CONFIRMED_HISTORY = 1,
   FP_NODE_SOURCE_LIVE_CANDIDATE    = 2
};

enum FP_NodeClearanceStatus
{
   FP_NODE_CLEARANCE_NONE       = 0,
   FP_NODE_CLEARANCE_OK         = 1,
   FP_NODE_CLEARANCE_PENDING    = 2,
   FP_NODE_CLEARANCE_BROKEN     = -1,
   FP_NODE_CLEARANCE_NOT_ENOUGH = -2
};

struct FP_NodeExtractConfig
{
   int     L;
   bool    include_pending;
   double  epsilon_points;
   bool    strict_contract;
   bool    print_sanity;
   bool    print_samples;
   int     sample_limit;
};

struct FP_NodeExtractReport
{
   bool    ok;
   string  status;
   string  reason;

   int     L;
   int     total_bars;
   bool    include_pending;
   double  epsilon_points;
   double  epsilon_price;

   int     candidate_high_plateaus;
   int     candidate_low_plateaus;
   int     raw_candidates;

   int     emitted_nodes;
   int     confirmed_nodes;
   int     pending_nodes;
   int     high_nodes;
   int     low_nodes;

   int     rejected_left;
   int     rejected_right;
   int     rejected_pending_not_allowed;
   int     rejected_invalid_params;
   int     left_broken;
   int     right_broken;
   int     left_not_enough;
   int     right_pending;

   int     equality_touches_skipped;
   int     plateau_max_width;
   int     first_anchor_index;
   int     last_anchor_index;
   datetime first_anchor_time;
   datetime last_anchor_time;
};

struct FP_NodeCompressReport
{
   bool    ok;
   string  status;
   string  reason;

   int     L;
   int     raw_count;
   int     compressed_count;
   int     same_side_runs;
   int     replaced_by_more_extreme;
   int     discarded_less_extreme;
   int     alternating_boundaries;
   int     pending_nodes_out;
   int     confirmed_nodes_out;
   int     high_nodes_out;
   int     low_nodes_out;
   int     first_anchor_index;
   int     last_anchor_index;
   datetime first_anchor_time;
   datetime last_anchor_time;
};

void FP_DefaultNodeExtractConfig(FP_NodeExtractConfig &cfg)
{
   cfg.L = 2;
   cfg.include_pending = false;
   cfg.epsilon_points = 0.0;
   cfg.strict_contract = true;
   cfg.print_sanity = false;
   cfg.print_samples = false;
   cfg.sample_limit = 6;
}

void FP_ResetNodeExtractReport(FP_NodeExtractReport &r)
{
   r.ok = false;
   r.status = "reset";
   r.reason = "reset";

   r.L = 0;
   r.total_bars = 0;
   r.include_pending = false;
   r.epsilon_points = 0.0;
   r.epsilon_price = 0.0;

   r.candidate_high_plateaus = 0;
   r.candidate_low_plateaus = 0;
   r.raw_candidates = 0;

   r.emitted_nodes = 0;
   r.confirmed_nodes = 0;
   r.pending_nodes = 0;
   r.high_nodes = 0;
   r.low_nodes = 0;

   r.rejected_left = 0;
   r.rejected_right = 0;
   r.rejected_pending_not_allowed = 0;
   r.rejected_invalid_params = 0;
   r.left_broken = 0;
   r.right_broken = 0;
   r.left_not_enough = 0;
   r.right_pending = 0;

   r.equality_touches_skipped = 0;
   r.plateau_max_width = 0;
   r.first_anchor_index = -1;
   r.last_anchor_index = -1;
   r.first_anchor_time = 0;
   r.last_anchor_time = 0;
}

void FP_ResetNodeCompressReport(FP_NodeCompressReport &r)
{
   r.ok = false;
   r.status = "reset";
   r.reason = "reset";

   r.L = 0;
   r.raw_count = 0;
   r.compressed_count = 0;
   r.same_side_runs = 0;
   r.replaced_by_more_extreme = 0;
   r.discarded_less_extreme = 0;
   r.alternating_boundaries = 0;
   r.pending_nodes_out = 0;
   r.confirmed_nodes_out = 0;
   r.high_nodes_out = 0;
   r.low_nodes_out = 0;
   r.first_anchor_index = -1;
   r.last_anchor_index = -1;
   r.first_anchor_time = 0;
   r.last_anchor_time = 0;
}

string FP_NodeSourceName(const int source)
{
   if(source == FP_NODE_SOURCE_CONFIRMED_HISTORY) return "confirmed_history";
   if(source == FP_NODE_SOURCE_LIVE_CANDIDATE)    return "live_candidate";
   return "none";
}

string FP_NodeClearanceStatusName(const int status)
{
   if(status == FP_NODE_CLEARANCE_OK)         return "ok";
   if(status == FP_NODE_CLEARANCE_PENDING)    return "pending";
   if(status == FP_NODE_CLEARANCE_BROKEN)     return "broken";
   if(status == FP_NODE_CLEARANCE_NOT_ENOUGH) return "not_enough";
   return "none";
}

#endif // __FP_NODE_EXTRACT_TYPES_MQH__
