//+------------------------------------------------------------------+
//| CGPI_CsvInspector.mqh                                            |
//| Phase 12.5 — CSV parser, schema, keys, timestamps, metrics       |
//+------------------------------------------------------------------+
#property strict
#ifndef __CGPI_CSV_INSPECTOR_MQH__
#define __CGPI_CSV_INSPECTOR_MQH__

#include <IntermarketDivergenceExecution/CG/CGPI_Types.mqh>

class CCGPI_CsvInspector
{
private:
   bool m_common_files;

   void AddIssue(SCGPISchemaIssue &issues[],const SCGPIFileContract &c,
                 const string column,const string issue_type,
                 const ECGPISeverity severity,const string detail)
   {
      int n = ArraySize(issues);
      ArrayResize(issues,n+1);
      issues[n].phase = c.phase;
      issues[n].logical_name = c.logical_name;
      issues[n].file_name = c.file_name;
      issues[n].column_name = column;
      issues[n].issue_type = issue_type;
      issues[n].severity = severity;
      issues[n].detail = detail;
   }

   string Clean(string value)
   {
      StringTrimLeft(value);
      StringTrimRight(value);
      if(StringLen(value) >= 2 && StringSubstr(value,0,1) == "\"" && StringSubstr(value,StringLen(value)-1,1) == "\"")
         value = StringSubstr(value,1,StringLen(value)-2);
      StringReplace(value,"\"\"","\"");
      return value;
   }

   int HeaderIndex(string &headers[],const string name)
   {
      for(int i=0;i<ArraySize(headers);i++)
      {
         if(StringCompare(Clean(headers[i]),name,false) == 0)
            return i;
      }
      return -1;
   }

   void SplitPipe(const string source,string &parts[])
   {
      if(StringLen(source) == 0)
      {
         ArrayResize(parts,0);
         return;
      }
      StringSplit(source,StringGetCharacter("|",0),parts);
      for(int i=0;i<ArraySize(parts);i++) parts[i] = Clean(parts[i]);
   }

   string BuildKey(string &fields[],string &headers[],const string key_columns_pipe)
   {
      string columns[];
      SplitPipe(key_columns_pipe,columns);
      if(ArraySize(columns) == 0) return "";
      string key = "";
      for(int i=0;i<ArraySize(columns);i++)
      {
         int idx = HeaderIndex(headers,columns[i]);
         string value = (idx >= 0 && idx < ArraySize(fields)) ? Clean(fields[idx]) : "";
         if(i > 0) key += "||";
         key += value;
      }
      return key;
   }

   bool IsEmptyCompositeKey(const string key)
   {
      if(StringLen(key) == 0) return true;
      string tmp = key;
      StringReplace(tmp,"|","");
      StringReplace(tmp," ","");
      return StringLen(tmp) == 0;
   }

   int CountDuplicates(string &keys[])
   {
      if(ArraySize(keys) <= 1) return 0;
      ArraySort(keys);
      int duplicates = 0;
      for(int i=1;i<ArraySize(keys);i++)
         if(keys[i] == keys[i-1]) duplicates++;
      return duplicates;
   }

public:
   void Setup(const bool common_files) { m_common_files = common_files; }

   int ParseCsvLine(const string line,string &fields[])
   {
      ArrayResize(fields,0);
      string current = "";
      bool in_quotes = false;
      int len = StringLen(line);
      for(int i=0;i<len;i++)
      {
         ushort ch = StringGetCharacter(line,i);
         if(ch == 34)
         {
            if(in_quotes && i+1 < len && StringGetCharacter(line,i+1) == 34)
            {
               current += "\"";
               i++;
            }
            else in_quotes = !in_quotes;
         }
         else if(ch == 44 && !in_quotes)
         {
            int n = ArraySize(fields);
            ArrayResize(fields,n+1);
            fields[n] = current;
            current = "";
         }
         else current += ShortToString(ch);
      }
      int n = ArraySize(fields);
      ArrayResize(fields,n+1);
      fields[n] = current;
      return ArraySize(fields);
   }

