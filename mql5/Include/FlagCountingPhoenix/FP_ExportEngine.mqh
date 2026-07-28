#ifndef __FP_EXPORT_ENGINE_MQH__
#define __FP_EXPORT_ENGINE_MQH__
#property strict

#include "FP_ExportRows.mqh"
#include <AlphaLab/UC04/AL_UC04CorePrimitives.mqh>

// ============================================================================
// FlagCounting Phoenix - Level 11.5 Export Engine
// ----------------------------------------------------------------------------
// Read-only CSV export of the canonical event/hook stream. This module has no
// renderer dependency and is safe to run with chart drawing disabled.
// ============================================================================

bool FP_ExportWriteLine(const int handle, const string line)
{
   return AL_UC04WriteLine(handle, line);
}

bool FP_ExportOpenWrite(const string path, int &handle)
{
   handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
   return (handle != INVALID_HANDLE);
}

void FP_PrintExportReport(const string prefix, const FP_ExportReport &r)
{
   string msg = prefix;
   msg += " attempted=" + FP_ExportBool(r.attempted);
   msg += " ok=" + FP_ExportBool(r.ok);
   msg += " run_id=" + r.run_id;
   msg += " folder=" + r.folder;
   msg += " files=" + FP_ExportInt(r.files_written);
   msg += " errors=" + FP_ExportInt(r.file_errors);
   msg += " events_seen=" + FP_ExportInt(r.events_seen);
   msg += " events_written=" + FP_ExportInt(r.events_written);
   msg += " events_visible=" + FP_ExportInt(r.events_visible_written);
   msg += " events_hidden=" + FP_ExportInt(r.events_hidden_written);
   msg += " events_skipped_hidden=" + FP_ExportInt(r.events_skipped_hidden);
   msg += " hooks_seen=" + FP_ExportInt(r.hooks_seen);
   msg += " hooks_written=" + FP_ExportInt(r.hooks_written);
   msg += " hooks_visible=" + FP_ExportInt(r.hooks_visible_written);
   msg += " hooks_hidden=" + FP_ExportInt(r.hooks_hidden_written);
   msg += " hooks_skipped_hidden=" + FP_ExportInt(r.hooks_skipped_hidden);
   msg += " manifest=" + r.manifest_file;
   msg += " summary=" + r.summary_file;
   msg += " events=" + r.events_file;
   msg += " hooks=" + r.hooks_file;
   msg += " reason=" + r.reason;
   Print(msg);
}

void FP_PrintExportSamples(const string prefix,
                           const FP_ExportReport &r,
                           const FP_FlagEvent &events[],
                           const FP_HookBranch &hooks[],
                           const int limit)
{
   int max_rows = MathMax(0, limit);
   for(int i=0; i<ArraySize(events) && i<max_rows; i++)
   {
      Print(prefix,
            "_EVENT_SAMPLE event_id=", events[i].event_id,
            " visible=", FP_ExportBool(events[i].visible_main),
            " level=", FP_LevelName(events[i].level),
            " status=", FP_StatusName(events[i].status),
            " canonical_id=", events[i].canonical_id,
            " hidden_reason=", events[i].hidden_reason);
   }
   for(int h=0; h<ArraySize(hooks) && h<max_rows; h++)
   {
      Print(prefix,
            "_HOOK_SAMPLE branch_id=", hooks[h].branch_id,
            " visible=", FP_ExportBool(hooks[h].visible_main),
            " is_nd=", FP_ExportBool(hooks[h].is_nd),
            " seeds_f1=", FP_ExportBool(hooks[h].seeds_visible_f1),
            " structural_id=", hooks[h].structural_id,
            " hidden_reason=", hooks[h].hidden_reason);
   }
}

