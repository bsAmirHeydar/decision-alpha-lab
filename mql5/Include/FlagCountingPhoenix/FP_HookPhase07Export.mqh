#ifndef __FP_HOOK_PHASE07_EXPORT_MQH__
#define __FP_HOOK_PHASE07_EXPORT_MQH__
#property strict

#include "FP_HookPhase07Visual.mqh"

string FP_HookP07SafeCsv(string s)
{
   StringReplace(s, "\"", "\"\"");
   return "\"" + s + "\"";
}

string FP_HookP07ProfilePath(const FP_HookPhase07Config &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P07_DEFAULT_FOLDER;
   return folder + "\\hook_phase07_view_profile.csv";
}

string FP_HookP07ProfileHeader()
{
   return "schema_version,version,display_family,view_profile,p01_enabled,p02_enabled,p03_enabled,p04_enabled,p05_enabled,p06_enabled,p01_draw,p02_draw,p03_draw,p04_draw,p05_draw,p06_draw,p01_export,p02_export,p03_export,p04_export,p05_export,p06_export,max_nodes_to_draw,max_sequences_to_draw,objects_deleted,status,reason";
}

string FP_HookP07ProfileRow(const FP_HookPhase07Report &r)
{
   string row = "";
   row += FP_HookP07SafeCsv(FP_HOOK_P07_SCHEMA_VERSION);
   row += "," + FP_HookP07SafeCsv(FP_HOOK_P07_VERSION);
   row += "," + FP_HookP07SafeCsv(FP_HookP01DisplayFamilyName(r.display_family));
   row += "," + FP_HookP07SafeCsv(FP_HookP07ViewProfileName(r.view_profile));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p01_enabled));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p02_enabled));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p03_enabled));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p04_enabled));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p05_enabled));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p06_enabled));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p01_draw));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p02_draw));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p03_draw));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p04_draw));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p05_draw));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p06_draw));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p01_export));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p02_export));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p03_export));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p04_export));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p05_export));
   row += "," + FP_HookP07SafeCsv(FP_HookP07BoolName(r.p06_export));
   row += "," + IntegerToString(r.max_nodes_to_draw);
   row += "," + IntegerToString(r.max_sequences_to_draw);
   row += "," + IntegerToString(r.objects_deleted);
   row += "," + FP_HookP07SafeCsv(r.status);
   row += "," + FP_HookP07SafeCsv(r.reason);
   return row;
}

bool FP_HookP07ExportProfile(const FP_HookPhase07Config &cfg,
                             FP_HookPhase07Report &report)
{
   if(!cfg.export_profile_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P07_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_HookP07ProfilePath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P07_PROFILE_EXPORT_OPEN_FAILED";
      return false;
   }

   FileWriteString(handle, FP_HookP07ProfileHeader() + "\r\n");
   FileWriteString(handle, FP_HookP07ProfileRow(report) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

#endif // __FP_HOOK_PHASE07_EXPORT_MQH__
