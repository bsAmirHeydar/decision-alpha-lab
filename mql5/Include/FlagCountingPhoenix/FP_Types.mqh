#ifndef __FP_TYPES_MQH__
#define __FP_TYPES_MQH__
#property strict

// ============================================================================
// FlagCounting Phoenix - Types and canonical helpers
// ----------------------------------------------------------------------------
// Clean rebuild namespace: FP_*
// This package intentionally does not include or depend on FlagCounting,
// FlagCountingVNext, or FlagCountingV6 modules.
// ============================================================================

#define FP_MAX_INTERNAL_NODES 4
#define FP_REASON_LEN         192

// ----------------------------- Core enums ----------------------------------

enum FP_NodeKind
{
   FP_NODE_NONE = 0,
   FP_NODE_HIGH = 1,
   FP_NODE_LOW  = -1
};

enum FP_Direction
{
   FP_DIR_NONE    = 0,
   FP_DIR_BULLISH = 1,
   FP_DIR_BEARISH = -1
};

enum FP_Level
{
   FP_LEVEL_NONE = 0,
   FP_LEVEL_F1   = 1,
   FP_LEVEL_F2   = 2,
   FP_LEVEL_F3   = 3,
   FP_LEVEL_ND   = 10
};

enum FP_Status
{
   FP_STATUS_NONE        = 0,
   FP_STATUS_SEED        = 1,
   FP_STATUS_LIVE_LEG    = 2,
   FP_STATUS_LIVE_BODY   = 3,
   FP_STATUS_POST_FLAG   = 4,
   FP_STATUS_QUALIFIED   = 5,
   FP_STATUS_CONFIRMED   = 6,
   FP_STATUS_COMPLETED   = 7,
   FP_STATUS_LOCKED      = 8,
   FP_STATUS_INVALIDATED = 9
};

enum FP_BranchKind
{
   FP_BRANCH_NONE            = 0,
   FP_BRANCH_NORMAL_INTERNAL = 1,
   FP_BRANCH_WAIST_BREAK     = 2,
   FP_BRANCH_ND_HOOK         = 3,
   FP_BRANCH_EXTENSION       = 4
};

enum FP_RenderKind
{
   FP_RENDER_NONE       = 0,
   FP_RENDER_FLAG_BODY  = 1,
   FP_RENDER_PROBABLE   = 2,
   FP_RENDER_HOOK_ARC   = 3,
   FP_RENDER_LABEL_ONLY = 4
};

// Level 05 body-construction state.  This is intentionally separate from
// lifecycle status: F1/F2/F3 may later confirm, complete, lock, or invalidate,
// but the body layer only owns whether O/A/W/B exists and whether Leg2 has
// been extended before the required internal count.
enum FP_BodyStatus
{
   FP_BODY_NONE            = 0,
   FP_BODY_SEED            = 1,
   FP_BODY_LIVE_LEG        = 2,
   FP_BODY_LIVE_CORRECTION = 3,
   FP_BODY_COMPLETE        = 4,
   FP_BODY_EXTENDED        = 5,
   FP_BODY_INVALID         = 6
};

// Level 07 F1 lifecycle state.  This is the semantic state of an F1 root after
// Level 05 body evidence and Level 06 internal-count evidence have been merged.
enum FP_F1LifecycleStatus
{
   FP_F1_LC_NONE           = 0,
   FP_F1_LC_PHASE_REJECTED = 1,
   FP_F1_LC_BODY_MISSING   = 2,
   FP_F1_LC_CANDIDATE      = 3,
   FP_F1_LC_POST_FLAG      = 4,
   FP_F1_LC_CONFIRMED      = 5,
   FP_F1_LC_INVALIDATED    = 6,
   FP_F1_LC_EXTENDED       = 7,
   FP_F1_LC_HIDDEN         = 8
};

// Level 08 F2 lifecycle state.  F2 is not just "the next body"; it must pass
// parent-readiness, F2-origin, parent-size, and internal confirmation gates
// before it can authorize F3 construction.
enum FP_F2LifecycleStatus
{
   FP_F2_LC_NONE            = 0,
   FP_F2_LC_PARENT_REJECTED = 1,
   FP_F2_LC_ORIGIN_MISSING  = 2,
   FP_F2_LC_BODY_MISSING    = 3,
   FP_F2_LC_SIZE_REJECTED   = 4,
   FP_F2_LC_CANDIDATE       = 5,
   FP_F2_LC_POST_FLAG       = 6,
   FP_F2_LC_CONFIRMED       = 7,
   FP_F2_LC_INVALIDATED     = 8,
   FP_F2_LC_EXTENDED        = 9,
   FP_F2_LC_HIDDEN          = 10
};

// Level 09 F3 lifecycle state. F3 is terminal: it uses parent-ready F2,
// terminal body construction, OR qualification by size or L, and later lock
// evidence from the first opposite confirmed F1.
enum FP_F3LifecycleStatus
{
   FP_F3_LC_NONE            = 0,
   FP_F3_LC_PARENT_REJECTED = 1,
   FP_F3_LC_ORIGIN_MISSING  = 2,
   FP_F3_LC_BODY_MISSING    = 3,
   FP_F3_LC_OR_REJECTED     = 4,
   FP_F3_LC_COMPLETED       = 5,
   FP_F3_LC_LOCKED          = 6,
   FP_F3_LC_HIDDEN          = 7
};

// Level 10 semantic ownership state. This layer owns main-chart phase truth after
// F1/F2/F3 lifecycles have emitted candidates. Renderer and duplicate pruning are
// not allowed to invent these states.
enum FP_OwnershipChainState
{
   FP_CHAIN_NONE             = 0,
   FP_CHAIN_F1_OWNER         = 1,
   FP_CHAIN_F2_SEARCH        = 2,
   FP_CHAIN_F2_OWNER         = 3,
   FP_CHAIN_F3_SEARCH        = 4,
   FP_CHAIN_F3_OWNER         = 5,
   FP_CHAIN_F3_EXTENSION     = 6,
   FP_CHAIN_LOCKED_BY_OP_F1  = 7,
   FP_CHAIN_RESET_ALLOWED    = 8,
   FP_CHAIN_HIDDEN_LOSER     = 9,
   FP_CHAIN_HIDDEN_DESCENDANT= 10,
   FP_CHAIN_ORPHAN_HIDDEN    = 11
};

// ------------------------------- Data model --------------------------------

struct FP_Node
{
   int       id;
   int       L;
   int       kind;
   int       index_start;
   int       index_end;
   int       index_anchor;
   datetime  time_start;
   datetime  time_end;
   datetime  time_anchor;
   double    price;
   bool      confirmed;

   // Level 02 explicit node-source fields. `confirmed` is kept for backward
   // compatibility with existing Phoenix modules; the explicit aliases make
   // audit and live-pending isolation unambiguous.
   bool      is_confirmed;
   bool      is_live_pending;
   int       source;
   int       plateau_start_index;
   int       plateau_end_index;

