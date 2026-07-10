//+------------------------------------------------------------------+
//| CGPI_Display.mqh                                                 |
//| Phase 12.5 — Compact offline-audit status output                 |
//+------------------------------------------------------------------+
#property strict
#ifndef __CGPI_DISPLAY_MQH__
#define __CGPI_DISPLAY_MQH__

#include <IntermarketDivergenceExecution/CG/CGPI_Types.mqh>

class CCGPI_Display
{
private:
   string SummaryText(const SCGPIRunStats &s)
   {
      string text="EXP0017 Phase 12.5 — Pipeline Integrity\n";
      text+="Readiness: "+s.readiness_status+"\n";
      text+="Files: "+IntegerToString(s.files_found)+" found / "+IntegerToString(s.files_missing)+" missing\n";
      text+="Critical schema issues: "+IntegerToString(s.critical_schema_issues)+"\n";
      text+="Duplicate keys: "+IntegerToString(s.duplicate_primary_keys)+"\n";
      text+="Lineage failures: "+IntegerToString(s.lineage_failures)+"\n";
      text+="Metric failures: "+IntegerToString(s.metric_failures)+"\n";
      text+="Boundary: research integrity only; no execution.";
      return text;
   }
public:
   void Show(const SCGPIConfig &cfg,const SCGPIRunStats &s)
   {
      if(cfg.show_chart_comment) Comment(SummaryText(s));
      else Comment("");
   }
   void PrintSummary(const SCGPIConfig &cfg,const SCGPIRunStats &s)
   {
      if(!cfg.print_summary) return;
      Print("EXP0017 Phase12.5 integrity complete: readiness=",s.readiness_status,
            " files_found=",s.files_found," missing=",s.files_missing,
            " critical_schema=",s.critical_schema_issues,
            " duplicate_keys=",s.duplicate_primary_keys,
            " lineage_failures=",s.lineage_failures,
            " metric_failures=",s.metric_failures);
   }
};

#endif
//+------------------------------------------------------------------+
