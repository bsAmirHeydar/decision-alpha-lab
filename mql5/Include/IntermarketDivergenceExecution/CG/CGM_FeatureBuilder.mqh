//+------------------------------------------------------------------+
//| CGM_FeatureBuilder.mqh                                           |
//| Phase 10 — Feature and label construction                        |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGM_FEATURE_BUILDER_MQH__
#define __CGM_FEATURE_BUILDER_MQH__

#include <IntermarketDivergenceExecution/CG/CGM_Types.mqh>

class CCGM_FeatureBuilder
{
private:
   SCGMConfig m_cfg;

   int FindRankByKey(SCGMRankRow &rows[], const string report_name, const string key)
   {
      string k = CGM_Clean(key);
      for(int i=0;i<ArraySize(rows);i++)
      {
         if(!rows[i].valid) continue;
         if(report_name != "" && rows[i].report_name != report_name) continue;
         if(CGM_Clean(rows[i].bucket_key) == k)
            return i;
      }
      return -1;
   }

   double PrimaryR(const SCGMOutcomeSample &s)
   {
      if(m_cfg.primary_label_window == CGM_LABEL_CYCLE_END) return s.cycle_end_r;
      if(m_cfg.primary_label_window == CGM_LABEL_PLUS_1_CYCLE) return s.plus1_r;
      if(m_cfg.primary_label_window == CGM_LABEL_PLUS_2_CYCLE) return s.plus2_r;
      if(m_cfg.primary_label_window == CGM_LABEL_PLUS_3_CYCLE) return s.plus3_r;
      if(m_cfg.primary_label_window == CGM_LABEL_DAY_END) return s.day_end_r;
      if(m_cfg.primary_label_window == CGM_LABEL_MFE) return s.mfe_r;
      return s.cycle_end_r;
   }

   double PrimaryPoints(const SCGMOutcomeSample &s)
   {
      if(m_cfg.primary_label_window == CGM_LABEL_CYCLE_END) return s.cycle_end_points;
      if(m_cfg.primary_label_window == CGM_LABEL_PLUS_1_CYCLE) return s.plus1_points;
      if(m_cfg.primary_label_window == CGM_LABEL_PLUS_2_CYCLE) return s.plus2_points;
      if(m_cfg.primary_label_window == CGM_LABEL_PLUS_3_CYCLE) return s.plus3_points;
      if(m_cfg.primary_label_window == CGM_LABEL_DAY_END) return s.day_end_points;
      if(m_cfg.primary_label_window == CGM_LABEL_MFE) return s.mfe_points;
      return s.cycle_end_points;
   }

   string LabelClass(const double r)
   {
      if(r > m_cfg.win_threshold_r) return "WIN";
      if(r < m_cfg.loss_threshold_r) return "LOSS";
      return "FLAT";
   }

public:
   void Configure(SCGMConfig &cfg)
   {
      m_cfg = cfg;
   }

