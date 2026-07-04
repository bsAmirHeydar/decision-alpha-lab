#ifndef __FP_HOOK_PHASE09_TYPES_MQH__
#define __FP_HOOK_PHASE09_TYPES_MQH__
#property strict

#include "FP_HookPhase08Engine.mqh"

// ============================================================================
// FlagCounting Phoenix - NDS Hook Phase 09 Types
// ----------------------------------------------------------------------------
// Scope:
// - visual smoke-test harness for Hook Phase 01..Phase 08
// - profile coverage checks for the currently selected Phase 07 view profile
// - chart object census by Hook object prefix
// - optional visual panel and CSV smoke artifacts
// - no execution, no broker request, no risk sizing, no volume sizing
// ============================================================================

#define FP_HOOK_P09_VERSION "HOOK-P09-visual-smoke-test-harness"
#define FP_HOOK_P09_SCHEMA_VERSION "hook_phase09_visual_smoke_v1"
#define FP_HOOK_P09_DEFAULT_FOLDER "FlagCountingPhoenix"
#define FP_HOOK_P09_DEFAULT_PREFIX "DAL_HOOK_P09_"

enum FP_HookPhase09Severity
{
   FP_HOOK_P09_SEVERITY_INFO    = 0,
   FP_HOOK_P09_SEVERITY_WARNING = 1,
   FP_HOOK_P09_SEVERITY_BLOCKER = 2
};

enum FP_HookPhase09ScenarioState
{
   FP_HOOK_P09_SCENARIO_UNKNOWN = 0,
   FP_HOOK_P09_SCENARIO_SKIPPED = 1,
   FP_HOOK_P09_SCENARIO_PASSED  = 2,
   FP_HOOK_P09_SCENARIO_FAILED  = 3
};

struct FP_HookPhase09Config
{
   bool enabled;
   FP_NDSHookDisplayFamily display_family;

   bool allow_rally_only_smoke;
   bool require_phase08_ok;
   bool require_current_profile_coverage;
   bool require_object_census;
   bool require_draw_contract_when_records_exist;
   bool require_audit_only_no_hook_draw;
   bool require_no_phase_file_errors;
   bool require_p09_panel_when_enabled;

   bool draw_panel;
   bool clean_p09_objects_before_draw;

   bool export_csv;
   bool export_scenarios_csv;
   bool export_object_census_csv;
   bool export_findings_csv;
   bool print_summary;
   bool print_samples;

   int max_warnings_allowed;
   int sample_limit;

   string folder;
   string object_prefix;

   ENUM_BASE_CORNER panel_corner;
   int panel_x;
   int panel_y;
   int panel_font_size;
   color panel_ok_color;
   color panel_warning_color;
   color panel_blocker_color;
   color panel_text_color;
};

struct FP_HookPhase09Finding
{
   string check_code;
   FP_HookPhase09Severity severity;
   bool passed;
   string scope;
   string evidence;
   string recommendation;
};

struct FP_HookPhase09ScenarioRow
{
   string scenario_code;
   string view_profile;
   bool required_for_current_profile;
   FP_HookPhase09ScenarioState state;
   bool passed;
   int expected_min_objects;
   int actual_objects;
   int records_seen;
   string evidence;
   string recommendation;
};

struct FP_HookPhase09ObjectCensusRow
{
   string phase;
   string prefix;
   bool cfg_enabled;
   bool draw_surface_enabled;
   int expected_min_objects;
   int actual_objects;
   bool passed;
   string reason;
};

struct FP_HookPhase09Report
{
   bool attempted;
   bool ok;
   string status;
   string reason;

   FP_NDSHookDisplayFamily display_family;
   FP_HookPhase07ViewProfile view_profile;

   int scenarios_total;
   int scenarios_required;
   int scenarios_passed;
   int scenarios_failed;
   int scenarios_skipped;

   int object_prefixes_checked;
   int object_prefixes_failed;
   int chart_hook_objects_seen;
   int p09_objects_deleted;
   int p09_objects_created;

   int findings_total;
   int info_count;
   int warning_count;
   int blocker_count;
   int passed_count;
   int failed_count;

   int draw_contract_checks;
   int draw_contract_failed;
   int audit_only_checks;
   int audit_only_failed;
   int phase_file_error_checks;
   int phase_file_error_failed;