   // Level 03 identity fields. These are deterministic strings, not renderer
   // object names. Later layers may hide or rank objects but must not invent
   // node identity.
   string    structural_id;
   string    visual_id;
   string    phase_id;
   string    chain_id;
   string    audit_id;
   string    source_mode;
   bool      visible_main;
   bool      is_fail_open;
   int       canonical_rank_score;
   string    hidden_reason;
};

struct FP_InternalPack
{
   int      count;
   FP_Node  n1;
   FP_Node  n2;
   FP_Node  n3;
   FP_Node  n4;
   FP_Node  mid12;
   FP_Node  mid23;
   FP_Node  mid34;
   bool     has_mid12;
   bool     has_mid23;
   bool     has_mid34;
   bool     valid12;
   bool     is_nd;
   double   retrace_ratio;

   // Level 06 internal-count identity and audit fields.  The pack is a
   // lifecycle-support object, not a renderer object.  It proves why a body is
   // post-flag, confirmation-ready, confirmed, or invalidated.
   string   internal_pack_id;
   int      branch_id;
   string   branch_id_text;
   int      scan_start_pos;
   int      scan_end_pos;
   int      first_valid12_pos;
   bool     has_valid12;
   FP_Node  first_valid12_node;
   FP_Node  middle_opposite_node;
   bool     has_middle_opposite_node;
   bool     middle_opposite_breaks_leg2;
   FP_Node  pre_internal_leg2_extension_node;
   bool     has_pre_internal_leg2_extension;
   int      pre_internal_leg2_extension_pos;
   int      confirm_pos;
   int      invalid_pos;
   int      last_counted_pos;
   string   status;
   string   reason;
};

struct FP_HookBranch
{
   int      branch_id;
   int      scale_L;
   int      direction;
   int      status;
   int      node_count;
   // First counted same-side branch node. Kept as the semantic branch start
   // used by F1 phase boundary logic. Do not replace this with the cycle
   // boundary; otherwise downstream sequence ownership changes.
   FP_Node  start_node;

   // True visual/cycle boundary. The gray Hook/ND arc starts here. This is
   // the nearest older same-side node that is strictly beyond the resolve node
   // in the adverse direction; it must not be strictly broken before resolve.
   FP_Node  cycle_start_node;
   bool     has_cycle_start;

   FP_Node  extreme_node;
   FP_Node  resolve_node;
   FP_Node  n1;
   FP_Node  n2;
   FP_Node  n3;
   FP_Node  n4;
   double   retrace_ratio;
   bool     is_nd;

   // Level 04 explicit Hook/ND context fields. These make Hook a first-class
   // auditable phase context rather than a renderer decoration.
   int      side_kind;
   bool     is_cycle_start_broken;
   int      max_branch_len;
   bool     nd_qualified;
   bool     seeds_visible_f1;

   // Level 03 identity fields for Hook/ND context objects.
   string   structural_id;
   string   visual_id;
   string   phase_id;
   string   chain_id;
   string   audit_id;
   int      source_L;
   string   source_mode;
   bool     visible_main;
   bool     is_fail_open;
   int      canonical_rank_score;
   string   hidden_reason;

   string   reason;
};

struct FP_FlagEvent
{
   int      event_id;
   int      sequence_id;
   int      parent_event_id;
   int      parent_sequence_id;
   int      chain_index;
   int      scale_L;
   int      direction;
   int      level;
   int      status;
   int      branch_kind;
   int      render_kind;

   // Level 05 body identity/audit fields.  These are body-layer facts only;
   // they do not confirm F1/F2 or authorize sequence ownership.
   string   body_id;
   int      body_status;
   int      origin_hit_status;
   int      leg1_break_status;
   int      leg2_extension_count;
   int      body_scan_start_pos;
   int      body_scan_end_pos;
   string   body_reason;

   // Level 07 F1 lifecycle evidence.  F1 lifecycle is the only source allowed
   // to decide whether an F1 can spawn F2.  Body/internal layers provide facts;
   // this layer owns candidate/confirmed/invalidated/root visibility state.
   string   lifecycle_id;
   int      lifecycle_status;
   int      lifecycle_stage_level;
   bool     lifecycle_phase_gate_passed;
   bool     lifecycle_body_complete;
   bool     lifecycle_internal_ready;
   bool     lifecycle_can_spawn_f2;
   int      lifecycle_scan_start_pos;
   int      lifecycle_scan_end_pos;
   string   lifecycle_reason;

   // Level 08 F2 lifecycle evidence.  F2 lifecycle is the only source allowed
   // to decide whether an F2 can spawn F3.  F1 lifecycle proves parent-readiness;
   // this layer proves F2 origin, parent-size gate, F2 internal confirmation,
   // and Origin-boundary invalidation.
   string   f2_lifecycle_id;
   int      f2_lifecycle_status;
   bool     f2_parent_ready;
   bool     f2_origin_found;
   bool     f2_body_complete;
   bool     f2_size_gate_passed;
   bool     f2_internal_ready;
   bool     f2_can_spawn_f3;
   int      f2_origin_scan_start_pos;
   int      f2_lifecycle_scan_end_pos;
   double   f2_parent_size_ratio;
   string   f2_lifecycle_reason;

   // Level 09 F3 lifecycle evidence. F3 is a terminal body authorized only by a
   // confirmed F2. It completes through OR qualification, then may lock on the
   // first opposite confirmed F1.
   string   f3_lifecycle_id;
   int      f3_lifecycle_status;
   bool     f3_parent_ready;
   bool     f3_origin_found;
   bool     f3_body_complete;
   bool     f3_size_gate_passed;
   bool     f3_leg1_L_gate_passed;
   bool     f3_or_gate_passed;
   bool     f3_terminal_complete;
   bool     f3_lock_ready;
   bool     f3_locked;
   int      f3_origin_scan_start_pos;
   int      f3_lifecycle_scan_end_pos;
   double   f3_parent_size_ratio;
   double   f3_parent_leg1_L_ratio;
   int      f3_lock_event_id;
   string   f3_lock_reason;
   string   f3_lifecycle_reason;

   // Level 10 sequence ownership and phase state. Ownership is semantic, not
   // visual. These fields explain why a chain is the main phase owner or why it
   // has been hidden as a competing restart, descendant, or orphan.
   int      phase_direction;
   int      phase_owner_root_id;
   int      chain_state;
   int      next_expected_f_level;
   string   phase_reset_reason;
   int      owner_rank_score;
   string   losing_candidate_ids;
   string   hidden_descendant_ids;

   // Level 11 final canonicalization state.  These fields are written only
   // after ownership and duplicate pruning. They are the final pre-render and
   // pre-export evidence for why an event is visible, hidden, repaired, or
   // invariant-failed.
   string   canonical_id;
   int      canonical_state;
   int      canonical_rank_final;
   string   canonical_conflict_group_id;
   int      canonical_invariant_flags;
   string   canonical_reason;

