//+------------------------------------------------------------------+
//| CGP13_FileInventory.mqh                                          |
//| Phase 13 — Terminal-side file and readiness inspection           |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGP13_FILE_INVENTORY_MQH__
#define __CGP13_FILE_INVENTORY_MQH__

#include <IntermarketDivergenceExecution/CG/CGP13_Types.mqh>

class CCGP13_FileInventory
{
private:
   bool HasText(string value)
   {
      StringTrimLeft(value);
      StringTrimRight(value);
      return StringLen(value)>0;
   }

   int CountColumns(const string header)
   {
      if(StringLen(header)==0) return 0;
      int count=1;
      bool quoted=false;
      for(int i=0;i<StringLen(header);i++)
      {
         ushort c=StringGetCharacter(header,i);
         if(c=='\"') quoted=!quoted;
         else if(c==',' && !quoted) count++;
      }
      return count;
   }

   void InspectTextFile(SCGP13FileRow &row)
   {
      row.exists=FileIsExist(row.file_name);
      row.size_bytes=0;
      row.row_count=0;
      row.column_count=0;
      if(!row.exists)
      {
         row.status=row.required ? "MISSING_REQUIRED" : "MISSING_OPTIONAL";
         row.note="File not present in terminal Files/Common path selected by runtime.";
         return;
      }

      int h=FileOpen(row.file_name,FILE_READ|FILE_TXT|FILE_ANSI);
      if(h==INVALID_HANDLE)
      {
         row.status="UNREADABLE";
         row.note="File exists but FileOpen failed.";
         return;
      }
      row.size_bytes=(long)FileSize(h);
      bool first=true;
      while(!FileIsEnding(h))
      {
         string line=FileReadString(h);
         if(first)
         {
            row.column_count=CountColumns(line);
            first=false;
         }
         else if(HasText(line))
            row.row_count++;
      }
      FileClose(h);
      row.status=(row.row_count>0 ? "PRESENT" : "EMPTY");
      row.note=(row.row_count>0 ? "Visible to terminal-side Phase 13 bridge." : "Header-only or empty file.");
   }

   string ReadMetricValue(const string file_name,const string metric_name)
   {
      int h=FileOpen(file_name,FILE_READ|FILE_CSV|FILE_ANSI,',');
      if(h==INVALID_HANDLE) return "";
      if(!FileIsEnding(h)) { FileReadString(h); FileReadString(h); }
      while(!FileIsEnding(h))
      {
         string key=FileReadString(h);
         string value=FileReadString(h);
         if(key==metric_name) { FileClose(h); return value; }
      }
      FileClose(h);
      return "";
   }

public:
   void AddAndInspect(SCGP13FileRow &rows[],const string stage,const string logical_name,const string file_name,const bool required)
   {
      int n=ArraySize(rows);
      ArrayResize(rows,n+1);
      rows[n].stage=stage;
      rows[n].logical_name=logical_name;
      rows[n].file_name=file_name;
      rows[n].required=required;
      InspectTextFile(rows[n]);
   }

   string ReadIntegrityStatus(const string readiness_file)
   {
      if(!FileIsExist(readiness_file)) return "MISSING";
      string v=ReadMetricValue(readiness_file,"status");
      if(StringLen(v)==0) v=ReadMetricValue(readiness_file,"readiness_status");
      if(StringLen(v)==0) return "UNKNOWN";
      return v;
   }

   bool PythonRunAllowed(const string status,const bool require_gate,const bool allow_warnings)
   {
      if(!require_gate) return true;
      if(status=="READY_FOR_PHASE13") return true;
      if(allow_warnings && status=="READY_WITH_WARNINGS") return true;
      return false;
   }
};

#endif
