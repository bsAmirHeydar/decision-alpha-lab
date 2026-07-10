//+------------------------------------------------------------------+
//| CGPI_Ledger.mqh                                                  |
//| Phase 12.5 — Integrity audit output writers                      |
//+------------------------------------------------------------------+
#property strict
#ifndef __CGPI_LEDGER_MQH__
#define __CGPI_LEDGER_MQH__

#include <IntermarketDivergenceExecution/CG/CGPI_Types.mqh>

class CCGPI_Ledger
{
private:
   bool m_common_files;

   int OpenWrite(const string file_name)
   {
      return FileOpen(file_name,CGPI_WriteFlags(m_common_files));
   }

   void MaybeDelete(const string file_name,const bool clear)
   {
      if(clear && FileIsExist(file_name,CGPI_FileScopeFlag(m_common_files)))
         FileDelete(file_name,CGPI_FileScopeFlag(m_common_files));
   }

public:
   void Setup(const bool common_files) { m_common_files=common_files; }

   bool WriteFileAudit(const string file_name,const bool clear,SCGPIFileAuditRow &rows[])
   {
      MaybeDelete(file_name,clear); int h=OpenWrite(file_name); if(h==INVALID_HANDLE) return false;
      FileWriteString(h,"phase,logical_name,file_name,required,exists,row_count,inspected_rows,column_count,missing_required_columns,empty_primary_keys,duplicate_primary_keys,timestamp_parse_failures,timestamp_out_of_order,inspection_truncated,status,notes\r\n");
      for(int i=0;i<ArraySize(rows);i++)
      {
         SCGPIFileAuditRow r=rows[i];
         FileWriteString(h,CGPI_CsvEscape(r.phase)+","+CGPI_CsvEscape(r.logical_name)+","+CGPI_CsvEscape(r.file_name)+","+
            CGPI_BoolText(r.required)+","+CGPI_BoolText(r.exists)+","+IntegerToString(r.row_count)+","+IntegerToString(r.inspected_rows)+","+
            IntegerToString(r.column_count)+","+IntegerToString(r.missing_required_columns)+","+IntegerToString(r.empty_primary_keys)+","+
            IntegerToString(r.duplicate_primary_keys)+","+IntegerToString(r.timestamp_parse_failures)+","+IntegerToString(r.timestamp_out_of_order)+","+
            CGPI_BoolText(r.inspection_truncated)+","+CGPI_CsvEscape(r.status)+","+CGPI_CsvEscape(r.notes)+"\r\n");
      }
      FileClose(h); return true;
   }

   bool WriteSchemaIssues(const string file_name,const bool clear,SCGPISchemaIssue &rows[])
   {
      MaybeDelete(file_name,clear); int h=OpenWrite(file_name); if(h==INVALID_HANDLE) return false;
      FileWriteString(h,"phase,logical_name,file_name,column_name,issue_type,severity,detail\r\n");
      for(int i=0;i<ArraySize(rows);i++)
         FileWriteString(h,CGPI_CsvEscape(rows[i].phase)+","+CGPI_CsvEscape(rows[i].logical_name)+","+CGPI_CsvEscape(rows[i].file_name)+","+
            CGPI_CsvEscape(rows[i].column_name)+","+CGPI_CsvEscape(rows[i].issue_type)+","+CGPI_CsvEscape(CGPI_SeverityText(rows[i].severity))+","+
            CGPI_CsvEscape(rows[i].detail)+"\r\n");
      FileClose(h); return true;
   }

   bool WriteReconciliation(const string file_name,const bool clear,SCGPIReconciliationRow &rows[])
   {
      MaybeDelete(file_name,clear); int h=OpenWrite(file_name); if(h==INVALID_HANDLE) return false;
      FileWriteString(h,"relation_name,relation_mode,parent_file,parent_key,child_file,child_key,parent_unique_keys,child_unique_keys,matched_keys,missing_in_child,orphan_in_child,parent_coverage_percent,child_coverage_percent,status,notes\r\n");
      for(int i=0;i<ArraySize(rows);i++)
      {
         SCGPIReconciliationRow r=rows[i];
         FileWriteString(h,CGPI_CsvEscape(r.relation_name)+","+CGPI_CsvEscape(CGPI_RelationModeText(r.relation_mode))+","+
            CGPI_CsvEscape(r.parent_file)+","+CGPI_CsvEscape(r.parent_key)+","+CGPI_CsvEscape(r.child_file)+","+CGPI_CsvEscape(r.child_key)+","+
            IntegerToString(r.parent_unique_keys)+","+IntegerToString(r.child_unique_keys)+","+IntegerToString(r.matched_keys)+","+
            IntegerToString(r.missing_in_child)+","+IntegerToString(r.orphan_in_child)+","+DoubleToString(r.parent_coverage_percent,4)+","+
            DoubleToString(r.child_coverage_percent,4)+","+CGPI_CsvEscape(r.status)+","+CGPI_CsvEscape(r.notes)+"\r\n");
      }
      FileClose(h); return true;
   }