   FP_Node  origin;
   FP_Node  leg1;
   FP_Node  waist;
   FP_Node  leg2;
   FP_Node  confirm;
   FP_Node  invalid;
   FP_Node  extension_end;

   FP_InternalPack internal_pack;

   bool     has_origin;
   bool     has_leg1;
   bool     has_waist;
   bool     has_leg2;
   bool     has_confirm;
   bool     has_invalid;
   bool     has_extension;

   int      pos_origin;
   int      pos_leg1;
   int      pos_waist;
   int      pos_leg2;
   int      pos_confirm;
   int      pos_invalid;
   int      pos_extension_end;

   double   flag_size;
   double   parent_flag_size;
   double   size_ratio;
   int      leg1_L;
   int      parent_leg1_L;

   bool     from_phase_boundary;
   bool     from_fail_open;

   // Level 03 identity fields.
   string   structural_id;
   string   visual_id;
   string   phase_id;
   string   chain_id;
   string   audit_id;
   int      source_L;
   string   source_mode;
   bool     is_fail_open;
   int      canonical_rank_score;
   string   hidden_reason;

   bool     visible_main;
   string   reason;
};

struct FP_Config
{
   bool   include_pending_nodes;
   bool   scan_hooks;
   bool   scan_f1;
   bool   scan_f2;
   bool   scan_f3;
   bool   show_invalidated_in_audit;
   bool   keep_confirmed_f1f2_after_boundary_hit;

   bool   require_f1_phase_boundary;
   bool   allow_f1_fail_open_when_no_hook;
   bool   enforce_single_chain_per_direction_scale;
   bool   enforce_single_chain_per_direction_global;
   bool   absorb_pre_internal_extensions;
   bool   hide_superseded_parent_states;
   bool   compact_hook_rendering;
   bool   strict_main_chart_ownership;

   bool   print_ownership_sanity;
   bool   print_ownership_samples;
   int    ownership_sample_limit;
   int    ownership_score_margin;
   bool   ownership_hide_orphans;

   bool   print_canonical_sanity;
   bool   print_canonical_samples;
   int    canonical_sample_limit;
   bool   canonical_strict_invariants;
   bool   canonical_hide_unresolved_orphans;

   bool   print_hook_sanity;
   bool   print_hook_samples;
   int    hook_sample_limit;
   bool   hook_main_requires_visible_f1;
   bool   hook_keep_unseeded_visible_for_debug;

   bool   print_body_sanity;
   bool   print_body_samples;
   int    body_sample_limit;

   bool   print_internal_sanity;
   bool   print_internal_samples;
   int    internal_sample_limit;

   bool   print_f1_sanity;
   bool   print_f1_samples;
   int    f1_sample_limit;
   bool   f1_show_post_flag_candidates;
   bool   f1_show_live_body_candidates;

   bool   print_f2_sanity;
   bool   print_f2_samples;
   int    f2_sample_limit;
   bool   f2_show_size_rejected_candidates;
   bool   f2_show_post_flag_candidates;
   bool   f2_show_live_body_candidates;

   bool   print_f3_sanity;
   bool   print_f3_samples;
   int    f3_sample_limit;
   bool   f3_show_or_rejected_candidates;
   bool   f3_show_live_body_candidates;

   int    max_events;
   int    max_hooks;
   int    max_roots_per_scale_direction;
   int    render_lookback_bars;

   bool   print_node_sanity;
   bool   print_node_samples;
   int    node_sample_limit;

   double boundary_epsilon_points;
   double f2_min_parent_size_ratio;
   double f3_min_parent_size_ratio;
   double f3_leg1_L_min_ratio;
   double nd_min_retrace_ratio;
   bool   nd_allow_below_half_cycle;

   // Level 03 identity/audit context.
   string context_symbol;
   string context_timeframe;
   string identity_generation_pass;
   string identity_config_hash;
   bool   print_identity_sanity;
   bool   print_identity_samples;
   int    identity_sample_limit;

   bool   verbose_logs;
};

struct FP_DetectResult
{
   int raw_nodes_total;
   int nodes_total;
   int confirmed_nodes_total;
   int pending_nodes_total;
   int hooks_total;
   int events_total;
   int visible_events_total;
   int hidden_events_total;
   int identity_assigned_events;
   int f1_total;
   int f2_total;
   int f3_total;
   int nd_total;
   int body_attempts_total;
   int body_complete_total;
   int body_invalid_total;
   int body_extended_total;
   int body_leg1_extensions_total;
   int body_waist_deepenings_total;
   int body_leg2_equal_touches_total;
   int internal_packs_total;
   int internal_valid12_total;
   int internal_confirm_ready_total;
   int internal_invalidated_total;
   int internal_pre_extensions_total;
   int internal_f1_middle_rejected_total;
   int internal_count0_total;
   int internal_count1_total;
   int internal_count2_total;
   int internal_count3_total;
   int internal_count4_total;
   int f1_lifecycle_attempts_total;
   int f1_lifecycle_phase_attempts_total;
   int f1_lifecycle_failopen_attempts_total;
   int f1_lifecycle_gate_pass_total;
   int f1_lifecycle_gate_reject_total;
   int f1_lifecycle_body_missing_total;
   int f1_lifecycle_body_complete_total;
   int f1_lifecycle_candidate_total;
   int f1_lifecycle_post_flag_total;
   int f1_lifecycle_confirmed_total;
   int f1_lifecycle_invalidated_total;
   int f1_lifecycle_extended_total;
   int f1_lifecycle_visible_total;
   int f1_lifecycle_hidden_total;
   int f1_lifecycle_f2_ready_total;
   int f1_lifecycle_duplicate_rejected_total;
   int f1_lifecycle_emitted_roots_total;
   int f2_lifecycle_parent_attempts_total;
   int f2_lifecycle_parent_ready_total;
   int f2_lifecycle_parent_rejected_total;
   int f2_lifecycle_origin_scans_total;
   int f2_lifecycle_origin_found_total;
   int f2_lifecycle_origin_missing_total;
   int f2_lifecycle_body_missing_total;
   int f2_lifecycle_body_complete_total;
   int f2_lifecycle_size_pass_total;
   int f2_lifecycle_size_reject_total;
   int f2_lifecycle_candidate_total;
   int f2_lifecycle_post_flag_total;
   int f2_lifecycle_confirmed_total;
   int f2_lifecycle_invalidated_total;
   int f2_lifecycle_extended_total;
   int f2_lifecycle_visible_total;
   int f2_lifecycle_hidden_total;
   int f2_lifecycle_f3_ready_total;
   int f2_lifecycle_emitted_children_total;
   int f2_lifecycle_duplicate_rejected_total;
   int f3_lifecycle_parent_attempts_total;
   int f3_lifecycle_parent_ready_total;
   int f3_lifecycle_parent_rejected_total;
   int f3_lifecycle_origin_scans_total;
   int f3_lifecycle_origin_found_total;
   int f3_lifecycle_origin_missing_total;
   int f3_lifecycle_body_missing_total;
   int f3_lifecycle_body_complete_total;
   int f3_lifecycle_size_pass_total;
   int f3_lifecycle_L_pass_total;
   int f3_lifecycle_or_pass_total;
   int f3_lifecycle_or_reject_total;
   int f3_lifecycle_completed_total;
   int f3_lifecycle_locked_total;
   int f3_lifecycle_visible_total;
   int f3_lifecycle_hidden_total;
   int f3_lifecycle_emitted_children_total;
   int f3_lifecycle_duplicate_rejected_total;
   int f3_lifecycle_lock_scans_total;
   int f3_lifecycle_lock_found_total;
   int f3_lifecycle_lock_missing_total;