   bool ReadHeader(const string file_name,string &headers[],string &diagnostic)
   {
      diagnostic = "";
      int h = FileOpen(file_name,CGPI_ReadFlags(m_common_files));
      if(h == INVALID_HANDLE)
      {
         diagnostic = "cannot_open:" + file_name + ":error=" + IntegerToString(GetLastError());
         ArrayResize(headers,0);
         return false;
      }
      if(FileIsEnding(h))
      {
         diagnostic = "empty_file:" + file_name;
         FileClose(h);
         ArrayResize(headers,0);
         return false;
      }
      string line = FileReadString(h);
      FileClose(h);
      ParseCsvLine(line,headers);
      for(int i=0;i<ArraySize(headers);i++) headers[i] = Clean(headers[i]);
      return ArraySize(headers) > 0;
   }

   bool Inspect(const SCGPIFileContract &contract,const SCGPIConfig &cfg,
                SCGPIFileAuditRow &audit,SCGPISchemaIssue &issues[],string &diagnostics[])
   {
      audit.phase = contract.phase;
      audit.logical_name = contract.logical_name;
      audit.file_name = contract.file_name;
      audit.required = contract.required;
      audit.exists = FileIsExist(contract.file_name,CGPI_FileScopeFlag(m_common_files));
      audit.row_count = 0;
      audit.inspected_rows = 0;
      audit.column_count = 0;
      audit.missing_required_columns = 0;
      audit.empty_primary_keys = 0;
      audit.duplicate_primary_keys = 0;
      audit.timestamp_parse_failures = 0;
      audit.timestamp_out_of_order = 0;
      audit.inspection_truncated = false;
      audit.status = "started";
      audit.notes = "";

      if(!audit.exists)
      {
         audit.status = contract.required ? "MISSING_REQUIRED" : "MISSING_OPTIONAL";
         audit.notes = "file_not_found";
         AddIssue(issues,contract,"","missing_file",contract.missing_file_severity,"Expected pipeline file does not exist.");
         return false;
      }

      int h = FileOpen(contract.file_name,CGPI_ReadFlags(m_common_files));
      if(h == INVALID_HANDLE)
      {
         audit.status = "OPEN_FAILED";
         audit.notes = "error=" + IntegerToString(GetLastError());
         AddIssue(issues,contract,"","open_failed",CGPI_SEVERITY_CRITICAL,audit.notes);
         return false;
      }
      if(FileIsEnding(h))
      {
         FileClose(h);
         audit.status = "EMPTY_FILE";
         AddIssue(issues,contract,"","empty_file",CGPI_SEVERITY_CRITICAL,"File exists but has no header.");
         return false;
      }

      string header_line = FileReadString(h);
      string headers[];
      ParseCsvLine(header_line,headers);
      for(int i=0;i<ArraySize(headers);i++) headers[i] = Clean(headers[i]);
      audit.column_count = ArraySize(headers);

      if(audit.column_count < contract.minimum_columns)
      {
         AddIssue(issues,contract,"","column_count_below_contract",CGPI_SEVERITY_ERROR,
                  "actual="+IntegerToString(audit.column_count)+" minimum="+IntegerToString(contract.minimum_columns));
      }

      if(cfg.enable_schema_audit)
      {
         string required_columns[];
         SplitPipe(contract.required_columns_pipe,required_columns);
         for(int i=0;i<ArraySize(required_columns);i++)
         {
            if(HeaderIndex(headers,required_columns[i]) < 0)
            {
               audit.missing_required_columns++;
               AddIssue(issues,contract,required_columns[i],"missing_required_column",CGPI_SEVERITY_CRITICAL,
                        "Required column absent from CSV header.");
            }
         }
      }

      int ts_idx = StringLen(contract.timestamp_column) > 0 ? HeaderIndex(headers,contract.timestamp_column) : -1;
      datetime previous_time = 0;
      string keys[];
      int row_limit = MathMax(cfg.max_rows_to_inspect_per_file,1);

      while(!FileIsEnding(h))
      {
         string line = FileReadString(h);
         if(StringLen(line) == 0) continue;
         audit.row_count++;
         if(audit.inspected_rows >= row_limit)
         {
            audit.inspection_truncated = true;
            continue;
         }
         audit.inspected_rows++;
         string fields[];
         ParseCsvLine(line,fields);

         if(cfg.enable_primary_key_audit && StringLen(contract.primary_key_columns_pipe) > 0)
         {
            string key = BuildKey(fields,headers,contract.primary_key_columns_pipe);
            if(IsEmptyCompositeKey(key)) audit.empty_primary_keys++;
            else
            {
               int n = ArraySize(keys);
               ArrayResize(keys,n+1);
               keys[n] = key;
            }
         }

         if(cfg.enable_temporal_audit && ts_idx >= 0 && ts_idx < ArraySize(fields))
         {
            string text = Clean(fields[ts_idx]);
            if(StringLen(text) > 0)
            {
               datetime t = StringToTime(text);
               if(t <= 0) audit.timestamp_parse_failures++;
               else
               {
                  if(previous_time > 0 && t < previous_time) audit.timestamp_out_of_order++;
                  previous_time = t;
               }
            }
         }
      }
      FileClose(h);

      audit.duplicate_primary_keys = CountDuplicates(keys);
      if(audit.empty_primary_keys > 0)
         AddIssue(issues,contract,contract.primary_key_columns_pipe,"empty_primary_key",CGPI_SEVERITY_CRITICAL,
                  "count="+IntegerToString(audit.empty_primary_keys));
      if(audit.duplicate_primary_keys > 0)
         AddIssue(issues,contract,contract.primary_key_columns_pipe,"duplicate_primary_key",CGPI_SEVERITY_CRITICAL,
                  "duplicate_occurrences="+IntegerToString(audit.duplicate_primary_keys));
      if(audit.timestamp_parse_failures > 0)
         AddIssue(issues,contract,contract.timestamp_column,"timestamp_parse_failure",CGPI_SEVERITY_ERROR,
                  "count="+IntegerToString(audit.timestamp_parse_failures));
      if(audit.timestamp_out_of_order > 0)
         AddIssue(issues,contract,contract.timestamp_column,"timestamp_out_of_order",CGPI_SEVERITY_WARNING,
                  "count="+IntegerToString(audit.timestamp_out_of_order)+"; row order is not chronological");
      if(audit.inspection_truncated)
         audit.notes += "inspection_truncated_at="+IntegerToString(row_limit)+";";

      if(audit.missing_required_columns > 0 || audit.empty_primary_keys > 0 || audit.duplicate_primary_keys > 0)
         audit.status = "FAILED";
      else if(audit.timestamp_parse_failures > 0 || audit.timestamp_out_of_order > 0 || audit.inspection_truncated)
         audit.status = "WARNING";
      else audit.status = "OK";
      return true;
   }

