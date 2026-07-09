//+------------------------------------------------------------------+
//| CGM_Engine.mqh                                                   |
//| Phase 10 — Dataset engine orchestration                          |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGM_ENGINE_MQH__
#define __CGM_ENGINE_MQH__

#include <IntermarketDivergenceExecution/CG/CGM_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGM_CsvReader.mqh>
#include <IntermarketDivergenceExecution/CG/CGM_FeatureBuilder.mqh>
#include <IntermarketDivergenceExecution/CG/CGM_Ledger.mqh>
#include <IntermarketDivergenceExecution/CG/CGM_Display.mqh>

class CCGM_Engine
{
private:
   SCGMConfig m_cfg;
   CCGM_CsvReader m_reader;
   CCGM_FeatureBuilder m_builder;
   CCGM_Ledger m_ledger;
   CCGM_Display m_display;

   void AddDiagnostic(string &diagnostics[], const string text)
   {
      int n = ArraySize(diagnostics);
      ArrayResize(diagnostics,n+1);
      diagnostics[n] = text;
   }

   void AddFeatureRow(SCGMFeatureRow &rows[], const SCGMFeatureRow &row)
   {
      int n = ArraySize(rows);
      ArrayResize(rows,n+1);
      rows[n] = row;
   }

   void UpdateSummary(SCGMSummary &s,const SCGMFeatureRow &row)
   {
      if(row.model_use_status == "EXCLUDED")
         s.rows_excluded++;
      else
      {
         s.complete_rows++;
         s.avg_primary_r += row.primary_r;
      }
      if(row.label_class == "WIN") s.win_rows++;
      else if(row.label_class == "LOSS") s.loss_rows++;
      else s.flat_rows++;
      if(row.label_hit_1r == 1) s.hit_1r_rows++;
      if(row.label_stopped_intraday == 1) s.stopped_rows++;
      if(row.label_adverse_1r == 1) s.adverse_1r_rows++;
      if(row.shortlist_match == 1) s.shortlist_matches++;
   }

public:
   void Configure(SCGMConfig &cfg)
   {
      m_cfg = cfg;
      m_builder.Configure(m_cfg);
   }

   bool Run()
   {
      string diagnostics[];
      SCGMSummary summary;
      summary.outcomes_loaded = 0;
      summary.rank_rows_loaded = 0;
      summary.shortlist_rows_loaded = 0;
      summary.rows_written = 0;
      summary.rows_excluded = 0;
      summary.complete_rows = 0;
      summary.win_rows = 0;
      summary.loss_rows = 0;
      summary.flat_rows = 0;
      summary.hit_1r_rows = 0;
      summary.stopped_rows = 0;
      summary.adverse_1r_rows = 0;
      summary.shortlist_matches = 0;
      summary.avg_primary_r = 0.0;

      SCGMOutcomeSample outcomes[];
      string diag = "";
      int loaded = 0;
      bool ok = m_reader.ReadOutcomes(m_cfg.phase07_outcome_file, outcomes, loaded, diag);
      AddDiagnostic(diagnostics, diag);
      summary.outcomes_loaded = loaded;
      if(!ok)
      {
         if(m_cfg.write_diagnostics) m_ledger.WriteDiagnostics(m_cfg.output_diagnostics_file, diagnostics);
         return false;
      }

      SCGMRankRow rankings[];
      SCGMRankRow shortlist[];
      if(m_cfg.use_phase09_ranking_enrichment)
      {
         int rank_loaded = 0;
         string rank_diag = "";
         m_reader.ReadRankings(m_cfg.phase09_all_ranking_file, rankings, rank_loaded, rank_diag);
         AddDiagnostic(diagnostics, rank_diag);
         summary.rank_rows_loaded = rank_loaded;
      }
      if(m_cfg.use_phase09_shortlist_enrichment)
      {
         int shortlist_loaded = 0;
         string shortlist_diag = "";
         m_reader.ReadRankings(m_cfg.phase09_shortlist_file, shortlist, shortlist_loaded, shortlist_diag);
         AddDiagnostic(diagnostics, shortlist_diag);
         summary.shortlist_rows_loaded = shortlist_loaded;
      }

      SCGMFeatureRow feature_rows[];
      int max_rows = MathMax(1, m_cfg.max_rows_to_write);
      for(int i=0;i<ArraySize(outcomes) && ArraySize(feature_rows)<max_rows;i++)
      {
         SCGMFeatureRow row;
         m_builder.Build(outcomes[i], rankings, shortlist, row);
         AddFeatureRow(feature_rows, row);
         UpdateSummary(summary, row);
      }
      summary.rows_written = ArraySize(feature_rows);
      if(summary.complete_rows > 0)
         summary.avg_primary_r = summary.avg_primary_r / (double)summary.complete_rows;

      if(!m_ledger.WriteDataset(m_cfg.output_dataset_file, feature_rows, max_rows))
         AddDiagnostic(diagnostics, "cannot_write_dataset:" + m_cfg.output_dataset_file);
      else
         AddDiagnostic(diagnostics, "wrote_dataset:" + m_cfg.output_dataset_file + ":" + IntegerToString(summary.rows_written));

      if(m_cfg.write_feature_dictionary)
      {
         if(!m_ledger.WriteFeatureDictionary(m_cfg.output_feature_dictionary_file))
            AddDiagnostic(diagnostics, "cannot_write_feature_dictionary:" + m_cfg.output_feature_dictionary_file);
      }
      if(m_cfg.write_label_summary)
      {
         if(!m_ledger.WriteLabelSummary(m_cfg.output_label_summary_file, summary))
            AddDiagnostic(diagnostics, "cannot_write_label_summary:" + m_cfg.output_label_summary_file);
      }
      if(m_cfg.write_diagnostics)
         m_ledger.WriteDiagnostics(m_cfg.output_diagnostics_file, diagnostics);

      if(m_cfg.print_summary)
         m_display.PrintSummary(summary, m_cfg);
      if(m_cfg.show_chart_comment)
         m_display.CommentSummary(summary, m_cfg);
      else
         Comment("");

      return true;
   }
};

#endif
