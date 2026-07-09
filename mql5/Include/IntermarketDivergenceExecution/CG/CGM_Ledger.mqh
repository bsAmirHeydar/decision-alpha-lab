//+------------------------------------------------------------------+
//| CGM_Ledger.mqh                                                   |
//| Phase 10 — Dataset, dictionary, summary, diagnostics writers     |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGM_LEDGER_MQH__
#define __CGM_LEDGER_MQH__

#include <IntermarketDivergenceExecution/CG/CGM_Types.mqh>

class CCGM_Ledger
{
private:
   string DatasetHeader()
   {
      return "sample_id,outcome_id,signal_id,model_use_status,exclusion_reason,availability,group,group_minutes,current_cycle,reference_cycle,reference_age_cycles,direction,direction_code,side,side_code,clean_symbol,hunter_symbol,role_key,confirmation_broker,confirmation_ny,hour_ny,minute_of_day_ny,session_ny,entry_price,stop_price,stop_points,daily_range_points,risk_to_daily_range,cycle_end_r,plus1_r,plus2_r,plus3_r,day_end_r,mfe_r,mae_r,cycle_end_points,plus1_points,plus2_points,plus3_points,day_end_points,mfe_points,mae_points,primary_window,primary_r,primary_points,primary_norm_daily_range,label_class,label_binary_win,label_hit_1r,label_stopped_intraday,label_adverse_1r,cg_quality_score,cg_rank,cg_direction_quality_score,cg_direction_rank,role_quality_score,role_rank,cg_direction_role_quality_score,cg_direction_role_rank,shortlist_match,notes";
   }

   string DatasetRow(const SCGMFeatureRow &r)
   {
      return CGM_CsvEscape(r.sample_id) + "," +
         CGM_CsvEscape(r.outcome_id) + "," +
         CGM_CsvEscape(r.signal_id) + "," +
         CGM_CsvEscape(r.model_use_status) + "," +
         CGM_CsvEscape(r.exclusion_reason) + "," +
         CGM_CsvEscape(r.availability) + "," +
         CGM_CsvEscape(r.group_name) + "," +
         IntegerToString(r.group_minutes) + "," +
         IntegerToString(r.current_cycle) + "," +
         IntegerToString(r.reference_cycle) + "," +
         IntegerToString(r.reference_age_cycles) + "," +
         CGM_CsvEscape(r.direction) + "," +
         IntegerToString(r.direction_code) + "," +
         CGM_CsvEscape(r.side) + "," +
         IntegerToString(r.side_code) + "," +
         CGM_CsvEscape(r.clean_symbol) + "," +
         CGM_CsvEscape(r.hunter_symbol) + "," +
         CGM_CsvEscape(r.role_key) + "," +
         CGM_CsvEscape(r.confirmation_broker) + "," +
         CGM_CsvEscape(r.confirmation_ny) + "," +
         IntegerToString(r.hour_ny) + "," +
         IntegerToString(r.minute_of_day_ny) + "," +
         CGM_CsvEscape(r.session_ny) + "," +
         DoubleToString(r.entry_price,8) + "," +
         DoubleToString(r.stop_price,8) + "," +
         DoubleToString(r.stop_points,2) + "," +
         DoubleToString(r.daily_range_points,2) + "," +
         DoubleToString(r.risk_to_daily_range,8) + "," +
         DoubleToString(r.cycle_end_r,4) + "," +
         DoubleToString(r.plus1_r,4) + "," +
         DoubleToString(r.plus2_r,4) + "," +
         DoubleToString(r.plus3_r,4) + "," +
         DoubleToString(r.day_end_r,4) + "," +
         DoubleToString(r.mfe_r,4) + "," +
         DoubleToString(r.mae_r,4) + "," +
         DoubleToString(r.cycle_end_points,2) + "," +
         DoubleToString(r.plus1_points,2) + "," +
         DoubleToString(r.plus2_points,2) + "," +
         DoubleToString(r.plus3_points,2) + "," +
         DoubleToString(r.day_end_points,2) + "," +
         DoubleToString(r.mfe_points,2) + "," +
         DoubleToString(r.mae_points,2) + "," +
         CGM_CsvEscape(r.primary_window) + "," +
         DoubleToString(r.primary_r,4) + "," +
         DoubleToString(r.primary_points,2) + "," +
         DoubleToString(r.primary_norm_daily_range,8) + "," +
         CGM_CsvEscape(r.label_class) + "," +
         IntegerToString(r.label_binary_win) + "," +
         IntegerToString(r.label_hit_1r) + "," +
         IntegerToString(r.label_stopped_intraday) + "," +
         IntegerToString(r.label_adverse_1r) + "," +
         DoubleToString(r.cg_quality_score,2) + "," +
         IntegerToString(r.cg_rank) + "," +
         DoubleToString(r.cg_direction_quality_score,2) + "," +
         IntegerToString(r.cg_direction_rank) + "," +
         DoubleToString(r.role_quality_score,2) + "," +
         IntegerToString(r.role_rank) + "," +
         DoubleToString(r.cg_direction_role_quality_score,2) + "," +
         IntegerToString(r.cg_direction_role_rank) + "," +
         IntegerToString(r.shortlist_match) + "," +
         CGM_CsvEscape(r.notes);
   }

