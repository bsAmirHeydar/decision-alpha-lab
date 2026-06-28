#ifndef __FP_RELEASE_RULES_MQH__
#define __FP_RELEASE_RULES_MQH__
#property strict

#include "FP_ReleaseTypes.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 14 Release Rules
// ----------------------------------------------------------------------------
// Pure operational profile rules. These functions may alter runtime configs but
// must never inspect or mutate event/hook structure.
// ============================================================================

void FP_ReleaseRecordOverride(FP_ReleaseReport &r, const string text)
{
   r.overrides_applied++;
   if(r.override_log == "") r.override_log = text;
   else r.override_log += ";" + text;
}

string FP_ReleaseRunTag(const FP_ReleaseConfig &cfg)
{
   if(cfg.run_tag != "") return cfg.run_tag;
   return FP_ReleaseProfileName(cfg.profile) + "_" + TimeToString(TimeCurrent(), TIME_DATE|TIME_MINUTES|TIME_SECONDS);
}

bool FP_ReleaseProfileWantsCleanup(const FP_ReleaseConfig &cfg)
{
   if(!cfg.clean_objects_for_profile) return false;
   return (cfg.profile != FP_RELEASE_PROFILE_NORMAL);
}

void FP_ReleaseForceNoRenderer(FP_RenderConfig &render_cfg, FP_ReleaseReport &r, const string reason)
{
   render_cfg.max_events_to_draw = 0;
   render_cfg.max_hooks_to_draw = 0;
   render_cfg.draw_f1 = false;
   render_cfg.draw_f2 = false;
   render_cfg.draw_f3 = false;
   render_cfg.draw_hooks = false;
   render_cfg.draw_candidates = false;
   render_cfg.draw_confirmed = false;
   render_cfg.draw_locked = false;
   render_cfg.draw_invalidated = false;
   r.render_suppressed = 1;
   FP_ReleaseRecordOverride(r, reason);
}

void FP_ReleaseApplyCleanMain(FP_Config &engine_cfg,
                              FP_RenderConfig &render_cfg,
                              FP_ReleaseReport &r)
{
   engine_cfg.strict_main_chart_ownership = true;
   engine_cfg.hook_main_requires_visible_f1 = true;
   engine_cfg.hook_keep_unseeded_visible_for_debug = false;
   engine_cfg.canonical_strict_invariants = true;
   engine_cfg.canonical_hide_unresolved_orphans = true;
   render_cfg.strict_visibility = true;
   render_cfg.use_canonical_object_names = true;
   render_cfg.delete_existing_by_prefix = true;
   render_cfg.detailed_labels = false;
   render_cfg.show_parent_ids = false;
   render_cfg.show_origin_labels = false;
   render_cfg.show_internal_labels = false;
   render_cfg.show_hook_count_labels = false;
   r.cleanup_requested = 1;
   FP_ReleaseRecordOverride(r, "clean_main_strict_visibility_and_labels");
}

void FP_ReleaseApplyDebugMax(FP_Config &engine_cfg,
                             FP_ExportConfig &export_cfg,
                             FP_RenderConfig &render_cfg,
                             FP_ValidationConfig &validation_cfg,
                             FP_ReleaseReport &r)
{
   engine_cfg.show_invalidated_in_audit = true;
   engine_cfg.hook_keep_unseeded_visible_for_debug = true;
   engine_cfg.verbose_logs = true;
   engine_cfg.print_node_samples = true;
   engine_cfg.print_identity_samples = true;
   engine_cfg.print_hook_samples = true;
   engine_cfg.print_body_samples = true;
   engine_cfg.print_internal_samples = true;
   engine_cfg.print_f1_samples = true;
   engine_cfg.print_f2_samples = true;
   engine_cfg.print_f3_samples = true;
   engine_cfg.print_ownership_samples = true;
   engine_cfg.print_canonical_samples = true;
   export_cfg.enabled = true;
   export_cfg.visible_only = false;
   export_cfg.print_samples = true;
   render_cfg.strict_visibility = false;
   render_cfg.detailed_labels = true;
   render_cfg.show_parent_ids = true;
   render_cfg.show_origin_labels = true;
   render_cfg.show_internal_labels = true;
   render_cfg.show_hook_count_labels = true;
   render_cfg.draw_invalidated = true;
   validation_cfg.enabled = true;
   validation_cfg.baseline_mode = true;
   validation_cfg.require_render_ok = false;
   r.export_forced = 1;
   r.validation_forced = 1;
   r.diagnostics_flags = 1;
   FP_ReleaseRecordOverride(r, "debug_max_samples_export_validation_audit_visibility");
}