   bool WriteMetrics(const string file_name,const bool clear,SCGPIMetricCheck &rows[])
   {
      MaybeDelete(file_name,clear); int h=OpenWrite(file_name); if(h==INVALID_HANDLE) return false;
      FileWriteString(h,"check_name,left_file,left_metric,left_value,right_file,right_metric,right_value,delta,tolerance,status,notes\r\n");
      for(int i=0;i<ArraySize(rows);i++)
      {
         SCGPIMetricCheck r=rows[i];
         FileWriteString(h,CGPI_CsvEscape(r.check_name)+","+CGPI_CsvEscape(r.left_file)+","+CGPI_CsvEscape(r.left_metric)+","+
            DoubleToString(r.left_value,6)+","+CGPI_CsvEscape(r.right_file)+","+CGPI_CsvEscape(r.right_metric)+","+DoubleToString(r.right_value,6)+","+
            DoubleToString(r.delta,6)+","+DoubleToString(r.tolerance,6)+","+CGPI_CsvEscape(r.status)+","+CGPI_CsvEscape(r.notes)+"\r\n");
      }
      FileClose(h); return true;
   }

   bool WriteGates(const string file_name,const bool clear,SCGPIReadinessGate &rows[])
   {
      MaybeDelete(file_name,clear); int h=OpenWrite(file_name); if(h==INVALID_HANDLE) return false;
      FileWriteString(h,"gate_name,required,passed,severity,evidence,remediation\r\n");
      for(int i=0;i<ArraySize(rows);i++)
         FileWriteString(h,CGPI_CsvEscape(rows[i].gate_name)+","+CGPI_BoolText(rows[i].required)+","+CGPI_BoolText(rows[i].passed)+","+
            CGPI_CsvEscape(CGPI_SeverityText(rows[i].severity))+","+CGPI_CsvEscape(rows[i].evidence)+","+CGPI_CsvEscape(rows[i].remediation)+"\r\n");
      FileClose(h); return true;
   }

   bool WriteSummary(const string file_name,const bool clear,const SCGPIRunStats &s)
   {
      MaybeDelete(file_name,clear); int h=OpenWrite(file_name); if(h==INVALID_HANDLE) return false;
      FileWriteString(h,"metric,value\r\n");
      FileWriteString(h,"readiness_status,"+CGPI_CsvEscape(s.readiness_status)+"\r\n");
      FileWriteString(h,"contracts_total,"+IntegerToString(s.contracts_total)+"\r\n");
      FileWriteString(h,"required_files,"+IntegerToString(s.required_files)+"\r\n");
      FileWriteString(h,"files_found,"+IntegerToString(s.files_found)+"\r\n");
      FileWriteString(h,"files_missing,"+IntegerToString(s.files_missing)+"\r\n");
      FileWriteString(h,"schema_issues,"+IntegerToString(s.schema_issues)+"\r\n");
      FileWriteString(h,"critical_schema_issues,"+IntegerToString(s.critical_schema_issues)+"\r\n");
      FileWriteString(h,"duplicate_primary_keys,"+IntegerToString(s.duplicate_primary_keys)+"\r\n");
      FileWriteString(h,"empty_primary_keys,"+IntegerToString(s.empty_primary_keys)+"\r\n");
      FileWriteString(h,"lineage_checks,"+IntegerToString(s.lineage_checks)+"\r\n");
      FileWriteString(h,"lineage_failures,"+IntegerToString(s.lineage_failures)+"\r\n");
      FileWriteString(h,"metric_checks,"+IntegerToString(s.metric_checks)+"\r\n");
      FileWriteString(h,"metric_failures,"+IntegerToString(s.metric_failures)+"\r\n");
      FileWriteString(h,"readiness_gates,"+IntegerToString(s.readiness_gates)+"\r\n");
      FileWriteString(h,"readiness_failures,"+IntegerToString(s.readiness_failures)+"\r\n");
      FileWriteString(h,"message,"+CGPI_CsvEscape(s.message)+"\r\n");
      FileClose(h); return true;
   }

   bool WriteDiagnostics(const string file_name,const bool clear,string &diagnostics[])
   {
      MaybeDelete(file_name,clear); int h=OpenWrite(file_name); if(h==INVALID_HANDLE) return false;
      FileWriteString(h,"row,diagnostic\r\n");
      for(int i=0;i<ArraySize(diagnostics);i++)
         FileWriteString(h,IntegerToString(i+1)+","+CGPI_CsvEscape(diagnostics[i])+"\r\n");
      FileClose(h); return true;
   }
};

#endif
//+------------------------------------------------------------------+
