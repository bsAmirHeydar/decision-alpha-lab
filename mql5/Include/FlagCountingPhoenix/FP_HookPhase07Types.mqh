#ifndef __FP_HOOK_PHASE07_TYPES_MQH__
#define __FP_HOOK_PHASE07_TYPES_MQH__
#property strict

#include "FP_HookPhase06Engine.mqh"

// ============================================================================
// FlagCounting Phoenix - NDS Hook Phase 07 Types
// ----------------------------------------------------------------------------
// Scope:
// - central Hook visualization/view orchestration
// - phase drawing profile control across Phase 01..Phase 06
// - optional stale Hook-object cleanup when switching view profiles
// - optional view-profile CSV audit
// - no execution, no broker request, no risk sizing, no volume sizing
// ============================================================================

#define FP_HOOK_P07_VERSION "HOOK-P07-visual-profile-orchestrator"
#define FP_HOOK_P07_SCHEMA_VERSION "hook_phase07_view_profile_v1"
#define FP_HOOK_P07_DEFAULT_FOLDER "FlagCountingPhoenix"
#define FP_HOOK_P07_DEFAULT_PREFIX "DAL_HOOK_P07_"

enum FP_HookPhase07ViewProfile
{
   FP_HOOK_P07_VIEW_KEEP_INPUTS       = 0,
   FP_HOOK_P07_VIEW_RAW_NODES         = 1,
   FP_HOOK_P07_VIEW_SEQUENCE_XY       = 2,
   FP_HOOK_P07_VIEW_LIFECYCLE         = 3,
   FP_HOOK_P07_VIEW_TYPE_QUALITY      = 4,
   FP_HOOK_P07_VIEW_QUALITY_FOCUS     = 5,
   FP_HOOK_P07_VIEW_FULL_DEBUG        = 6,
   FP_HOOK_P07_VIEW_AUDIT_EXPORT_ONLY = 7
};

struct FP_HookPhase07Config
{
   bool enabled;
   FP_NDSHookDisplayFamily display_family;
   FP_HookPhase07ViewProfile view_profile;

   bool respect_individual_phase_enabled;
   bool force_enable_required_phases;
   bool show_labels;
   bool global_export_csv;
   bool global_print_summary;
   bool global_print_samples;
   bool export_profile_csv;
   bool print_summary;
   bool clean_before_apply;
   bool clean_p01_objects;
   bool clean_p02_objects;
   bool clean_p03_objects;
   bool clean_p04_objects;
   bool clean_p05_objects;
   bool clean_p06_objects;
   bool clean_p07_objects;

   int max_nodes_to_draw;
   int max_sequences_to_draw;
   int sample_limit;

   string folder;
   string object_prefix;
};

struct FP_HookPhase07Report
{
   bool attempted;
   bool ok;
   string status;
   string reason;

   FP_NDSHookDisplayFamily display_family;
   FP_HookPhase07ViewProfile view_profile;

   bool p01_enabled;
   bool p02_enabled;
   bool p03_enabled;
   bool p04_enabled;
   bool p05_enabled;
   bool p06_enabled;

   bool p01_draw;
   bool p02_draw;
   bool p03_draw;
   bool p04_draw;
   bool p05_draw;
   bool p06_draw;

   bool p01_export;
   bool p02_export;
   bool p03_export;
   bool p04_export;
   bool p05_export;
   bool p06_export;

   int max_nodes_to_draw;
   int max_sequences_to_draw;

   int objects_deleted;
   int profiles_applied;
   int files_written;
   int file_errors;
};

string FP_HookP07BoolName(const bool v)
{
   return (v ? "true" : "false");
}

string FP_HookP07ViewProfileName(const FP_HookPhase07ViewProfile p)
{
   if(p == FP_HOOK_P07_VIEW_KEEP_INPUTS) return "KEEP_INPUTS";
   if(p == FP_HOOK_P07_VIEW_RAW_NODES) return "RAW_NODES";
   if(p == FP_HOOK_P07_VIEW_SEQUENCE_XY) return "SEQUENCE_XY";
   if(p == FP_HOOK_P07_VIEW_LIFECYCLE) return "LIFECYCLE";
   if(p == FP_HOOK_P07_VIEW_TYPE_QUALITY) return "TYPE_QUALITY";
   if(p == FP_HOOK_P07_VIEW_QUALITY_FOCUS) return "QUALITY_FOCUS";
   if(p == FP_HOOK_P07_VIEW_FULL_DEBUG) return "FULL_DEBUG";
   if(p == FP_HOOK_P07_VIEW_AUDIT_EXPORT_ONLY) return "AUDIT_EXPORT_ONLY";
   return "UNKNOWN_VIEW_PROFILE";
}

void FP_ResetHookPhase07Config(FP_HookPhase07Config &cfg)
{
   cfg.enabled = true;
   cfg.display_family = FP_NDS_HOOK_DISPLAY_RALLY_ONLY;
   cfg.view_profile = FP_HOOK_P07_VIEW_KEEP_INPUTS;

   cfg.respect_individual_phase_enabled = true;
   cfg.force_enable_required_phases = true;
   cfg.show_labels = true;
   cfg.global_export_csv = false;
   cfg.global_print_summary = false;
   cfg.global_print_samples = false;
   cfg.export_profile_csv = false;
   cfg.print_summary = false;
   cfg.clean_before_apply = false;
   cfg.clean_p01_objects = true;
   cfg.clean_p02_objects = true;
   cfg.clean_p03_objects = true;
   cfg.clean_p04_objects = true;
   cfg.clean_p05_objects = true;
   cfg.clean_p06_objects = true;
   cfg.clean_p07_objects = true;

   cfg.max_nodes_to_draw = 500;
   cfg.max_sequences_to_draw = 120;
   cfg.sample_limit = 10;

   cfg.folder = FP_HOOK_P07_DEFAULT_FOLDER;
   cfg.object_prefix = FP_HOOK_P07_DEFAULT_PREFIX;
}

void FP_ResetHookPhase07Report(FP_HookPhase07Report &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "HOOK_P07_RESET";
   r.reason = "RESET";

   r.display_family = FP_NDS_HOOK_DISPLAY_RALLY_ONLY;
   r.view_profile = FP_HOOK_P07_VIEW_KEEP_INPUTS;

   r.p01_enabled = false;
   r.p02_enabled = false;
   r.p03_enabled = false;
   r.p04_enabled = false;
   r.p05_enabled = false;
   r.p06_enabled = false;

   r.p01_draw = false;
   r.p02_draw = false;
   r.p03_draw = false;
   r.p04_draw = false;
   r.p05_draw = false;
   r.p06_draw = false;

   r.p01_export = false;
   r.p02_export = false;
   r.p03_export = false;
   r.p04_export = false;
   r.p05_export = false;
   r.p06_export = false;

   r.max_nodes_to_draw = 0;
   r.max_sequences_to_draw = 0;

   r.objects_deleted = 0;
   r.profiles_applied = 0;
   r.files_written = 0;
   r.file_errors = 0;
}

#endif // __FP_HOOK_PHASE07_TYPES_MQH__