   int ownership_phases_total;
   int ownership_owner_roots_total;
   int ownership_competing_roots_total;
   int ownership_resets_total;
   int ownership_hidden_roots_total;
   int ownership_hidden_descendants_total;
   int ownership_orphans_hidden_total;
   int ownership_phase_safe_duplicate_hides_total;

   int canonical_visible_before_total;
   int canonical_visible_after_total;
   int canonical_hidden_before_total;
   int canonical_hidden_after_total;
   int canonical_duplicates_hidden_total;
   int canonical_orphans_hidden_total;
   int canonical_invalid_hidden_total;
   int canonical_missing_body_hidden_total;
   int canonical_hidden_reason_repaired_total;
   int canonical_parent_ids_repaired_total;
   int canonical_invariant_failures_total;
   int canonical_visible_duplicate_after_total;
   int canonical_parent_missing_after_total;

   int hook_contexts_total;
   int hook_contexts_rejected_total;
   int hook_branch_scans_total;
   int hook_branch_len5plus_total;
   int hook_retrace_rejected_total;
   int hooks_seed_visible_f1_total;

   int export_attempted_total;
   int export_ok_total;
   int export_files_written_total;
   int export_file_errors_total;
   int export_events_written_total;
   int export_visible_events_written_total;
   int export_hidden_events_written_total;
   int export_hooks_written_total;
   int export_visible_hooks_written_total;
   int export_hidden_hooks_written_total;

   int render_attempted_total;
   int render_ok_total;
   int render_objects_total;
   int render_object_errors_total;
   int render_deleted_objects_total;
   int render_events_drawn_total;
   int render_hooks_drawn_total;
   int render_event_filtered_total;
   int render_hook_filtered_total;
   int render_duplicate_names_total;
   int render_fallback_curves_total;

   int validation_attempted_total;
   int validation_ok_total;
   int validation_checks_total;
   int validation_pass_total;
   int validation_fail_total;
   int validation_warn_total;
   int validation_skipped_total;
   int validation_file_errors_total;

   int release_attempted_total;
   int release_ok_total;
   int release_gate_pass_total;
   int release_gate_fail_total;
   int release_overrides_total;
   int release_files_written_total;
   int release_file_errors_total;
   int release_cleanup_requested_total;
   int release_export_forced_total;
   int release_render_suppressed_total;
   int release_validation_forced_total;
   int release_rollback_safe_total;

   int interface_attempted_total;
   int interface_ok_total;
   int interface_checks_total;
   int interface_pass_total;
   int interface_fail_total;
   int interface_warn_total;
   int interface_skipped_total;
   int interface_file_errors_total;
   int interface_missing_ids_total;
   int interface_parent_errors_total;
   int interface_negative_counter_errors_total;
   int interface_partition_errors_total;

   int acceptance_attempted_total;
   int acceptance_ok_total;
   int acceptance_checks_total;
   int acceptance_pass_total;
   int acceptance_fail_total;
   int acceptance_warn_total;
   int acceptance_skipped_total;
   int acceptance_file_errors_total;
   int acceptance_hard_gates_total;
   int acceptance_hard_gate_fail_total;
   int acceptance_order_errors_total;
   int acceptance_dependency_errors_total;
   int acceptance_matrix_errors_total;
   int acceptance_invariant_errors_total;

   int invalid_total;
};

// ------------------------------ Reset helpers ------------------------------

void FP_ResetNode(FP_Node &n)
{
   n.id = -1;
   n.L = 0;
   n.kind = FP_NODE_NONE;
   n.index_start = -1;
   n.index_end = -1;
   n.index_anchor = -1;
   n.time_start = 0;
   n.time_end = 0;
   n.time_anchor = 0;
   n.price = 0.0;
   n.confirmed = false;
   n.is_confirmed = false;
   n.is_live_pending = false;
   n.source = 0;
   n.plateau_start_index = -1;
   n.plateau_end_index = -1;
   n.structural_id = "";
   n.visual_id = "";
   n.phase_id = "";
   n.chain_id = "";
   n.audit_id = "";
   n.source_mode = "";
   n.visible_main = true;
   n.is_fail_open = false;
   n.canonical_rank_score = 0;
   n.hidden_reason = "";
}

void FP_ResetInternalPack(FP_InternalPack &p)
{
   p.count = 0;
   FP_ResetNode(p.n1);
   FP_ResetNode(p.n2);
   FP_ResetNode(p.n3);
   FP_ResetNode(p.n4);
   FP_ResetNode(p.mid12);
   FP_ResetNode(p.mid23);
   FP_ResetNode(p.mid34);
   p.has_mid12 = false;
   p.has_mid23 = false;
   p.has_mid34 = false;
   p.valid12 = false;
   p.is_nd = false;
   p.retrace_ratio = 0.0;
   p.internal_pack_id = "";
   p.branch_id = -1;
   p.branch_id_text = "";
   p.scan_start_pos = -1;
   p.scan_end_pos = -1;
   p.first_valid12_pos = -1;
   p.has_valid12 = false;
   FP_ResetNode(p.first_valid12_node);
   FP_ResetNode(p.middle_opposite_node);
   p.has_middle_opposite_node = false;
   p.middle_opposite_breaks_leg2 = false;
   FP_ResetNode(p.pre_internal_leg2_extension_node);
   p.has_pre_internal_leg2_extension = false;
   p.pre_internal_leg2_extension_pos = -1;
   p.confirm_pos = -1;
   p.invalid_pos = -1;
   p.last_counted_pos = -1;
   p.status = "none";
   p.reason = "";
}

void FP_ResetHook(FP_HookBranch &h)
{
   h.branch_id = -1;
   h.scale_L = 0;
   h.direction = FP_DIR_NONE;
   h.status = FP_STATUS_NONE;
   h.node_count = 0;
   FP_ResetNode(h.start_node);
   FP_ResetNode(h.cycle_start_node);
   h.has_cycle_start = false;
   FP_ResetNode(h.extreme_node);
   FP_ResetNode(h.resolve_node);
   FP_ResetNode(h.n1);
   FP_ResetNode(h.n2);
   FP_ResetNode(h.n3);
   FP_ResetNode(h.n4);
   h.retrace_ratio = 0.0;
   h.is_nd = false;
   h.side_kind = FP_NODE_NONE;
   h.is_cycle_start_broken = false;
   h.max_branch_len = 0;
   h.nd_qualified = false;
   h.seeds_visible_f1 = false;
   h.structural_id = "";
   h.visual_id = "";
   h.phase_id = "";
   h.chain_id = "";
   h.audit_id = "";
   h.source_L = 0;
   h.source_mode = "";
   h.visible_main = true;
   h.is_fail_open = false;
   h.canonical_rank_score = 0;
   h.hidden_reason = "";
   h.reason = "";
}

