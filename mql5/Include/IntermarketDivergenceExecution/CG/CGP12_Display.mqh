//+------------------------------------------------------------------+
//| CGP12_Display.mqh                                                |
//| Phase 12 — compact display                                       |
//+------------------------------------------------------------------+
#property strict
#ifndef __CGP12_DISPLAY_MQH__
#define __CGP12_DISPLAY_MQH__

#include <IntermarketDivergenceExecution/CG/CGP12_Types.mqh>

class CCGP12_Display
{
public:
   void Show(const SCGP12Config &config, const SCGP12RunStats &stats)
   {
      if(!config.show_chart_comment)
      {
         Comment("");
         return;
      }
      string text = "EXP0017 Phase 12 — Python Research Bridge\n";
      text += "status: "+stats.status+"\n";
      text += "files found: "+IntegerToString(stats.files_found)+" / "+IntegerToString(stats.inventory_rows)+"\n";
      text += "manifest: "+IntegerToString(stats.manifest_written)+" registry: "+IntegerToString(stats.registry_written)+" run_plan: "+IntegerToString(stats.run_plan_written)+"\n";
      text += "outputs prefix: "+config.output_prefix+"\n";
      text += "NO TRADING — research bridge only";
      Comment(text);
   }

   void PrintSummary(const SCGP12Config &config, const SCGP12RunStats &stats)
   {
      if(!config.print_summary)
         return;
      Print("EXP0017 Phase12 bridge complete: status=", stats.status,
            " inventory=", stats.inventory_rows,
            " found=", stats.files_found,
            " missing=", stats.files_missing,
            " message=", stats.message);
   }
};

#endif
//+------------------------------------------------------------------+