   int phase08_attempted;
   bool phase08_ok;
   string phase08_status;
   string phase08_reason;

   int files_written;
   int file_errors;
};

string FP_HookP09BoolName(const bool v)
{
   return (v ? "true" : "false");
}

string FP_HookP09SeverityName(const FP_HookPhase09Severity s)
{
   if(s == FP_HOOK_P09_SEVERITY_INFO) return "INFO";
   if(s == FP_HOOK_P09_SEVERITY_WARNING) return "WARNING";
   if(s == FP_HOOK_P09_SEVERITY_BLOCKER) return "BLOCKER";
   return "UNKNOWN_SEVERITY";
}

string FP_HookP09ScenarioStateName(const FP_HookPhase09ScenarioState s)
{
   if(s == FP_HOOK_P09_SCENARIO_UNKNOWN) return "UNKNOWN";
   if(s == FP_HOOK_P09_SCENARIO_SKIPPED) return "SKIPPED";
   if(s == FP_HOOK_P09_SCENARIO_PASSED) return "PASSED";
   if(s == FP_HOOK_P09_SCENARIO_FAILED) return "FAILED";
   return "UNKNOWN_SCENARIO_STATE";
}

void FP_ResetHookPhase09Config(FP_HookPhase09Config &cfg)
{
   cfg.enabled = true;
   cfg.display_family = FP_NDS_HOOK_DISPLAY_RALLY_ONLY;

   cfg.allow_rally_only_smoke = false;
   cfg.require_phase08_ok = true;
   cfg.require_current_profile_coverage = true;
   cfg.require_object_census = true;
   cfg.require_draw_contract_when_records_exist = true;
   cfg.require_audit_only_no_hook_draw = true;
   cfg.require_no_phase_file_errors = true;
   cfg.require_p09_panel_when_enabled = true;

   cfg.draw_panel = false;
   cfg.clean_p09_objects_before_draw = true;

   cfg.export_csv = false;
   cfg.export_scenarios_csv = true;
   cfg.export_object_census_csv = true;
   cfg.export_findings_csv = true;
   cfg.print_summary = false;
   cfg.print_samples = false;

   cfg.max_warnings_allowed = 0;
   cfg.sample_limit = 20;

   cfg.folder = FP_HOOK_P09_DEFAULT_FOLDER;
   cfg.object_prefix = FP_HOOK_P09_DEFAULT_PREFIX;

   cfg.panel_corner = CORNER_RIGHT_UPPER;
   cfg.panel_x = 16;
   cfg.panel_y = 86;
   cfg.panel_font_size = 8;
   cfg.panel_ok_color = clrLime;
   cfg.panel_warning_color = clrOrange;
   cfg.panel_blocker_color = clrRed;
   cfg.panel_text_color = clrWhite;
}

void FP_ResetHookPhase09Report(FP_HookPhase09Report &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "HOOK_P09_RESET";
   r.reason = "RESET";

   r.display_family = FP_NDS_HOOK_DISPLAY_RALLY_ONLY;
   r.view_profile = FP_HOOK_P07_VIEW_KEEP_INPUTS;

   r.scenarios_total = 0;
   r.scenarios_required = 0;
   r.scenarios_passed = 0;
   r.scenarios_failed = 0;
   r.scenarios_skipped = 0;

   r.object_prefixes_checked = 0;
   r.object_prefixes_failed = 0;
   r.chart_hook_objects_seen = 0;
   r.p09_objects_deleted = 0;
   r.p09_objects_created = 0;

   r.findings_total = 0;
   r.info_count = 0;
   r.warning_count = 0;
   r.blocker_count = 0;
   r.passed_count = 0;
   r.failed_count = 0;

   r.draw_contract_checks = 0;
   r.draw_contract_failed = 0;
   r.audit_only_checks = 0;
   r.audit_only_failed = 0;
   r.phase_file_error_checks = 0;
   r.phase_file_error_failed = 0;

   r.phase08_attempted = 0;
   r.phase08_ok = false;
   r.phase08_status = "";
   r.phase08_reason = "";

   r.files_written = 0;
   r.file_errors = 0;
}

#endif // __FP_HOOK_PHASE09_TYPES_MQH__