   bool LoadUniqueKeys(const string file_name,const string key_columns_pipe,const int max_rows,
                       string &unique_keys[],int &rows_read,int &empty_keys,int &duplicate_keys,
                       string &diagnostic)
   {
      ArrayResize(unique_keys,0);
      rows_read = 0;
      empty_keys = 0;
      duplicate_keys = 0;
      diagnostic = "";
      int h = FileOpen(file_name,CGPI_ReadFlags(m_common_files));
      if(h == INVALID_HANDLE)
      {
         diagnostic = "cannot_open_for_keys:"+file_name;
         return false;
      }
      if(FileIsEnding(h)) { FileClose(h); diagnostic="empty_file:"+file_name; return false; }
      string headers[];
      ParseCsvLine(FileReadString(h),headers);
      for(int i=0;i<ArraySize(headers);i++) headers[i]=Clean(headers[i]);

      string key_columns[];
      SplitPipe(key_columns_pipe,key_columns);
      for(int i=0;i<ArraySize(key_columns);i++)
      {
         if(HeaderIndex(headers,key_columns[i]) < 0)
         {
            FileClose(h);
            diagnostic = "missing_key_column:"+file_name+":"+key_columns[i];
            return false;
         }
      }

      string raw_keys[];
      while(!FileIsEnding(h) && rows_read < MathMax(max_rows,1))
      {
         string line = FileReadString(h);
         if(StringLen(line) == 0) continue;
         rows_read++;
         string fields[];
         ParseCsvLine(line,fields);
         string key = BuildKey(fields,headers,key_columns_pipe);
         if(IsEmptyCompositeKey(key)) empty_keys++;
         else
         {
            int n=ArraySize(raw_keys);
            ArrayResize(raw_keys,n+1);
            raw_keys[n]=key;
         }
      }
      FileClose(h);
      if(ArraySize(raw_keys) == 0) return true;
      ArraySort(raw_keys);
      for(int i=0;i<ArraySize(raw_keys);i++)
      {
         if(i>0 && raw_keys[i] == raw_keys[i-1])
         {
            duplicate_keys++;
            continue;
         }
         int n=ArraySize(unique_keys);
         ArrayResize(unique_keys,n+1);
         unique_keys[n]=raw_keys[i];
      }
      return true;
   }