void FP_ResetFlagEvent(FP_FlagEvent &e)
{
   e.event_id = -1;
   e.sequence_id = -1;
   e.parent_event_id = -1;
   e.parent_sequence_id = -1;
   e.chain_index = 0;
   e.scale_L = 0;
   e.direction = FP_DIR_NONE;
   e.level = FP_LEVEL_NONE;
   e.status = FP_STATUS_NONE;
   e.branch_kind = FP_BRANCH_NONE;
   e.render_kind = FP_RENDER_NONE;

   e.body_id = "";
   e.body_status = FP_BODY_NONE;
   e.origin_hit_status = 0;
   e.leg1_break_status = 0;
   e.leg2_extension_count = 0;
   e.body_scan_start_pos = -1;
   e.body_scan_end_pos = -1;
   e.body_reason = "";

   e.lifecycle_id = "";
   e.lifecycle_status = FP_F1_LC_NONE;
   e.lifecycle_stage_level = FP_LEVEL_NONE;
   e.lifecycle_phase_gate_passed = false;
   e.lifecycle_body_complete = false;
   e.lifecycle_internal_ready = false;
   e.lifecycle_can_spawn_f2 = false;
   e.lifecycle_scan_start_pos = -1;
   e.lifecycle_scan_end_pos = -1;
   e.lifecycle_reason = "";

   e.f2_lifecycle_id = "";
   e.f2_lifecycle_status = FP_F2_LC_NONE;
   e.f2_parent_ready = false;
   e.f2_origin_found = false;
   e.f2_body_complete = false;
   e.f2_size_gate_passed = false;
   e.f2_internal_ready = false;
   e.f2_can_spawn_f3 = false;
   e.f2_origin_scan_start_pos = -1;
   e.f2_lifecycle_scan_end_pos = -1;
   e.f2_parent_size_ratio = 0.0;
   e.f2_lifecycle_reason = "";

   e.f3_lifecycle_id = "";
   e.f3_lifecycle_status = FP_F3_LC_NONE;
   e.f3_parent_ready = false;
   e.f3_origin_found = false;
   e.f3_body_complete = false;
   e.f3_size_gate_passed = false;
   e.f3_leg1_L_gate_passed = false;
   e.f3_or_gate_passed = false;
   e.f3_terminal_complete = false;
   e.f3_lock_ready = false;
   e.f3_locked = false;
   e.f3_origin_scan_start_pos = -1;
   e.f3_lifecycle_scan_end_pos = -1;
   e.f3_parent_size_ratio = 0.0;
   e.f3_parent_leg1_L_ratio = 0.0;
   e.f3_lock_event_id = -1;
   e.f3_lock_reason = "";
   e.f3_lifecycle_reason = "";

   e.phase_direction = FP_DIR_NONE;
   e.phase_owner_root_id = -1;
   e.chain_state = FP_CHAIN_NONE;
   e.next_expected_f_level = FP_LEVEL_NONE;
   e.phase_reset_reason = "";
   e.owner_rank_score = 0;
   e.losing_candidate_ids = "";
   e.hidden_descendant_ids = "";

   e.canonical_id = "";
   e.canonical_state = 0;
   e.canonical_rank_final = 0;
   e.canonical_conflict_group_id = "";
   e.canonical_invariant_flags = 0;
   e.canonical_reason = "";

   FP_ResetNode(e.origin);
   FP_ResetNode(e.leg1);
   FP_ResetNode(e.waist);
   FP_ResetNode(e.leg2);
   FP_ResetNode(e.confirm);
   FP_ResetNode(e.invalid);
   FP_ResetNode(e.extension_end);
   FP_ResetInternalPack(e.internal_pack);

   e.has_origin = false;
   e.has_leg1 = false;
   e.has_waist = false;
   e.has_leg2 = false;
   e.has_confirm = false;
   e.has_invalid = false;
   e.has_extension = false;

   e.pos_origin = -1;
   e.pos_leg1 = -1;
   e.pos_waist = -1;
   e.pos_leg2 = -1;
   e.pos_confirm = -1;
   e.pos_invalid = -1;
   e.pos_extension_end = -1;

   e.flag_size = 0.0;
   e.parent_flag_size = 0.0;
   e.size_ratio = 0.0;
   e.leg1_L = 0;
   e.parent_leg1_L = 0;

   e.from_phase_boundary = false;
   e.from_fail_open = false;
   e.structural_id = "";
   e.visual_id = "";
   e.phase_id = "";
   e.chain_id = "";
   e.audit_id = "";
   e.source_L = 0;
   e.source_mode = "";
   e.is_fail_open = false;
   e.canonical_rank_score = 0;
   e.hidden_reason = "";
   e.visible_main = true;
   e.reason = "";
}

void FP_DefaultConfig(FP_Config &cfg)
{
   cfg.include_pending_nodes = false;
   cfg.scan_hooks = true;
   cfg.scan_f1 = true;
   cfg.scan_f2 = true;
   cfg.scan_f3 = true;
   cfg.show_invalidated_in_audit = false;
   cfg.keep_confirmed_f1f2_after_boundary_hit = false;

   cfg.require_f1_phase_boundary = true;
   cfg.allow_f1_fail_open_when_no_hook = true;
   cfg.enforce_single_chain_per_direction_scale = false;
   cfg.enforce_single_chain_per_direction_global = false;
   cfg.absorb_pre_internal_extensions = true;
   cfg.hide_superseded_parent_states = true;
   cfg.compact_hook_rendering = true;
   cfg.strict_main_chart_ownership = true;

   cfg.print_ownership_sanity = true;
   cfg.print_ownership_samples = false;
   cfg.ownership_sample_limit = 8;
   cfg.ownership_score_margin = 25;
   cfg.ownership_hide_orphans = true;

   cfg.print_canonical_sanity = true;
   cfg.print_canonical_samples = false;
   cfg.canonical_sample_limit = 8;
   cfg.canonical_strict_invariants = true;
   cfg.canonical_hide_unresolved_orphans = true;

   cfg.print_hook_sanity = true;
   cfg.print_hook_samples = false;
   cfg.hook_sample_limit = 6;
   cfg.hook_main_requires_visible_f1 = true;
   cfg.hook_keep_unseeded_visible_for_debug = false;

   cfg.print_body_sanity = true;
   cfg.print_body_samples = false;
   cfg.body_sample_limit = 6;

   cfg.print_internal_sanity = true;
   cfg.print_internal_samples = false;
   cfg.internal_sample_limit = 6;

   cfg.print_f1_sanity = true;
   cfg.print_f1_samples = false;
   cfg.f1_sample_limit = 6;
   cfg.f1_show_post_flag_candidates = true;
   cfg.f1_show_live_body_candidates = true;

   cfg.print_f2_sanity = true;
   cfg.print_f2_samples = false;
   cfg.f2_sample_limit = 6;
   cfg.f2_show_size_rejected_candidates = false;
   cfg.f2_show_post_flag_candidates = true;
   cfg.f2_show_live_body_candidates = true;

   cfg.print_f3_sanity = true;
   cfg.print_f3_samples = false;
   cfg.f3_sample_limit = 6;
   cfg.f3_show_or_rejected_candidates = false;
   cfg.f3_show_live_body_candidates = true;

   cfg.max_events = 6000;
   cfg.max_hooks = 6000;
   cfg.max_roots_per_scale_direction = 0;
   cfg.render_lookback_bars = 0;

   cfg.print_node_sanity = true;
   cfg.print_node_samples = false;
   cfg.node_sample_limit = 6;

   cfg.boundary_epsilon_points = 0.0;
   cfg.f2_min_parent_size_ratio = 1.0;
   cfg.f3_min_parent_size_ratio = 0.70;
   cfg.f3_leg1_L_min_ratio = 0.80;
   cfg.nd_min_retrace_ratio = 0.50;
   cfg.nd_allow_below_half_cycle = false;

   cfg.context_symbol = "";
   cfg.context_timeframe = "";
   cfg.identity_generation_pass = "phoenix_level16";
   cfg.identity_config_hash = "default";
   cfg.print_identity_sanity = true;
   cfg.print_identity_samples = false;
   cfg.identity_sample_limit = 6;

   cfg.verbose_logs = false;
}