void FP_ExportApplyReportToResult(const FP_ExportReport &er, FP_DetectResult &r)
{
   r.export_attempted_total += (er.attempted ? 1 : 0);
   r.export_ok_total += (er.ok ? 1 : 0);
   r.export_files_written_total += er.files_written;
   r.export_file_errors_total += er.file_errors;
   r.export_events_written_total += er.events_written;
   r.export_visible_events_written_total += er.events_visible_written;
   r.export_hidden_events_written_total += er.events_hidden_written;
   r.export_hooks_written_total += er.hooks_written;
   r.export_visible_hooks_written_total += er.hooks_visible_written;
   r.export_hidden_hooks_written_total += er.hooks_hidden_written;
}

bool FP_ExportEventsCsv(const string path,
                        const string run_id,
                        const string symbol,
                        const ENUM_TIMEFRAMES period,
                        const int bars,
                        const FP_FlagEvent &events[],
                        const FP_ExportConfig &cfg,
                        FP_ExportReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_ExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";events_open_failed_" + path;
      return false;
   }

   FP_ExportWriteLine(handle, FP_ExportEventsHeader());
   int written = 0;
   for(int i=0; i<ArraySize(events); i++)
   {
      report.events_seen++;
      if(cfg.visible_only && !events[i].visible_main)
      {
         report.events_skipped_hidden++;
         continue;
      }
      if(cfg.max_events > 0 && written >= cfg.max_events) break;
      FP_ExportWriteLine(handle, FP_ExportEventRow(run_id, symbol, period, bars, events[i]));
      written++;
      report.events_written++;
      if(events[i].visible_main) report.events_visible_written++;
      else report.events_hidden_written++;
   }
   FileClose(handle);
   report.events_file = path;
   report.files_written++;
   return true;
}

bool FP_ExportHooksCsv(const string path,
                       const string run_id,
                       const string symbol,
                       const ENUM_TIMEFRAMES period,
                       const FP_HookBranch &hooks[],
                       const FP_ExportConfig &cfg,
                       FP_ExportReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_ExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";hooks_open_failed_" + path;
      return false;
   }

   FP_ExportWriteLine(handle, FP_ExportHooksHeader());
   int written = 0;
   for(int h=0; h<ArraySize(hooks); h++)
   {
      report.hooks_seen++;
      if(cfg.visible_only && !hooks[h].visible_main)
      {
         report.hooks_skipped_hidden++;
         continue;
      }
      if(cfg.max_hooks > 0 && written >= cfg.max_hooks) break;
      FP_ExportWriteLine(handle, FP_ExportHookRow(run_id, symbol, period, hooks[h]));
      written++;
      report.hooks_written++;
      if(hooks[h].visible_main) report.hooks_visible_written++;
      else report.hooks_hidden_written++;
   }
   FileClose(handle);
   report.hooks_file = path;
   report.files_written++;
   return true;
}

bool FP_ExportSummaryCsv(const string path,
                         const string run_id,
                         const string symbol,
                         const ENUM_TIMEFRAMES period,
                         const int bars,
                         const int scale_count,
                         const FP_DetectResult &result,
                         FP_ExportReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_ExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";summary_open_failed_" + path;
      return false;
   }
   FP_ExportWriteLine(handle, FP_ExportSummaryHeader());
   FP_ExportWriteLine(handle, FP_ExportSummaryRow(run_id, symbol, period, bars, scale_count, result));
   FileClose(handle);
   report.summary_file = path;
   report.summary_rows_written = 1;
   report.files_written++;
   return true;
}

void FP_ExportManifestKV(const int handle, const string key, const string value, int &rows)
{
   string line = "";
   FP_ExportCsvAppend(line, key);
   FP_ExportCsvAppend(line, value);
   FP_ExportWriteLine(handle, line);
   rows++;
}

