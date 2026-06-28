#ifndef __FP_EXPORT_TYPES_MQH__
#define __FP_EXPORT_TYPES_MQH__
#property strict

#include "FP_Types.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 11.5 Export Types
// ----------------------------------------------------------------------------
// Raw audit export is a read-only layer that serializes the canonical engine
// stream after Level 11 and before Level 12 renderer inspection.  It must never
// mutate events, hooks, identity, visibility, parent links, or chart objects.
// ============================================================================

struct FP_ExportConfig
{
   bool   enabled;
   bool   export_events_csv;
   bool   export_hooks_csv;
   bool   export_summary_csv;
   bool   export_manifest_csv;
   bool   visible_only;
   bool   overwrite_latest;
   string folder;
   string run_tag;
   int    max_events;
   int    max_hooks;
   bool   print_sanity;
   bool   print_samples;
   int    sample_limit;
};

struct FP_ExportReport
{
   bool   attempted;
   bool   ok;
   string run_id;
   string folder;
   string manifest_file;
   string summary_file;
   string events_file;
   string hooks_file;
   int    files_written;
   int    file_errors;
   int    events_seen;
   int    events_written;
   int    events_visible_written;
   int    events_hidden_written;
   int    events_skipped_hidden;
   int    hooks_seen;
   int    hooks_written;
   int    hooks_visible_written;
   int    hooks_hidden_written;
   int    hooks_skipped_hidden;
   int    summary_rows_written;
   int    manifest_rows_written;
   string reason;
};

void FP_DefaultExportConfig(FP_ExportConfig &cfg)
{
   cfg.enabled = false;
   cfg.export_events_csv = true;
   cfg.export_hooks_csv = true;
   cfg.export_summary_csv = true;
   cfg.export_manifest_csv = true;
   cfg.visible_only = false;
   cfg.overwrite_latest = true;
   cfg.folder = "FlagCountingPhoenix";
   cfg.run_tag = "";
   cfg.max_events = 0;
   cfg.max_hooks = 0;
   cfg.print_sanity = true;
   cfg.print_samples = false;
   cfg.sample_limit = 5;
}

void FP_ResetExportReport(FP_ExportReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.run_id = "";
   r.folder = "";
   r.manifest_file = "";
   r.summary_file = "";
   r.events_file = "";
   r.hooks_file = "";
   r.files_written = 0;
   r.file_errors = 0;
   r.events_seen = 0;
   r.events_written = 0;
   r.events_visible_written = 0;
   r.events_hidden_written = 0;
   r.events_skipped_hidden = 0;
   r.hooks_seen = 0;
   r.hooks_written = 0;
   r.hooks_visible_written = 0;
   r.hooks_hidden_written = 0;
   r.hooks_skipped_hidden = 0;
   r.summary_rows_written = 0;
   r.manifest_rows_written = 0;
   r.reason = "not_attempted";
}

#endif // __FP_EXPORT_TYPES_MQH__
