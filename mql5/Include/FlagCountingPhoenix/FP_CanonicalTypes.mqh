#ifndef __FP_CANONICAL_TYPES_MQH__
#define __FP_CANONICAL_TYPES_MQH__
#property strict

#include "FP_Types.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 11 / Canonicalization Types
// ----------------------------------------------------------------------------
// Level 11 is the last engine-owned consistency pass before renderer/export.
// It does not discover new market structure. It normalizes final event state,
// enforces audit invariants, and records why the final stream is trustworthy.
// ============================================================================

enum FP_CanonicalState
{
   FP_CANON_NONE              = 0,
   FP_CANON_VISIBLE           = 1,
   FP_CANON_HIDDEN            = 2,
   FP_CANON_HIDDEN_DUPLICATE  = 3,
   FP_CANON_HIDDEN_ORPHAN     = 4,
   FP_CANON_HIDDEN_INVALID    = 5,
   FP_CANON_REPAIRED          = 6,
   FP_CANON_INVARIANT_FAILED  = 7
};

string FP_CanonicalStateName(const int state)
{
   if(state == FP_CANON_VISIBLE)          return "visible";
   if(state == FP_CANON_HIDDEN)           return "hidden";
   if(state == FP_CANON_HIDDEN_DUPLICATE) return "hidden_duplicate";
   if(state == FP_CANON_HIDDEN_ORPHAN)    return "hidden_orphan";
   if(state == FP_CANON_HIDDEN_INVALID)   return "hidden_invalid";
   if(state == FP_CANON_REPAIRED)         return "repaired";
   if(state == FP_CANON_INVARIANT_FAILED) return "invariant_failed";
   return "none";
}

struct FP_CanonicalReport
{
   int events_seen;
   int hooks_seen;
   int visible_before;
   int visible_after;
   int hidden_before;
   int hidden_after;

   int ids_reassigned;
   int event_ids_repaired;
   int parent_ids_repaired;
   int missing_identity_repaired;
   int hidden_reason_repaired;
   int visible_reason_cleaned;
   int hidden_no_reason_after;

   int visible_duplicate_groups;
   int visible_duplicates_hidden;
   int visual_id_duplicate_conflicts;
   int structural_id_duplicate_conflicts;
   int phase_safe_duplicate_hides;
   int exact_duplicate_hides;

   int orphan_visible_before;
   int orphan_hidden;
   int orphan_visible_after;
   int invalid_visible_hidden;
   int render_none_hidden;
   int missing_body_hidden;
   int chain_index_repaired;

   int invariant_checks;
   int invariant_failures;
   int visible_missing_identity;
   int visible_duplicate_visual_after;
   int parent_missing_after;
   int parent_mismatch_after;
   int phase_owner_missing_after;
   int broken_chain_after;

   int hooks_hidden_reason_repaired;
   int hooks_visible_after;
   int hooks_hidden_after;

   int max_canonical_rank;
   int min_canonical_rank;
   string status;
   string reason;
};

void FP_ResetCanonicalReport(FP_CanonicalReport &r)
{
   r.events_seen = 0;
   r.hooks_seen = 0;
   r.visible_before = 0;
   r.visible_after = 0;
   r.hidden_before = 0;
   r.hidden_after = 0;

   r.ids_reassigned = 0;
   r.event_ids_repaired = 0;
   r.parent_ids_repaired = 0;
   r.missing_identity_repaired = 0;
   r.hidden_reason_repaired = 0;
   r.visible_reason_cleaned = 0;
   r.hidden_no_reason_after = 0;

   r.visible_duplicate_groups = 0;
   r.visible_duplicates_hidden = 0;
   r.visual_id_duplicate_conflicts = 0;
   r.structural_id_duplicate_conflicts = 0;
   r.phase_safe_duplicate_hides = 0;
   r.exact_duplicate_hides = 0;

   r.orphan_visible_before = 0;
   r.orphan_hidden = 0;
   r.orphan_visible_after = 0;
   r.invalid_visible_hidden = 0;
   r.render_none_hidden = 0;
   r.missing_body_hidden = 0;
   r.chain_index_repaired = 0;

   r.invariant_checks = 0;
   r.invariant_failures = 0;
   r.visible_missing_identity = 0;
   r.visible_duplicate_visual_after = 0;
   r.parent_missing_after = 0;
   r.parent_mismatch_after = 0;
   r.phase_owner_missing_after = 0;
   r.broken_chain_after = 0;

   r.hooks_hidden_reason_repaired = 0;
   r.hooks_visible_after = 0;
   r.hooks_hidden_after = 0;

   r.max_canonical_rank = 0;
   r.min_canonical_rank = 0;
   r.status = "none";
   r.reason = "";
}

#endif // __FP_CANONICAL_TYPES_MQH__