   bool Build(const SCGMOutcomeSample &s, SCGMRankRow &rankings[], SCGMRankRow &shortlist[], SCGMFeatureRow &row)
   {
      row.valid = true;
      row.model_use_status = "INCLUDED";
      row.exclusion_reason = "";
      row.outcome_id = s.outcome_id;
      row.signal_id = s.signal_id;
      row.sample_id = (s.outcome_id != "" ? s.outcome_id : s.signal_id);
      row.availability = s.availability;
      row.group_name = s.group_name;
      row.group_minutes = s.group_minutes;
      row.current_cycle = s.current_cycle;
      row.reference_cycle = s.reference_cycle;
      row.reference_age_cycles = s.current_cycle - s.reference_cycle;
      row.direction = s.direction;
      row.direction_code = CGM_DirectionCode(s.direction);
      row.side = s.side;
      row.side_code = CGM_SideCode(s.side);
      row.clean_symbol = s.clean_symbol;
      row.hunter_symbol = s.hunter_symbol;
      row.role_key = s.role_key;
      row.confirmation_broker = s.confirmation_broker;
      row.confirmation_ny = s.confirmation_ny;
      row.hour_ny = CGM_HourFromText(s.confirmation_ny);
      row.minute_of_day_ny = CGM_MinuteOfDayFromText(s.confirmation_ny);
      row.session_ny = CGM_SessionFromNyMinute(row.minute_of_day_ny);
      row.entry_price = s.entry_price;
      row.stop_price = s.stop_price;
      row.stop_points = s.stop_points;
      row.daily_range_points = s.daily_range_points;
      row.risk_to_daily_range = CGM_SafeDiv(s.stop_points, s.daily_range_points);
      row.cycle_end_r = s.cycle_end_r;
      row.plus1_r = s.plus1_r;
      row.plus2_r = s.plus2_r;
      row.plus3_r = s.plus3_r;
      row.day_end_r = s.day_end_r;
      row.mfe_r = s.mfe_r;
      row.mae_r = s.mae_r;
      row.cycle_end_points = s.cycle_end_points;
      row.plus1_points = s.plus1_points;
      row.plus2_points = s.plus2_points;
      row.plus3_points = s.plus3_points;
      row.day_end_points = s.day_end_points;
      row.mfe_points = s.mfe_points;
      row.mae_points = s.mae_points;
      row.primary_window = CGM_LabelWindowText(m_cfg.primary_label_window);
      row.primary_r = PrimaryR(s);
      row.primary_points = PrimaryPoints(s);
      row.primary_norm_daily_range = CGM_SafeDiv(row.primary_points, s.daily_range_points);
      row.label_class = LabelClass(row.primary_r);
      row.label_binary_win = (row.label_class == "WIN" ? 1 : 0);
      row.label_hit_1r = (s.mfe_r >= m_cfg.one_r_threshold ? 1 : 0);
      row.label_stopped_intraday = (s.stop_hit_intraday ? 1 : 0);
      row.label_adverse_1r = (s.mae_r <= m_cfg.adverse_one_r_threshold ? 1 : 0);

      row.cg_quality_score = 0.0;
      row.cg_rank = 0;
      row.cg_direction_quality_score = 0.0;
      row.cg_direction_rank = 0;
      row.role_quality_score = 0.0;
      row.role_rank = 0;
      row.cg_direction_role_quality_score = 0.0;
      row.cg_direction_role_rank = 0;
      row.shortlist_match = 0;
      row.notes = "";

      if(m_cfg.require_complete_outcome && StringToUpper(CGM_Clean(s.availability)) != "COMPLETE")
      {
         row.model_use_status = "EXCLUDED";
         row.exclusion_reason = "availability_not_complete";
      }

      if(m_cfg.skip_zero_risk_rows && s.stop_points <= 0.0)
      {
         row.model_use_status = "EXCLUDED";
         row.exclusion_reason = (row.exclusion_reason == "" ? "zero_or_negative_stop_points" : row.exclusion_reason + ";zero_or_negative_stop_points");
      }

      if(m_cfg.use_phase09_ranking_enrichment)
      {
         string cg_key = s.group_name;
         string cg_dir_key = s.group_name + "|" + s.direction;
         string role_key = s.role_key;
         string cg_dir_role_key = s.group_name + "|" + s.direction + "|" + s.role_key;

         int idx = FindRankByKey(rankings,"",cg_key);
         if(idx >= 0) { row.cg_quality_score = rankings[idx].quality_score; row.cg_rank = rankings[idx].rank; }
         idx = FindRankByKey(rankings,"",cg_dir_key);
         if(idx >= 0) { row.cg_direction_quality_score = rankings[idx].quality_score; row.cg_direction_rank = rankings[idx].rank; }
         idx = FindRankByKey(rankings,"",role_key);
         if(idx >= 0) { row.role_quality_score = rankings[idx].quality_score; row.role_rank = rankings[idx].rank; }
         idx = FindRankByKey(rankings,"",cg_dir_role_key);
         if(idx >= 0) { row.cg_direction_role_quality_score = rankings[idx].quality_score; row.cg_direction_role_rank = rankings[idx].rank; }
      }

      if(m_cfg.use_phase09_shortlist_enrichment)
      {
         string cg_dir_role_key = s.group_name + "|" + s.direction + "|" + s.role_key;
         if(FindRankByKey(shortlist,"",cg_dir_role_key) >= 0 || FindRankByKey(shortlist,"",s.group_name + "|" + s.direction) >= 0 || FindRankByKey(shortlist,"",s.group_name) >= 0)
            row.shortlist_match = 1;
      }

      return true;
   }
};

#endif
