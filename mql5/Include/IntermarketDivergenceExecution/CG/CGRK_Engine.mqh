//+------------------------------------------------------------------+
//| CGRK_Engine.mqh                                                  |
//| Phase 09 — Engine orchestration                                  |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGRK_ENGINE_MQH__
#define __CGRK_ENGINE_MQH__

#include <IntermarketDivergenceExecution/CG/CGRK_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGRK_CsvReader.mqh>
#include <IntermarketDivergenceExecution/CG/CGRK_Ranker.mqh>
#include <IntermarketDivergenceExecution/CG/CGRK_Ledger.mqh>
#include <IntermarketDivergenceExecution/CG/CGRK_Display.mqh>

class CCGRK_Engine
{
private:
   SCGRKConfig   m_cfg;
   SCGRKReportRow m_rows[];
   string        m_diagnostics[];
   CCGRK_CsvReader m_reader;
   CCGRK_Ranker    m_ranker;
   CCGRK_Ledger    m_ledger;
   CCGRK_Display   m_display;

   void AddDiagnostic(const string text)
   {
      int n = ArraySize(m_diagnostics);
      ArrayResize(m_diagnostics, n + 1);
      m_diagnostics[n] = TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS) + ":" + text;
   }

   void LoadOne(const bool enabled, const string file_name, const ECGRKReportKind kind)
   {
      if(!enabled)
      {
         AddDiagnostic("skip_disabled:" + file_name);
         return;
      }

      int before = ArraySize(m_rows);
      int loaded = 0;
      string diag = "";
      bool ok = m_reader.ReadReport(file_name, kind, m_rows, loaded, diag);
      AddDiagnostic((ok ? "ok:" : "fail:") + diag);

      int after = ArraySize(m_rows);
      if(after < before)
         ArrayResize(m_rows, before);
   }

   int RankedCount()
   {
      int c=0;
      for(int i=0; i<ArraySize(m_rows); i++)
         if(m_rows[i].eligible_for_ranking) c++;
      return c;
   }

   int ShortlistCount()
   {
      int c=0;
      for(int i=0; i<ArraySize(m_rows); i++)
         if(m_rows[i].eligible_for_shortlist) c++;
      return c;
   }

public:
   void Configure(const SCGRKConfig &cfg)
   {
      m_cfg = cfg;
   }

   bool Run()
   {
      ArrayResize(m_rows, 0);
      ArrayResize(m_diagnostics, 0);

      LoadOne(m_cfg.read_overall,              m_cfg.phase08_overall_file,              CGRK_REPORT_OVERALL);
      LoadOne(m_cfg.read_by_cg,                m_cfg.phase08_by_cg_file,                CGRK_REPORT_BY_CG);
      LoadOne(m_cfg.read_by_direction,         m_cfg.phase08_by_direction_file,         CGRK_REPORT_BY_DIRECTION);
      LoadOne(m_cfg.read_by_cg_direction,      m_cfg.phase08_by_cg_direction_file,      CGRK_REPORT_BY_CG_DIRECTION);
      LoadOne(m_cfg.read_by_role,              m_cfg.phase08_by_role_file,              CGRK_REPORT_BY_ROLE);
      LoadOne(m_cfg.read_by_cg_direction_role, m_cfg.phase08_by_cg_direction_role_file, CGRK_REPORT_BY_CG_DIRECTION_ROLE);

      m_ranker.ScoreRows(m_rows, m_cfg);
      m_ranker.SortByQualityDescending(m_rows);

      if(m_cfg.write_csv_outputs)
      {
         m_ledger.WriteAll(m_cfg.output_all_ranking_file, m_rows);
         m_ledger.WriteTop(m_cfg.output_top_ranking_file, m_rows, m_cfg.top_rows);
         m_ledger.WriteBottom(m_cfg.output_bottom_ranking_file, m_rows, m_cfg.bottom_rows);
         m_ledger.WriteShortlist(m_cfg.output_shortlist_file, m_rows);
         m_ledger.WriteDiagnostics(m_cfg.output_diagnostics_file, m_diagnostics);
      }

      if(m_cfg.write_html_dashboard)
         m_ledger.WriteHtmlDashboard(m_cfg.output_dashboard_html_file, m_rows, m_cfg.top_rows);

      int loaded_rows = ArraySize(m_rows);
      int ranked_rows = RankedCount();
      int shortlist_rows = ShortlistCount();
      m_display.Show(m_rows, loaded_rows, ranked_rows, shortlist_rows, m_cfg);

      if(m_cfg.print_summary)
      {
         Print("EXP0017 Phase09 ranking complete: loaded=", loaded_rows,
               " ranked=", ranked_rows,
               " shortlist=", shortlist_rows,
               " all_file=", m_cfg.output_all_ranking_file,
               " html=", m_cfg.output_dashboard_html_file);
      }

      return true;
   }
};

#endif
