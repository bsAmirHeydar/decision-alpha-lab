#ifndef __FP_RELEASE_TYPES_MQH__
#define __FP_RELEASE_TYPES_MQH__
#property strict

#include "FP_TimebaseTypes.mqh"
#include "FP_ExportRows.mqh"
#include "FP_RenderTypes.mqh"
#include "FP_ValidationTypes.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 14 Release / Debug / Rollback Types
// ----------------------------------------------------------------------------
// Level 14 is operational glue. It may choose safe runtime profiles and write
// release diagnostics, but it must never create or reinterpret market structure.
// ============================================================================

enum FP_ReleaseProfile
{
   FP_RELEASE_PROFILE_NORMAL        = 0,
   FP_RELEASE_PROFILE_CLEAN_MAIN    = 1,
   FP_RELEASE_PROFILE_AUDIT_EXPORT  = 2,
   FP_RELEASE_PROFILE_VALIDATION    = 3,
   FP_RELEASE_PROFILE_DEBUG_MAX     = 4,
   FP_RELEASE_PROFILE_RENDER_OFF    = 5,
   FP_RELEASE_PROFILE_SAFE_ROLLBACK = 6
};

struct FP_ReleaseConfig
{
   bool              enabled;
   FP_ReleaseProfile profile;
   string            folder;
   string            run_tag;
   bool              write_manifest;
   bool              overwrite_latest;
   bool              strict_gate;
   bool              require_validation_ok;
   bool              require_export_ok;
   bool              require_render_ok;
   bool              require_no_render_errors;
   bool              require_no_export_errors;
   bool              require_no_canonical_failures;
   bool              clean_objects_for_profile;
   bool              print_sanity;
   bool              print_samples;
   int               sample_limit;
};

struct FP_ReleaseReport
{
   bool              attempted;
   bool              ok;
   FP_ReleaseProfile profile;
   string            profile_name;
   string            folder;
   string            run_tag;
   string            manifest_file;
   bool              gate_passed;
   bool              gate_blocking;
   int               overrides_applied;
   int               files_written;
   int               file_errors;
   int               diagnostics_flags;
   int               cleanup_requested;
   int               export_forced;
   int               render_suppressed;
   int               validation_forced;
   int               rollback_safe_mode;
   int               release_checks_total;
   int               release_checks_passed;
   int               release_checks_failed;
   int               actual_events;
   int               actual_visible_events;
   int               actual_hidden_events;
   int               actual_hooks;
   int               actual_render_errors;
   int               actual_export_errors;
   int               actual_validation_failures;
   int               actual_canonical_failures;
   string            override_log;
   string            reason;
};

string FP_ReleaseProfileName(const FP_ReleaseProfile p)
{
   if(p == FP_RELEASE_PROFILE_CLEAN_MAIN)    return "clean_main";
   if(p == FP_RELEASE_PROFILE_AUDIT_EXPORT)  return "audit_export";
   if(p == FP_RELEASE_PROFILE_VALIDATION)    return "validation";
   if(p == FP_RELEASE_PROFILE_DEBUG_MAX)     return "debug_max";
   if(p == FP_RELEASE_PROFILE_RENDER_OFF)    return "render_off";
   if(p == FP_RELEASE_PROFILE_SAFE_ROLLBACK) return "safe_rollback";
   return "normal";
}

void FP_DefaultReleaseConfig(FP_ReleaseConfig &cfg)
{
   cfg.enabled = true;
   cfg.profile = FP_RELEASE_PROFILE_NORMAL;
   cfg.folder = "FlagCountingPhoenix";
   cfg.run_tag = "";
   cfg.write_manifest = true;
   cfg.overwrite_latest = true;
   cfg.strict_gate = false;
   cfg.require_validation_ok = false;
   cfg.require_export_ok = false;
   cfg.require_render_ok = true;
   cfg.require_no_render_errors = true;
   cfg.require_no_export_errors = false;
   cfg.require_no_canonical_failures = true;
   cfg.clean_objects_for_profile = true;
   cfg.print_sanity = true;
   cfg.print_samples = false;
   cfg.sample_limit = 8;
}

void FP_ResetReleaseReport(FP_ReleaseReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.profile = FP_RELEASE_PROFILE_NORMAL;
   r.profile_name = "normal";
   r.folder = "";
   r.run_tag = "";
   r.manifest_file = "";
   r.gate_passed = true;
   r.gate_blocking = false;
   r.overrides_applied = 0;
   r.files_written = 0;
   r.file_errors = 0;
   r.diagnostics_flags = 0;
   r.cleanup_requested = 0;
   r.export_forced = 0;
   r.render_suppressed = 0;
   r.validation_forced = 0;
   r.rollback_safe_mode = 0;
   r.release_checks_total = 0;
   r.release_checks_passed = 0;
   r.release_checks_failed = 0;
   r.actual_events = 0;
   r.actual_visible_events = 0;
   r.actual_hidden_events = 0;
   r.actual_hooks = 0;
   r.actual_render_errors = 0;
   r.actual_export_errors = 0;
   r.actual_validation_failures = 0;
   r.actual_canonical_failures = 0;
   r.override_log = "";
   r.reason = "not_attempted";
}

#endif // __FP_RELEASE_TYPES_MQH__