   bool ReadMetricValue(const string file_name,const string metric_name,double &value,string &diagnostic)
   {
      value = 0.0;
      diagnostic = "";
      int h=FileOpen(file_name,CGPI_ReadFlags(m_common_files));
      if(h==INVALID_HANDLE) { diagnostic="cannot_open_metric_file:"+file_name; return false; }
      if(FileIsEnding(h)) { FileClose(h); diagnostic="empty_metric_file:"+file_name; return false; }
      string headers[];
      ParseCsvLine(FileReadString(h),headers);
      for(int i=0;i<ArraySize(headers);i++) headers[i]=Clean(headers[i]);
      int metric_idx=HeaderIndex(headers,"metric");
      int value_idx=HeaderIndex(headers,"value");
      if(metric_idx<0 || value_idx<0) { FileClose(h); diagnostic="metric_value_columns_missing:"+file_name; return false; }
      while(!FileIsEnding(h))
      {
         string line=FileReadString(h);
         if(StringLen(line)==0) continue;
         string fields[]; ParseCsvLine(line,fields);
         if(metric_idx<ArraySize(fields) && value_idx<ArraySize(fields) && Clean(fields[metric_idx])==metric_name)
         {
            value=StringToDouble(Clean(fields[value_idx]));
            FileClose(h);
            return true;
         }
      }
      FileClose(h);
      diagnostic="metric_not_found:"+file_name+":"+metric_name;
      return false;
   }

   bool ReadFirstNumericColumnValue(const string file_name,const string column_name,double &value,string &diagnostic)
   {
      value=0.0; diagnostic="";
      int h=FileOpen(file_name,CGPI_ReadFlags(m_common_files));
      if(h==INVALID_HANDLE) { diagnostic="cannot_open_column_file:"+file_name; return false; }
      if(FileIsEnding(h)) { FileClose(h); diagnostic="empty_file:"+file_name; return false; }
      string headers[]; ParseCsvLine(FileReadString(h),headers);
      for(int i=0;i<ArraySize(headers);i++) headers[i]=Clean(headers[i]);
      int idx=HeaderIndex(headers,column_name);
      if(idx<0) { FileClose(h); diagnostic="column_not_found:"+file_name+":"+column_name; return false; }
      while(!FileIsEnding(h))
      {
         string line=FileReadString(h); if(StringLen(line)==0) continue;
         string fields[]; ParseCsvLine(line,fields);
         if(idx<ArraySize(fields)) { value=StringToDouble(Clean(fields[idx])); FileClose(h); return true; }
      }
      FileClose(h); diagnostic="no_data_rows:"+file_name; return false;
   }

   int CountRowsWhere(const string file_name,const string column_name,const string expected_value,string &diagnostic)
   {
      diagnostic="";
      int h=FileOpen(file_name,CGPI_ReadFlags(m_common_files));
      if(h==INVALID_HANDLE) { diagnostic="cannot_open_count_file:"+file_name; return -1; }
      if(FileIsEnding(h)) { FileClose(h); diagnostic="empty_file:"+file_name; return -1; }
      string headers[]; ParseCsvLine(FileReadString(h),headers);
      for(int i=0;i<ArraySize(headers);i++) headers[i]=Clean(headers[i]);
      int idx=HeaderIndex(headers,column_name);
      if(idx<0) { FileClose(h); diagnostic="count_column_missing:"+file_name+":"+column_name; return -1; }
      int count=0;
      while(!FileIsEnding(h))
      {
         string line=FileReadString(h); if(StringLen(line)==0) continue;
         string fields[]; ParseCsvLine(line,fields);
         if(idx<ArraySize(fields) && StringCompare(Clean(fields[idx]),expected_value,false)==0) count++;
      }
      FileClose(h); return count;
   }
};

#endif
//+------------------------------------------------------------------+