void FP_ReleaseApplyProfile(FP_TimebaseConfig &timebase_cfg,
                            FP_Config &engine_cfg,
                            FP_ExportConfig &export_cfg,
                            FP_RenderConfig &render_cfg,
                            FP_ValidationConfig &validation_cfg,
                            const FP_ReleaseConfig &release_cfg,
                            FP_ReleaseReport &report)
{
   FP_ResetReleaseReport(report);
   report.attempted = release_cfg.enabled;
   report.profile = release_cfg.profile;
   report.profile_name = FP_ReleaseProfileName(release_cfg.profile);
   report.folder = release_cfg.folder;
   report.run_tag = FP_ReleaseRunTag(release_cfg);
   report.gate_blocking = release_cfg.strict_gate;
   report.reason = "profile_applied";

   if(!release_cfg.enabled)
   {
      report.ok = true;
      report.reason = "disabled";
      return;
   }

   if(release_cfg.profile == FP_RELEASE_PROFILE_NORMAL)
   {
      report.ok = true;
      report.reason = "normal_no_overrides";
      return;
   }

   if(release_cfg.profile == FP_RELEASE_PROFILE_CLEAN_MAIN)
   {
      FP_ReleaseApplyCleanMain(engine_cfg, render_cfg, report);
   }
   else if(release_cfg.profile == FP_RELEASE_PROFILE_AUDIT_EXPORT)
   {
      export_cfg.enabled = true;
      export_cfg.visible_only = false;
      export_cfg.print_sanity = true;
      export_cfg.print_samples = true;
      FP_ReleaseForceNoRenderer(render_cfg, report, "audit_export_renderer_suppressed");
      r.export_forced = 1;
   }
   else if(release_cfg.profile == FP_RELEASE_PROFILE_VALIDATION)
   {
      export_cfg.enabled = true;
      export_cfg.visible_only = false;
      validation_cfg.enabled = true;
      validation_cfg.baseline_mode = false;
      validation_cfg.strict = true;
      validation_cfg.require_render_ok = true;
      validation_cfg.require_no_render_errors = true;
      validation_cfg.require_no_canonical_failures = true;
      r.export_forced = 1;
      report.validation_forced = 1;
      FP_ReleaseRecordOverride(report, "validation_profile_export_validation_gate");
   }
   else if(release_cfg.profile == FP_RELEASE_PROFILE_DEBUG_MAX)
   {
      timebase_cfg.print_sanity = true;
      timebase_cfg.print_samples = true;
      FP_ReleaseApplyDebugMax(engine_cfg, export_cfg, render_cfg, validation_cfg, report);
   }
   else if(release_cfg.profile == FP_RELEASE_PROFILE_RENDER_OFF)
   {
      export_cfg.enabled = true;
      export_cfg.visible_only = false;
      validation_cfg.require_render_ok = false;
      validation_cfg.require_no_render_errors = false;
      FP_ReleaseForceNoRenderer(render_cfg, report, "render_off_profile");
      r.export_forced = 1;
   }
   else if(release_cfg.profile == FP_RELEASE_PROFILE_SAFE_ROLLBACK)
   {
      engine_cfg.scan_hooks = false;
      engine_cfg.scan_f1 = false;
      engine_cfg.scan_f2 = false;
      engine_cfg.scan_f3 = false;
      export_cfg.enabled = false;
      validation_cfg.enabled = false;
      FP_ReleaseForceNoRenderer(render_cfg, report, "safe_rollback_no_draw_no_scan");
      render_cfg.delete_existing_by_prefix = true;
      report.rollback_safe_mode = 1;
      report.cleanup_requested = 1;
      FP_ReleaseRecordOverride(report, "safe_rollback_scan_export_validation_disabled");
   }

   report.ok = true;
}

bool FP_ReleaseCheck(const bool pass, FP_ReleaseReport &r, const string fail_reason)
{
   r.release_checks_total++;
   if(pass)
   {
      r.release_checks_passed++;
      return true;
   }
   r.release_checks_failed++;
   if(r.reason == "ok" || r.reason == "profile_applied" || r.reason == "normal_no_overrides")
      r.reason = fail_reason;
   else
      r.reason += ";" + fail_reason;
   return false;
}

void FP_ReleaseFinalizeReport(const FP_ReleaseConfig &cfg,
                              const FP_DetectResult &result,
                              const FP_ExportReport &export_report,
                              const FP_RenderReport &render_report,
                              const FP_ValidationReport &validation_report,
                              FP_ReleaseReport &report)
{
   if(!cfg.enabled)
   {
      report.ok = true;
      report.reason = "disabled";
      return;
   }

   report.actual_events = result.events_total;
   report.actual_visible_events = result.visible_events_total;
   report.actual_hidden_events = result.hidden_events_total;
   report.actual_hooks = result.hooks_total;
   report.actual_render_errors = result.render_object_errors_total;
   report.actual_export_errors = result.export_file_errors_total;
   report.actual_validation_failures = result.validation_fail_total + result.validation_file_errors_total;
   report.actual_canonical_failures = result.canonical_invariant_failures_total;
   report.reason = "ok";

   bool pass = true;
   if(cfg.require_export_ok)
      pass = FP_ReleaseCheck(export_report.attempted && export_report.ok, report, "export_not_ok") && pass;
   if(cfg.require_render_ok)
      pass = FP_ReleaseCheck(render_report.attempted && render_report.ok, report, "render_not_ok") && pass;
   if(cfg.require_validation_ok)
      pass = FP_ReleaseCheck(validation_report.attempted && validation_report.ok, report, "validation_not_ok") && pass;
   if(cfg.require_no_render_errors)
      pass = FP_ReleaseCheck(result.render_object_errors_total == 0, report, "render_errors_present") && pass;
   if(cfg.require_no_export_errors)
      pass = FP_ReleaseCheck(result.export_file_errors_total == 0, report, "export_errors_present") && pass;
   if(cfg.require_no_canonical_failures)
      pass = FP_ReleaseCheck(result.canonical_invariant_failures_total == 0, report, "canonical_failures_present") && pass;

   report.gate_passed = pass;
   report.ok = pass || !cfg.strict_gate;
}

#endif // __FP_RELEASE_RULES_MQH__