void FP_ResetDetectResult(FP_DetectResult &r)
{
   r.raw_nodes_total = 0;
   r.nodes_total = 0;
   r.confirmed_nodes_total = 0;
   r.pending_nodes_total = 0;
   r.hooks_total = 0;
   r.events_total = 0;
   r.visible_events_total = 0;
   r.hidden_events_total = 0;
   r.identity_assigned_events = 0;
   r.f1_total = 0;
   r.f2_total = 0;
   r.f3_total = 0;
   r.nd_total = 0;
   r.body_attempts_total = 0;
   r.body_complete_total = 0;
   r.body_invalid_total = 0;
   r.body_extended_total = 0;
   r.body_leg1_extensions_total = 0;
   r.body_waist_deepenings_total = 0;
   r.body_leg2_equal_touches_total = 0;
   r.internal_packs_total = 0;
   r.internal_valid12_total = 0;
   r.internal_confirm_ready_total = 0;
   r.internal_invalidated_total = 0;
   r.internal_pre_extensions_total = 0;
   r.internal_f1_middle_rejected_total = 0;
   r.internal_count0_total = 0;
   r.internal_count1_total = 0;
   r.internal_count2_total = 0;
   r.internal_count3_total = 0;
   r.internal_count4_total = 0;
   r.f1_lifecycle_attempts_total = 0;
   r.f1_lifecycle_phase_attempts_total = 0;
   r.f1_lifecycle_failopen_attempts_total = 0;
   r.f1_lifecycle_gate_pass_total = 0;
   r.f1_lifecycle_gate_reject_total = 0;
   r.f1_lifecycle_body_missing_total = 0;
   r.f1_lifecycle_body_complete_total = 0;
   r.f1_lifecycle_candidate_total = 0;
   r.f1_lifecycle_post_flag_total = 0;
   r.f1_lifecycle_confirmed_total = 0;
   r.f1_lifecycle_invalidated_total = 0;
   r.f1_lifecycle_extended_total = 0;
   r.f1_lifecycle_visible_total = 0;
   r.f1_lifecycle_hidden_total = 0;
   r.f1_lifecycle_f2_ready_total = 0;
   r.f1_lifecycle_duplicate_rejected_total = 0;
   r.f1_lifecycle_emitted_roots_total = 0;
   r.f2_lifecycle_parent_attempts_total = 0;
   r.f2_lifecycle_parent_ready_total = 0;
   r.f2_lifecycle_parent_rejected_total = 0;
   r.f2_lifecycle_origin_scans_total = 0;
   r.f2_lifecycle_origin_found_total = 0;
   r.f2_lifecycle_origin_missing_total = 0;
   r.f2_lifecycle_body_missing_total = 0;
   r.f2_lifecycle_body_complete_total = 0;
   r.f2_lifecycle_size_pass_total = 0;
   r.f2_lifecycle_size_reject_total = 0;
   r.f2_lifecycle_candidate_total = 0;
   r.f2_lifecycle_post_flag_total = 0;
   r.f2_lifecycle_confirmed_total = 0;
   r.f2_lifecycle_invalidated_total = 0;
   r.f2_lifecycle_extended_total = 0;
   r.f2_lifecycle_visible_total = 0;
   r.f2_lifecycle_hidden_total = 0;
   r.f2_lifecycle_f3_ready_total = 0;
   r.f2_lifecycle_emitted_children_total = 0;
   r.f2_lifecycle_duplicate_rejected_total = 0;
   r.f3_lifecycle_parent_attempts_total = 0;
   r.f3_lifecycle_parent_ready_total = 0;
   r.f3_lifecycle_parent_rejected_total = 0;
   r.f3_lifecycle_origin_scans_total = 0;
   r.f3_lifecycle_origin_found_total = 0;
   r.f3_lifecycle_origin_missing_total = 0;
   r.f3_lifecycle_body_missing_total = 0;
   r.f3_lifecycle_body_complete_total = 0;
   r.f3_lifecycle_size_pass_total = 0;
   r.f3_lifecycle_L_pass_total = 0;
   r.f3_lifecycle_or_pass_total = 0;
   r.f3_lifecycle_or_reject_total = 0;
   r.f3_lifecycle_completed_total = 0;
   r.f3_lifecycle_locked_total = 0;
   r.f3_lifecycle_visible_total = 0;
   r.f3_lifecycle_hidden_total = 0;
   r.f3_lifecycle_emitted_children_total = 0;
   r.f3_lifecycle_duplicate_rejected_total = 0;
   r.f3_lifecycle_lock_scans_total = 0;
   r.f3_lifecycle_lock_found_total = 0;
   r.f3_lifecycle_lock_missing_total = 0;

   r.ownership_phases_total = 0;
   r.ownership_owner_roots_total = 0;
   r.ownership_competing_roots_total = 0;
   r.ownership_resets_total = 0;
   r.ownership_hidden_roots_total = 0;
   r.ownership_hidden_descendants_total = 0;
   r.ownership_orphans_hidden_total = 0;
   r.ownership_phase_safe_duplicate_hides_total = 0;

   r.canonical_visible_before_total = 0;
   r.canonical_visible_after_total = 0;
   r.canonical_hidden_before_total = 0;
   r.canonical_hidden_after_total = 0;
   r.canonical_duplicates_hidden_total = 0;
   r.canonical_orphans_hidden_total = 0;
   r.canonical_invalid_hidden_total = 0;
   r.canonical_missing_body_hidden_total = 0;
   r.canonical_hidden_reason_repaired_total = 0;
   r.canonical_parent_ids_repaired_total = 0;
   r.canonical_invariant_failures_total = 0;
   r.canonical_visible_duplicate_after_total = 0;
   r.canonical_parent_missing_after_total = 0;

   r.hook_contexts_total = 0;
   r.hook_contexts_rejected_total = 0;
   r.hook_branch_scans_total = 0;
   r.hook_branch_len5plus_total = 0;
   r.hook_retrace_rejected_total = 0;
   r.hooks_seed_visible_f1_total = 0;

   r.export_attempted_total = 0;
   r.export_ok_total = 0;
   r.export_files_written_total = 0;
   r.export_file_errors_total = 0;
   r.export_events_written_total = 0;
   r.export_visible_events_written_total = 0;
   r.export_hidden_events_written_total = 0;
   r.export_hooks_written_total = 0;
   r.export_visible_hooks_written_total = 0;
   r.export_hidden_hooks_written_total = 0;

   r.render_attempted_total = 0;
   r.render_ok_total = 0;
   r.render_objects_total = 0;
   r.render_object_errors_total = 0;
   r.render_deleted_objects_total = 0;
   r.render_events_drawn_total = 0;
   r.render_hooks_drawn_total = 0;
   r.render_event_filtered_total = 0;
   r.render_hook_filtered_total = 0;
   r.render_duplicate_names_total = 0;
   r.render_fallback_curves_total = 0;

   r.validation_attempted_total = 0;
   r.validation_ok_total = 0;
   r.validation_checks_total = 0;
   r.validation_pass_total = 0;
   r.validation_fail_total = 0;
   r.validation_warn_total = 0;
   r.validation_skipped_total = 0;
   r.validation_file_errors_total = 0;

   r.release_attempted_total = 0;
   r.release_ok_total = 0;
   r.release_gate_pass_total = 0;
   r.release_gate_fail_total = 0;
   r.release_overrides_total = 0;
   r.release_files_written_total = 0;
   r.release_file_errors_total = 0;
   r.release_cleanup_requested_total = 0;
   r.release_export_forced_total = 0;
   r.release_render_suppressed_total = 0;
   r.release_validation_forced_total = 0;
   r.release_rollback_safe_total = 0;

   r.interface_attempted_total = 0;
   r.interface_ok_total = 0;
   r.interface_checks_total = 0;
   r.interface_pass_total = 0;
   r.interface_fail_total = 0;
   r.interface_warn_total = 0;
   r.interface_skipped_total = 0;
   r.interface_file_errors_total = 0;
   r.interface_missing_ids_total = 0;
   r.interface_parent_errors_total = 0;
   r.interface_negative_counter_errors_total = 0;
   r.interface_partition_errors_total = 0;

   r.acceptance_attempted_total = 0;
   r.acceptance_ok_total = 0;
   r.acceptance_checks_total = 0;
   r.acceptance_pass_total = 0;
   r.acceptance_fail_total = 0;
   r.acceptance_warn_total = 0;
   r.acceptance_skipped_total = 0;
   r.acceptance_file_errors_total = 0;
   r.acceptance_hard_gates_total = 0;
   r.acceptance_hard_gate_fail_total = 0;
   r.acceptance_order_errors_total = 0;
   r.acceptance_dependency_errors_total = 0;
   r.acceptance_matrix_errors_total = 0;
   r.acceptance_invariant_errors_total = 0;

   r.invalid_total = 0;
}

