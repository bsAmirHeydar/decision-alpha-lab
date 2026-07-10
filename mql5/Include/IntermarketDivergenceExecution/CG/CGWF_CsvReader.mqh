//+------------------------------------------------------------------+
//| CGWF_CsvReader.mqh                                               |
//| Phase 11 — Reads Phase 10 model-ready dataset                    |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGWF_CSV_READER_MQH__
#define __CGWF_CSV_READER_MQH__

#include <IntermarketDivergenceExecution/CG/CGWF_Types.mqh>

class CCGWF_CsvReader
{
private:
   void SplitLine(const string line, string &parts[])
   {
      ushort sep = StringGetCharacter(",", 0);
      StringSplit(line, sep, parts);
   }

   int HeaderIndex(string &headers[], const string name)
   {
      for(int i=0;i<ArraySize(headers);i++)
         if(StringCompare(CGWF_Clean(headers[i]), name, false) == 0)
            return i;
      return -1;
   }

   string Cell(string &cells[], const int index)
   {
      if(index < 0 || index >= ArraySize(cells)) return "";
      return CGWF_Clean(cells[index]);
   }

   int CellInt(string &cells[], const int index)
   {
      string v = Cell(cells,index);
      if(v == "") return 0;
      return (int)StringToInteger(v);
   }

