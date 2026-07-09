//+------------------------------------------------------------------+
//| CGS_Engine.mqh                                                   |
//| EXP0017 Phase 08 — Statistical Report Engine                     |
//+------------------------------------------------------------------+
#ifndef __EXP0017_CGS_ENGINE_MQH__
#define __EXP0017_CGS_ENGINE_MQH__

#include <IntermarketDivergenceExecution/CG/CGS_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGS_CsvReader.mqh>
#include <IntermarketDivergenceExecution/CG/CGS_Aggregator.mqh>
#include <IntermarketDivergenceExecution/CG/CGS_Ledger.mqh>
#include <IntermarketDivergenceExecution/CG/CGS_Display.mqh>

class CCGS_StatisticalReportEngine
{
private:
   SCGSReportConfig cfg;
   CCGS_CsvReader   reader;
   CCGS_Aggregator  aggregator;
   CCGS_ReportWriter writer;
   CCGS_Display     display;

   int m_last_sample_count;
   int m_last_report_count;
   datetime m_last_run_time;

   string ReportFile(const string suffix) const
   {
      return cfg.report_prefix + "_" + suffix + ".csv";
   }

   void MaybeWrite(const bool enabled,const string suffix,SCGSGroupStats &groups[],int &report_count)
   {
      if(!enabled)
         return;
      if(writer.WriteStatsFile(ReportFile(suffix), cfg.use_common_files_folder, groups))
         report_count++;
   }

public:
   CCGS_StatisticalReportEngine()
   {
      m_last_sample_count = 0;
      m_last_report_count = 0;
      m_last_run_time = 0;
   }

   void Configure(const SCGSReportConfig &config)
   {
      cfg = config;
      reader.SetDelimiter(cfg.csv_delimiter);
      aggregator.SetWindow(cfg.primary_window);
   }

   bool RunReport()
   {
      SCGSOutcomeSample samples[];
      bool loaded = reader.LoadOutcomeSamples(cfg.outcome_file, cfg.use_common_files_folder, cfg.max_rows_to_read, samples);
      if(!loaded)
      {
         m_last_sample_count = 0;
         m_last_report_count = 0;
         m_last_run_time = TimeCurrent();
         string msg = display.BuildSummary(cfg,0,0,m_last_run_time) + "\nStatus: no samples loaded.";
         display.SetText(msg);
         if(cfg.show_chart_comment) display.ShowIfEnabled(true);
         if(cfg.print_summary) Print(msg);
         return false;
      }

      int reports = 0;
      SCGSGroupStats groups[];
      SCGSGroupStats redflag_source[];

      aggregator.BuildOverall(samples, groups);
      if(ArraySize(redflag_source)==0) { ArrayResize(redflag_source, ArraySize(groups)); for(int i=0;i<ArraySize(groups);i++) redflag_source[i]=groups[i]; }
      MaybeWrite(cfg.generate_overall, "Overall", groups, reports);

      aggregator.BuildByCG(samples, groups);
      MaybeWrite(cfg.generate_cg, "By_CG", groups, reports);

      aggregator.BuildByDirection(samples, groups);
      MaybeWrite(cfg.generate_direction, "By_Direction", groups, reports);

      aggregator.BuildByCGDirection(samples, groups);
      MaybeWrite(cfg.generate_cg_direction, "By_CG_Direction", groups, reports);

      aggregator.BuildByRole(samples, groups);
      MaybeWrite(cfg.generate_role, "By_Role", groups, reports);

      aggregator.BuildByCGDirectionRole(samples, groups);
      MaybeWrite(cfg.generate_cg_direction_role, "By_CG_Direction_Role", groups, reports);

      if(cfg.generate_red_flags)
      {
         // Red flags are most useful on CG-direction-role buckets.
         if(writer.WriteRedFlags(ReportFile("Red_Flags"), cfg.use_common_files_folder, groups, cfg))
            reports++;
      }

      m_last_sample_count = ArraySize(samples);
      m_last_report_count = reports;
      m_last_run_time = TimeCurrent();
      string msg = display.BuildSummary(cfg,m_last_sample_count,m_last_report_count,m_last_run_time);
      display.SetText(msg);
      if(cfg.show_chart_comment) display.ShowIfEnabled(true);
      if(cfg.print_summary) Print(msg);
      return true;
   }

   void UpdateComment()
   {
      display.ShowIfEnabled(cfg.show_chart_comment);
   }
};

#endif