// ------------------------------ String helpers -----------------------------

string FP_NodeKindName(const int kind)
{
   if(kind == FP_NODE_HIGH) return "HIGH";
   if(kind == FP_NODE_LOW)  return "LOW";
   return "NONE";
}

string FP_DirectionName(const int direction)
{
   if(direction == FP_DIR_BULLISH) return "bull";
   if(direction == FP_DIR_BEARISH) return "bear";
   return "none";
}

string FP_LevelName(const int level)
{
   if(level == FP_LEVEL_F1) return "F1";
   if(level == FP_LEVEL_F2) return "F2";
   if(level == FP_LEVEL_F3) return "F3";
   if(level == FP_LEVEL_ND) return "ND";
   return "F?";
}

string FP_StatusName(const int status)
{
   if(status == FP_STATUS_SEED)        return "seed";
   if(status == FP_STATUS_LIVE_LEG)    return "live_leg";
   if(status == FP_STATUS_LIVE_BODY)   return "live_body";
   if(status == FP_STATUS_POST_FLAG)   return "post_flag";
   if(status == FP_STATUS_QUALIFIED)   return "qualified";
   if(status == FP_STATUS_CONFIRMED)   return "confirmed";
   if(status == FP_STATUS_COMPLETED)   return "completed";
   if(status == FP_STATUS_LOCKED)      return "locked";
   if(status == FP_STATUS_INVALIDATED) return "invalidated";
   return "none";
}


string FP_OwnershipChainStateName(const int state)
{
   if(state == FP_CHAIN_F1_OWNER) return "f1_owner";
   if(state == FP_CHAIN_F2_SEARCH) return "f2_search";
   if(state == FP_CHAIN_F2_OWNER) return "f2_owner";
   if(state == FP_CHAIN_F3_SEARCH) return "f3_search";
   if(state == FP_CHAIN_F3_OWNER) return "f3_owner";
   if(state == FP_CHAIN_F3_EXTENSION) return "f3_extension";
   if(state == FP_CHAIN_LOCKED_BY_OP_F1) return "locked_by_opposite_f1";
   if(state == FP_CHAIN_RESET_ALLOWED) return "reset_allowed";
   if(state == FP_CHAIN_HIDDEN_LOSER) return "hidden_loser";
   if(state == FP_CHAIN_HIDDEN_DESCENDANT) return "hidden_descendant";
   if(state == FP_CHAIN_ORPHAN_HIDDEN) return "orphan_hidden";
   return "none";
}

string FP_BodyStatusName(const int status)
{
   if(status == FP_BODY_SEED)            return "seed";
   if(status == FP_BODY_LIVE_LEG)        return "live_leg";
   if(status == FP_BODY_LIVE_CORRECTION) return "live_correction";
   if(status == FP_BODY_COMPLETE)        return "body_complete";
   if(status == FP_BODY_EXTENDED)        return "body_extended";
   if(status == FP_BODY_INVALID)         return "invalid";
   return "none";
}


string FP_F1LifecycleStatusName(const int status)
{
   if(status == FP_F1_LC_PHASE_REJECTED) return "phase_rejected";
   if(status == FP_F1_LC_BODY_MISSING)   return "body_missing";
   if(status == FP_F1_LC_CANDIDATE)      return "candidate";
   if(status == FP_F1_LC_POST_FLAG)      return "post_flag";
   if(status == FP_F1_LC_CONFIRMED)      return "confirmed";
   if(status == FP_F1_LC_INVALIDATED)    return "invalidated";
   if(status == FP_F1_LC_EXTENDED)       return "extended";
   if(status == FP_F1_LC_HIDDEN)         return "hidden";
   return "none";
}