   double CellDouble(string &cells[], const int index)
   {
      string v = Cell(cells,index);
      if(v == "") return 0.0;
      return StringToDouble(v);
   }

public:
   bool ReadDataset(const string file_name, SCGWFModelRow &rows[], int &loaded, int &accepted, int &rejected, const bool use_only_model_ready, const int max_rows, string &diagnostic)
   {
      loaded = 0;
      accepted = 0;
      rejected = 0;
      diagnostic = "";
      ArrayResize(rows,0);

      int h = FileOpen(file_name, FILE_READ | FILE_TXT | FILE_ANSI);
      if(h == INVALID_HANDLE)
      {
         diagnostic = "missing_phase10_dataset:" + file_name;
         return false;
      }
      if(FileIsEnding(h))
      {
         FileClose(h);
         diagnostic = "empty_phase10_dataset:" + file_name;
         return false;
      }

      string header_line = FileReadString(h);
      string headers[];
      SplitLine(header_line, headers);

      int idx_sample_id = HeaderIndex(headers,"sample_id");
      int idx_outcome_id = HeaderIndex(headers,"outcome_id");
      int idx_signal_id = HeaderIndex(headers,"signal_id");
      int idx_model_use_status = HeaderIndex(headers,"model_use_status");
      int idx_exclusion_reason = HeaderIndex(headers,"exclusion_reason");
      int idx_group = HeaderIndex(headers,"group");
      int idx_group_minutes = HeaderIndex(headers,"group_minutes");
      int idx_current_cycle = HeaderIndex(headers,"current_cycle");
      int idx_reference_cycle = HeaderIndex(headers,"reference_cycle");
      int idx_reference_age = HeaderIndex(headers,"reference_age_cycles");
      int idx_direction = HeaderIndex(headers,"direction");
      int idx_direction_code = HeaderIndex(headers,"direction_code");
      int idx_side = HeaderIndex(headers,"side");
      int idx_side_code = HeaderIndex(headers,"side_code");
      int idx_clean_symbol = HeaderIndex(headers,"clean_symbol");
      int idx_hunter_symbol = HeaderIndex(headers,"hunter_symbol");
      int idx_role_key = HeaderIndex(headers,"role_key");
      int idx_confirmation_broker = HeaderIndex(headers,"confirmation_broker");
      int idx_confirmation_ny = HeaderIndex(headers,"confirmation_ny");
      int idx_hour_ny = HeaderIndex(headers,"hour_ny");
      int idx_minute_ny = HeaderIndex(headers,"minute_of_day_ny");
      int idx_session_ny = HeaderIndex(headers,"session_ny");
      int idx_stop_points = HeaderIndex(headers,"stop_points");
      int idx_daily_range = HeaderIndex(headers,"daily_range_points");
      int idx_risk_to_range = HeaderIndex(headers,"risk_to_daily_range");
      int idx_cycle_end_r = HeaderIndex(headers,"cycle_end_r");
      int idx_plus1_r = HeaderIndex(headers,"plus1_r");
      int idx_plus2_r = HeaderIndex(headers,"plus2_r");
      int idx_plus3_r = HeaderIndex(headers,"plus3_r");
      int idx_day_end_r = HeaderIndex(headers,"day_end_r");
      int idx_mfe_r = HeaderIndex(headers,"mfe_r");
      int idx_mae_r = HeaderIndex(headers,"mae_r");
      int idx_primary_r = HeaderIndex(headers,"primary_r");
      int idx_primary_points = HeaderIndex(headers,"primary_points");
      int idx_primary_norm = HeaderIndex(headers,"primary_norm_daily_range");
      int idx_label_class = HeaderIndex(headers,"label_class");
      int idx_label_win = HeaderIndex(headers,"label_binary_win");
      int idx_hit_1r = HeaderIndex(headers,"label_hit_1r");
      int idx_stopped = HeaderIndex(headers,"label_stopped_intraday");
      int idx_adverse_1r = HeaderIndex(headers,"label_adverse_1r");
      int idx_cg_q = HeaderIndex(headers,"cg_quality_score");
      int idx_cg_rank = HeaderIndex(headers,"cg_rank");
      int idx_cgd_q = HeaderIndex(headers,"cg_direction_quality_score");
      int idx_cgd_rank = HeaderIndex(headers,"cg_direction_rank");
      int idx_role_q = HeaderIndex(headers,"role_quality_score");
      int idx_role_rank = HeaderIndex(headers,"role_rank");
      int idx_cgdr_q = HeaderIndex(headers,"cg_direction_role_quality_score");
      int idx_cgdr_rank = HeaderIndex(headers,"cg_direction_role_rank");
      int idx_shortlist = HeaderIndex(headers,"shortlist_match");
      int idx_notes = HeaderIndex(headers,"notes");

      if(idx_sample_id < 0 || idx_group < 0 || idx_direction < 0 || idx_role_key < 0 || idx_primary_r < 0)
      {
         FileClose(h);
         diagnostic = "invalid_phase10_header:" + file_name;
         return false;
      }

      while(!FileIsEnding(h))
      {
         if(max_rows > 0 && loaded >= max_rows) break;
         string line = FileReadString(h);
         if(StringLen(CGWF_Clean(line)) <= 0) continue;
         string cells[];
         SplitLine(line,cells);
         loaded++;

         SCGWFModelRow r;
         r.valid = true;
         r.source_row_number = loaded;
         r.sample_id = Cell(cells,idx_sample_id);
         r.outcome_id = Cell(cells,idx_outcome_id);
         r.signal_id = Cell(cells,idx_signal_id);
         r.model_use_status = Cell(cells,idx_model_use_status);
         r.exclusion_reason = Cell(cells,idx_exclusion_reason);
         r.group_name = Cell(cells,idx_group);
         r.group_minutes = CellInt(cells,idx_group_minutes);
         r.current_cycle = CellInt(cells,idx_current_cycle);
         r.reference_cycle = CellInt(cells,idx_reference_cycle);
         r.reference_age_cycles = CellInt(cells,idx_reference_age);
         r.direction = Cell(cells,idx_direction);
         r.direction_code = CellInt(cells,idx_direction_code);
         r.side = Cell(cells,idx_side);
         r.side_code = CellInt(cells,idx_side_code);
         r.clean_symbol = Cell(cells,idx_clean_symbol);
         r.hunter_symbol = Cell(cells,idx_hunter_symbol);
         r.role_key = Cell(cells,idx_role_key);
         r.confirmation_broker = Cell(cells,idx_confirmation_broker);
         r.confirmation_ny = Cell(cells,idx_confirmation_ny);
         r.confirmation_time = CGWF_ParseTime(r.confirmation_broker,r.confirmation_ny);
         r.hour_ny = CellInt(cells,idx_hour_ny);
         r.minute_of_day_ny = CellInt(cells,idx_minute_ny);
         r.session_ny = Cell(cells,idx_session_ny);
         r.stop_points = CellDouble(cells,idx_stop_points);
         r.daily_range_points = CellDouble(cells,idx_daily_range);
         r.risk_to_daily_range = CellDouble(cells,idx_risk_to_range);
         r.cycle_end_r = CellDouble(cells,idx_cycle_end_r);
         r.plus1_r = CellDouble(cells,idx_plus1_r);
         r.plus2_r = CellDouble(cells,idx_plus2_r);
         r.plus3_r = CellDouble(cells,idx_plus3_r);
         r.day_end_r = CellDouble(cells,idx_day_end_r);
         r.mfe_r = CellDouble(cells,idx_mfe_r);
         r.mae_r = CellDouble(cells,idx_mae_r);
         r.primary_r = CellDouble(cells,idx_primary_r);
         r.primary_points = CellDouble(cells,idx_primary_points);
         r.primary_norm_daily_range = CellDouble(cells,idx_primary_norm);
         r.label_class = Cell(cells,idx_label_class);
         r.label_binary_win = CellInt(cells,idx_label_win);
         r.label_hit_1r = CellInt(cells,idx_hit_1r);
         r.label_stopped_intraday = CellInt(cells,idx_stopped);
         r.label_adverse_1r = CellInt(cells,idx_adverse_1r);
         r.cg_quality_score = CellDouble(cells,idx_cg_q);
         r.cg_rank = CellInt(cells,idx_cg_rank);
         r.cg_direction_quality_score = CellDouble(cells,idx_cgd_q);
         r.cg_direction_rank = CellInt(cells,idx_cgd_rank);
         r.role_quality_score = CellDouble(cells,idx_role_q);
         r.role_rank = CellInt(cells,idx_role_rank);
         r.cg_direction_role_quality_score = CellDouble(cells,idx_cgdr_q);
         r.cg_direction_role_rank = CellInt(cells,idx_cgdr_rank);
         r.shortlist_match = CellInt(cells,idx_shortlist);
         r.notes = Cell(cells,idx_notes);

         bool accept = true;
         if(use_only_model_ready && r.model_use_status != "model_ready") accept = false;
         if(r.confirmation_time <= 0) accept = false;
         if(r.group_name == "" || r.direction == "" || r.role_key == "") accept = false;

         if(!accept)
         {
            rejected++;
            continue;
         }

         int n = ArraySize(rows);
         ArrayResize(rows,n+1);
         rows[n] = r;
         accepted++;
      }
      FileClose(h);
      diagnostic = "loaded=" + IntegerToString(loaded) + ";accepted=" + IntegerToString(accepted) + ";rejected=" + IntegerToString(rejected);
      return true;
   }
};

#endif
