#ifndef __FP_OWNERSHIP_TYPES_MQH__
#define __FP_OWNERSHIP_TYPES_MQH__
#property strict

#include "FP_Types.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 10 / Ownership Types
// ----------------------------------------------------------------------------
// Ownership is the semantic main-chart phase layer. It runs after F1/F2/F3
// lifecycle emission and before visual duplicate pruning / renderer output.
// ============================================================================

struct FP_OwnershipReport
{
   int events_seen;
   int visible_before;
   int visible_after;
   int phases_seen;
   int root_candidates;
   int owner_roots;
   int competing_roots;
   int resets;
   int hidden_roots;
   int hidden_descendants;
   int orphans_hidden;
   int failopen_hidden;
   int superseded_parent_hides;
   int phase_safe_duplicate_hides;
   int max_owner_rank;
   int min_owner_rank;
   string reason;
};

void FP_ResetOwnershipReport(FP_OwnershipReport &r)
{
   r.events_seen = 0;
   r.visible_before = 0;
   r.visible_after = 0;
   r.phases_seen = 0;
   r.root_candidates = 0;
   r.owner_roots = 0;
   r.competing_roots = 0;
   r.resets = 0;
   r.hidden_roots = 0;
   r.hidden_descendants = 0;
   r.orphans_hidden = 0;
   r.failopen_hidden = 0;
   r.superseded_parent_hides = 0;
   r.phase_safe_duplicate_hides = 0;
   r.max_owner_rank = -1000000000;
   r.min_owner_rank = 1000000000;
   r.reason = "";
}

void FP_RecordOwnershipRank(FP_OwnershipReport &r, const int rank)
{
   if(rank > r.max_owner_rank) r.max_owner_rank = rank;
   if(rank < r.min_owner_rank) r.min_owner_rank = rank;
}

#endif // __FP_OWNERSHIP_TYPES_MQH__