string FP_F2LifecycleStatusName(const int status)
{
   if(status == FP_F2_LC_PARENT_REJECTED) return "parent_rejected";
   if(status == FP_F2_LC_ORIGIN_MISSING)  return "origin_missing";
   if(status == FP_F2_LC_BODY_MISSING)    return "body_missing";
   if(status == FP_F2_LC_SIZE_REJECTED)   return "size_rejected";
   if(status == FP_F2_LC_CANDIDATE)       return "candidate";
   if(status == FP_F2_LC_POST_FLAG)       return "post_flag";
   if(status == FP_F2_LC_CONFIRMED)       return "confirmed";
   if(status == FP_F2_LC_INVALIDATED)     return "invalidated";
   if(status == FP_F2_LC_EXTENDED)        return "extended";
   if(status == FP_F2_LC_HIDDEN)          return "hidden";
   return "none";
}

string FP_F3LifecycleStatusName(const int status)
{
   if(status == FP_F3_LC_PARENT_REJECTED) return "parent_rejected";
   if(status == FP_F3_LC_ORIGIN_MISSING)  return "origin_missing";
   if(status == FP_F3_LC_BODY_MISSING)    return "body_missing";
   if(status == FP_F3_LC_OR_REJECTED)     return "or_rejected";
   if(status == FP_F3_LC_COMPLETED)       return "completed";
   if(status == FP_F3_LC_LOCKED)          return "locked";
   if(status == FP_F3_LC_HIDDEN)          return "hidden";
   return "none";
}

string FP_BoolName(const bool v)
{
   return (v ? "true" : "false");
}

// ------------------------------ Comparators --------------------------------

double FP_EpsilonPrice(const double points)
{
   return MathMax(0.0, points) * _Point;
}

bool FP_AlmostEqual(const double a, const double b, const double eps)
{
   return MathAbs(a - b) <= eps;
}

// In this contract equality never counts as break.  Price must cross strictly.
bool FP_BreaksAbove(const double price, const double boundary, const double eps)
{
   return (price > boundary + eps);
}

bool FP_BreaksBelow(const double price, const double boundary, const double eps)
{
   return (price < boundary - eps);
}

bool FP_NodeBreaksBoundary(const FP_Node &n, const int direction, const double boundary, const double eps)
{
   if(direction == FP_DIR_BULLISH)
      return (n.kind == FP_NODE_LOW && FP_BreaksBelow(n.price, boundary, eps));
   if(direction == FP_DIR_BEARISH)
      return (n.kind == FP_NODE_HIGH && FP_BreaksAbove(n.price, boundary, eps));
   return false;
}

bool FP_NodeBreaksFlagEnd(const FP_Node &n, const int direction, const double flag_end, const double eps)
{
   if(direction == FP_DIR_BULLISH)
      return (n.kind == FP_NODE_HIGH && FP_BreaksAbove(n.price, flag_end, eps));
   if(direction == FP_DIR_BEARISH)
      return (n.kind == FP_NODE_LOW && FP_BreaksBelow(n.price, flag_end, eps));
   return false;
}

int FP_OriginKindForDirection(const int direction)
{
   if(direction == FP_DIR_BULLISH) return FP_NODE_LOW;
   if(direction == FP_DIR_BEARISH) return FP_NODE_HIGH;
   return FP_NODE_NONE;
}

int FP_OppositeKind(const int kind)
{
   if(kind == FP_NODE_HIGH) return FP_NODE_LOW;
   if(kind == FP_NODE_LOW)  return FP_NODE_HIGH;
   return FP_NODE_NONE;
}

bool FP_IsMoreAdverse(const int direction, const double a, const double b, const double eps)
{
   // True if a is deeper/more adverse than b for the direction.
   if(direction == FP_DIR_BULLISH) return FP_BreaksBelow(a, b, eps);
   if(direction == FP_DIR_BEARISH) return FP_BreaksAbove(a, b, eps);
   return false;
}

bool FP_IsMoreFavorable(const int direction, const double a, const double b, const double eps)
{
   if(direction == FP_DIR_BULLISH) return FP_BreaksAbove(a, b, eps);
   if(direction == FP_DIR_BEARISH) return FP_BreaksBelow(a, b, eps);
   return false;
}

int FP_AddNode(FP_Node &arr[], const FP_Node &n)
{
   int sz = ArraySize(arr);
   ArrayResize(arr, sz + 1);
   arr[sz] = n;
   return sz;
}

int FP_AddHook(FP_HookBranch &arr[], const FP_HookBranch &h)
{
   int sz = ArraySize(arr);
   ArrayResize(arr, sz + 1);
   arr[sz] = h;
   return sz;
}

int FP_AddEvent(FP_FlagEvent &arr[], const FP_FlagEvent &e)
{
   int sz = ArraySize(arr);
   ArrayResize(arr, sz + 1);
   arr[sz] = e;
   return sz;
}

bool FP_SameNodeIdentity(const FP_Node &a, const FP_Node &b)
{
   if(a.structural_id != "" && b.structural_id != "") return (a.structural_id == b.structural_id);
   return (a.id == b.id && a.L == b.L && a.kind == b.kind && a.index_anchor == b.index_anchor && a.price == b.price);
}

bool FP_SameNodeVisualIdentity(const FP_Node &a, const FP_Node &b)
{
   if(a.visual_id != "" && b.visual_id != "") return (a.visual_id == b.visual_id);
   return (a.kind == b.kind && a.index_anchor == b.index_anchor && a.price == b.price);
}

bool FP_SameBodyIdentity(const FP_FlagEvent &a, const FP_FlagEvent &b)
{
   if(a.level != b.level) return false;
   if(a.direction != b.direction) return false;
   if(!FP_SameNodeIdentity(a.origin, b.origin)) return false;
   if(!FP_SameNodeIdentity(a.leg1, b.leg1)) return false;
   if(!FP_SameNodeIdentity(a.waist, b.waist)) return false;
   if(!FP_SameNodeIdentity(a.leg2, b.leg2)) return false;
   return true;
}

bool FP_SameBodyVisualIdentity(const FP_FlagEvent &a, const FP_FlagEvent &b)
{
   if(a.level != b.level) return false;
   if(a.direction != b.direction) return false;
   if(!FP_SameNodeVisualIdentity(a.origin, b.origin)) return false;
   if(!FP_SameNodeVisualIdentity(a.leg1, b.leg1)) return false;
   if(!FP_SameNodeVisualIdentity(a.waist, b.waist)) return false;
   if(!FP_SameNodeVisualIdentity(a.leg2, b.leg2)) return false;
   return true;
}

#endif // __FP_TYPES_MQH__
