//+------------------------------------------------------------------+
//| CGP12_Engine.mqh                                                 |
//| Phase 12 — bridge engine                                         |
//+------------------------------------------------------------------+
#property strict
#ifndef __CGP12_ENGINE_MQH__
#define __CGP12_ENGINE_MQH__

#include <IntermarketDivergenceExecution/CG/CGP12_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGP12_FileInventory.mqh>
#include <IntermarketDivergenceExecution/CG/CGP12_Writers.mqh>
#include <IntermarketDivergenceExecution/CG/CGP12_Display.mqh>

class CCGP12_Engine
{
private:
   CCGP12_FileInventory m_inventory;
   CCGP12_Writers       m_writers;
   CCGP12_Display       m_display;

   void CountFiles(SCGP12FileInventoryRow &rows[], SCGP12RunStats &stats)
   {
      stats.files_found = 0;
      stats.files_missing = 0;
      for(int i=0; i<ArraySize(rows); i++)
      {
         if(rows[i].exists) stats.files_found++;
         else stats.files_missing++;
      }
   }

public:
   bool Run(const SCGP12Config &config)
   {
      SCGP12RunStats stats;
      stats.inventory_rows = 0;
      stats.files_found = 0;
      stats.files_missing = 0;
      stats.manifest_written = 0;
      stats.registry_written = 0;
      stats.run_plan_written = 0;
      stats.diagnostics_written = 0;
      stats.status = "started";
      stats.message = "";

      m_inventory.Setup(config.use_common_files, config.max_header_columns_to_inspect);
      m_writers.Setup(config.use_common_files);

      SCGP12FileInventoryRow rows[];
      stats.inventory_rows = m_inventory.Build(config, rows);
      CountFiles(rows, stats);

      if(config.write_inventory_csv)
      {
         if(!m_writers.WriteInventory(config.output_prefix+"_File_Inventory.csv", config.clear_outputs_on_run, rows))
            stats.message += "inventory_write_failed;";
      }

      if(config.write_research_manifest)
      {
         if(m_writers.WriteManifest(config.output_prefix+"_Research_Manifest.json", config.clear_outputs_on_run, config, rows)) stats.manifest_written = 1;
         else stats.message += "manifest_write_failed;";
      }

      if(config.write_experiment_registry_template)
      {
         if(m_writers.WriteRegistryTemplate(config.output_prefix+"_Experiment_Registry_Template.csv", config.clear_outputs_on_run)) stats.registry_written = 1;
         else stats.message += "registry_write_failed;";
      }

      if(config.write_python_run_plan)
      {
         if(m_writers.WritePythonRunPlan(config.output_prefix+"_Python_Run_Plan.md", config.clear_outputs_on_run)) stats.run_plan_written = 1;
         else stats.message += "run_plan_write_failed;";
      }

      stats.status = (StringLen(stats.message) == 0 ? "complete" : "complete_with_warnings");
      if(stats.files_missing > 0)
         stats.message += "some_expected_files_missing;";
      if(StringLen(stats.message) == 0)
         stats.message = "ok";

      if(config.write_diagnostics)
      {
         if(m_writers.WriteDiagnostics(config.output_prefix+"_Diagnostics.csv", config.clear_outputs_on_run, stats)) stats.diagnostics_written = 1;
      }

      m_display.Show(config, stats);
      m_display.PrintSummary(config, stats);
      return true;
   }
};

#endif
//+------------------------------------------------------------------+