bool FP_ExportManifestCsv(const string path,
                          const string run_id,
                          const string symbol,
                          const ENUM_TIMEFRAMES period,
                          const int bars,
                          const int scale_count,
                          const FP_Config &engine_cfg,
                          const FP_ExportConfig &export_cfg,
                          FP_ExportReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_ExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";manifest_open_failed_" + path;
      return false;
   }
   string header = "";
   FP_ExportCsvAppend(header, "key");
   FP_ExportCsvAppend(header, "value");
   FP_ExportWriteLine(handle, header);

   int rows = 0;
   FP_ExportManifestKV(handle, "run_id", run_id, rows);
   FP_ExportManifestKV(handle, "export_time", TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS), rows);
   FP_ExportManifestKV(handle, "symbol", symbol, rows);
   FP_ExportManifestKV(handle, "timeframe", EnumToString(period), rows);
   FP_ExportManifestKV(handle, "bars", FP_ExportInt(bars), rows);
   FP_ExportManifestKV(handle, "scale_count", FP_ExportInt(scale_count), rows);
   FP_ExportManifestKV(handle, "identity_pass", engine_cfg.identity_generation_pass, rows);
   FP_ExportManifestKV(handle, "identity_config_hash", engine_cfg.identity_config_hash, rows);
   FP_ExportManifestKV(handle, "visible_only", FP_ExportBool(export_cfg.visible_only), rows);
   FP_ExportManifestKV(handle, "events_file", report.events_file, rows);
   FP_ExportManifestKV(handle, "hooks_file", report.hooks_file, rows);
   FP_ExportManifestKV(handle, "summary_file", report.summary_file, rows);
   FP_ExportManifestKV(handle, "events_written", FP_ExportInt(report.events_written), rows);
   FP_ExportManifestKV(handle, "hooks_written", FP_ExportInt(report.hooks_written), rows);
   FP_ExportManifestKV(handle, "files_written_before_manifest", FP_ExportInt(report.files_written), rows);
   FP_ExportManifestKV(handle, "file_errors_before_manifest", FP_ExportInt(report.file_errors), rows);
   FileClose(handle);
   report.manifest_file = path;
   report.manifest_rows_written = rows;
   report.files_written++;
   return true;
}

bool FP_ExportAuditWithReport(const string symbol,
                              const ENUM_TIMEFRAMES period,
                              const int bars,
                              const int scale_count,
                              const FP_Config &engine_cfg,
                              const FP_ExportConfig &export_cfg,
                              const FP_FlagEvent &events[],
                              const FP_HookBranch &hooks[],
                              const FP_DetectResult &result,
                              FP_ExportReport &report)
{
   FP_ResetExportReport(report);
   report.attempted = export_cfg.enabled;
   report.folder = export_cfg.folder;

   if(!export_cfg.enabled)
   {
      report.reason = "disabled";
      return false;
   }

   FP_ExportEnsureFolder(export_cfg.folder);
   string run_id = FP_ExportRunId(symbol, period, export_cfg);
   report.run_id = run_id;
   report.reason = "ok";

   string events_path = FP_ExportJoinPath(export_cfg.folder, FP_ExportFileName(run_id, "events", export_cfg));
   string hooks_path = FP_ExportJoinPath(export_cfg.folder, FP_ExportFileName(run_id, "hooks", export_cfg));
   string summary_path = FP_ExportJoinPath(export_cfg.folder, FP_ExportFileName(run_id, "summary", export_cfg));
   string manifest_path = FP_ExportJoinPath(export_cfg.folder, FP_ExportFileName(run_id, "manifest", export_cfg));

   if(export_cfg.export_events_csv)
      FP_ExportEventsCsv(events_path, run_id, symbol, period, bars, events, export_cfg, report);
   else
      report.events_seen = ArraySize(events);

   if(export_cfg.export_hooks_csv)
      FP_ExportHooksCsv(hooks_path, run_id, symbol, period, hooks, export_cfg, report);
   else
      report.hooks_seen = ArraySize(hooks);

   if(export_cfg.export_summary_csv)
      FP_ExportSummaryCsv(summary_path, run_id, symbol, period, bars, scale_count, result, report);

   if(export_cfg.export_manifest_csv)
      FP_ExportManifestCsv(manifest_path, run_id, symbol, period, bars, scale_count, engine_cfg, export_cfg, report);

   report.ok = (report.file_errors == 0);
   if(!report.ok && report.reason == "ok") report.reason = "file_errors";
   return report.ok;
}

#endif // __FP_EXPORT_ENGINE_MQH__