   void WriteDictRow(const int h,const string name,const string role,const string type,const string description)
   {
      FileWriteString(h, CGM_CsvEscape(name) + "," + CGM_CsvEscape(role) + "," + CGM_CsvEscape(type) + "," + CGM_CsvEscape(description) + "\r\n");
   }

public:
   bool WriteDataset(const string file_name, SCGMFeatureRow &rows[], const int max_rows)
   {
      int h = FileOpen(file_name, FILE_WRITE | FILE_TXT | FILE_ANSI);
      if(h == INVALID_HANDLE) return false;
      FileWriteString(h, DatasetHeader() + "\r\n");
      int written = 0;
      for(int i=0;i<ArraySize(rows) && written < max_rows;i++)
      {
         FileWriteString(h, DatasetRow(rows[i]) + "\r\n");
         written++;
      }
      FileClose(h);
      return true;
   }

   bool WriteFeatureDictionary(const string file_name)
   {
      int h = FileOpen(file_name, FILE_WRITE | FILE_TXT | FILE_ANSI);
      if(h == INVALID_HANDLE) return false;
      FileWriteString(h, "feature_name,role,type,description\r\n");
      WriteDictRow(h,"group_minutes","feature","integer","Cycle-group duration in minutes.");
      WriteDictRow(h,"reference_age_cycles","feature","integer","Distance between current cycle and reference cycle.");
      WriteDictRow(h,"direction_code","feature","integer","BUY=1, SELL=-1.");
      WriteDictRow(h,"side_code","feature","integer","LOW=1, HIGH=-1.");
      WriteDictRow(h,"hour_ny","feature","integer","Confirmation hour in New York-derived trading clock when parseable.");
      WriteDictRow(h,"session_ny","feature","categorical","Session bucket inferred from New York minute-of-day.");
      WriteDictRow(h,"stop_points","feature","double","Clean-symbol stop-reference distance in points.");
      WriteDictRow(h,"risk_to_daily_range","feature","double","Stop distance divided by clean-symbol daily range.");
      WriteDictRow(h,"mfe_r","feature/outcome","double","Maximum favorable excursion in R after confirmation.");
      WriteDictRow(h,"mae_r","feature/outcome","double","Maximum adverse excursion in R after confirmation.");
      WriteDictRow(h,"primary_r","label_source","double","R result from selected label window.");
      WriteDictRow(h,"label_class","label","categorical","WIN, LOSS, or FLAT based on selected R thresholds.");
      WriteDictRow(h,"label_binary_win","label","integer","1 when label_class is WIN, otherwise 0.");
      WriteDictRow(h,"label_hit_1r","label","integer","1 when MFE reaches configured one-R threshold.");
      WriteDictRow(h,"label_stopped_intraday","label","integer","1 when stop was touched intraday.");
      WriteDictRow(h,"cg_direction_role_quality_score","enrichment","double","Phase09 quality score for CG-direction-role bucket when available.");
      WriteDictRow(h,"shortlist_match","enrichment","integer","1 when this signal belongs to a Phase09 shortlist bucket.");
      FileClose(h);
      return true;
   }

   bool WriteLabelSummary(const string file_name, const SCGMSummary &s)
   {
      int h = FileOpen(file_name, FILE_WRITE | FILE_TXT | FILE_ANSI);
      if(h == INVALID_HANDLE) return false;
      FileWriteString(h,"metric,value\r\n");
      FileWriteString(h,"outcomes_loaded," + IntegerToString(s.outcomes_loaded) + "\r\n");
      FileWriteString(h,"rank_rows_loaded," + IntegerToString(s.rank_rows_loaded) + "\r\n");
      FileWriteString(h,"shortlist_rows_loaded," + IntegerToString(s.shortlist_rows_loaded) + "\r\n");
      FileWriteString(h,"rows_written," + IntegerToString(s.rows_written) + "\r\n");
      FileWriteString(h,"rows_excluded," + IntegerToString(s.rows_excluded) + "\r\n");
      FileWriteString(h,"win_rows," + IntegerToString(s.win_rows) + "\r\n");
      FileWriteString(h,"loss_rows," + IntegerToString(s.loss_rows) + "\r\n");
      FileWriteString(h,"flat_rows," + IntegerToString(s.flat_rows) + "\r\n");
      FileWriteString(h,"hit_1r_rows," + IntegerToString(s.hit_1r_rows) + "\r\n");
      FileWriteString(h,"stopped_rows," + IntegerToString(s.stopped_rows) + "\r\n");
      FileWriteString(h,"adverse_1r_rows," + IntegerToString(s.adverse_1r_rows) + "\r\n");
      FileWriteString(h,"shortlist_matches," + IntegerToString(s.shortlist_matches) + "\r\n");
      FileWriteString(h,"avg_primary_r," + DoubleToString(s.avg_primary_r,6) + "\r\n");
      FileClose(h);
      return true;
   }

   bool WriteDiagnostics(const string file_name, string &diagnostics[])
   {
      int h = FileOpen(file_name, FILE_WRITE | FILE_TXT | FILE_ANSI);
      if(h == INVALID_HANDLE) return false;
      FileWriteString(h,"row,diagnostic\r\n");
      for(int i=0;i<ArraySize(diagnostics);i++)
         FileWriteString(h,IntegerToString(i+1) + "," + CGM_CsvEscape(diagnostics[i]) + "\r\n");
      FileClose(h);
      return true;
   }
};

#endif
