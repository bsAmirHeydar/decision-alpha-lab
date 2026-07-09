//+------------------------------------------------------------------+
//| CGM_CsvReader.mqh                                                |
//| Phase 10 — Reads Phase 07 outcomes and Phase 09 rankings         |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGM_CSV_READER_MQH__
#define __CGM_CSV_READER_MQH__

#include <IntermarketDivergenceExecution/CG/CGM_Types.mqh>

class CCGM_CsvReader
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
         if(StringCompare(CGM_Clean(headers[i]), name, false) == 0)
            return i;
      return -1;
   }

   string Cell(string &cells[], const int index)
   {
      if(index < 0 || index >= ArraySize(cells)) return "";
      return CGM_Clean(cells[index]);
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
   bool ReadOutcomes(const string file_name, SCGMOutcomeSample &samples[], int &loaded, string &diagnostic)
   {
      loaded = 0;
      diagnostic = "";
      ArrayResize(samples,0);

      int h = FileOpen(file_name, FILE_READ | FILE_TXT | FILE_ANSI);
      if(h == INVALID_HANDLE)
      {
         diagnostic = "missing_phase07_outcome_file:" + file_name;
         return false;
      }
      if(FileIsEnding(h))
      {
         FileClose(h);
         diagnostic = "empty_phase07_outcome_file:" + file_name;
         return false;
      }

      string header_line = FileReadString(h);
      string headers[];
      SplitLine(header_line, headers);

      int idx_outcome_id       = HeaderIndex(headers,"outcome_id");
      int idx_signal_id        = HeaderIndex(headers,"signal_id");
      int idx_availability     = HeaderIndex(headers,"availability");
      int idx_availability_note= HeaderIndex(headers,"availability_note");
      int idx_group            = HeaderIndex(headers,"group");
      int idx_group_minutes    = HeaderIndex(headers,"group_minutes");
      int idx_current_cycle    = HeaderIndex(headers,"current_cycle");
      int idx_reference_cycle  = HeaderIndex(headers,"reference_cycle");
      int idx_direction        = HeaderIndex(headers,"direction");
      int idx_side             = HeaderIndex(headers,"side");
      int idx_clean_symbol     = HeaderIndex(headers,"clean_symbol");
      int idx_hunter_symbol    = HeaderIndex(headers,"hunter_symbol");
      int idx_confirmation_broker = HeaderIndex(headers,"confirmation_broker");
      int idx_confirmation_ny  = HeaderIndex(headers,"confirmation_ny");
      int idx_entry_broker     = HeaderIndex(headers,"entry_broker");
      int idx_entry_price      = HeaderIndex(headers,"entry_price");
      int idx_stop_price       = HeaderIndex(headers,"stop_price");
      int idx_stop_points      = HeaderIndex(headers,"stop_points");
      int idx_cycle_end_broker = HeaderIndex(headers,"cycle_end_broker");
      int idx_cycle_end_price  = HeaderIndex(headers,"cycle_end_price");
      int idx_cycle_end_points = HeaderIndex(headers,"cycle_end_points");
      int idx_cycle_end_r      = HeaderIndex(headers,"cycle_end_r");
      int idx_cycle_stop_hit   = HeaderIndex(headers,"cycle_stop_hit");
      int idx_plus1_points     = HeaderIndex(headers,"plus1_points");
      int idx_plus1_r          = HeaderIndex(headers,"plus1_r");
      int idx_plus2_points     = HeaderIndex(headers,"plus2_points");
      int idx_plus2_r          = HeaderIndex(headers,"plus2_r");
      int idx_plus3_points     = HeaderIndex(headers,"plus3_points");
      int idx_plus3_r          = HeaderIndex(headers,"plus3_r");
      int idx_day_end_points   = HeaderIndex(headers,"day_end_points");
      int idx_day_end_r        = HeaderIndex(headers,"day_end_r");
      int idx_mfe_points       = HeaderIndex(headers,"mfe_points");
      int idx_mfe_r            = HeaderIndex(headers,"mfe_r");
      int idx_mae_points       = HeaderIndex(headers,"mae_points");
      int idx_mae_r            = HeaderIndex(headers,"mae_r");
      int idx_stop_hit_intraday= HeaderIndex(headers,"stop_hit_intraday");
      int idx_stop_hit_time    = HeaderIndex(headers,"stop_hit_time");
      int idx_daily_range      = HeaderIndex(headers,"daily_range_points");
      int idx_day_end_norm     = HeaderIndex(headers,"day_end_norm_daily_range");
      int idx_mfe_norm         = HeaderIndex(headers,"mfe_norm_daily_range");
      int idx_note             = HeaderIndex(headers,"note");

      if(idx_signal_id < 0 || idx_group < 0 || idx_direction < 0 || idx_clean_symbol < 0 || idx_hunter_symbol < 0)
      {
         FileClose(h);
         diagnostic = "invalid_phase07_header:" + file_name;
         return false;
      }

      while(!FileIsEnding(h))
      {
         string line = FileReadString(h);
         if(StringLen(CGM_Clean(line)) <= 0) continue;
         string cells[];
         SplitLine(line,cells);

         SCGMOutcomeSample s;
         s.valid = true;
         s.outcome_id = Cell(cells,idx_outcome_id);
         s.signal_id = Cell(cells,idx_signal_id);
         s.availability = Cell(cells,idx_availability);
         s.availability_note = Cell(cells,idx_availability_note);
         s.group_name = Cell(cells,idx_group);
         s.group_minutes = CellInt(cells,idx_group_minutes);
         s.current_cycle = CellInt(cells,idx_current_cycle);
         s.reference_cycle = CellInt(cells,idx_reference_cycle);
         s.direction = Cell(cells,idx_direction);
         s.side = Cell(cells,idx_side);
         s.clean_symbol = Cell(cells,idx_clean_symbol);
         s.hunter_symbol = Cell(cells,idx_hunter_symbol);
         s.role_key = s.hunter_symbol + "_hunter__" + s.clean_symbol + "_clean";
         s.confirmation_broker = Cell(cells,idx_confirmation_broker);
         s.confirmation_ny = Cell(cells,idx_confirmation_ny);
         s.entry_broker = Cell(cells,idx_entry_broker);
         s.entry_price = CellDouble(cells,idx_entry_price);
         s.stop_price = CellDouble(cells,idx_stop_price);
         s.stop_points = CellDouble(cells,idx_stop_points);
         s.cycle_end_broker = Cell(cells,idx_cycle_end_broker);
         s.cycle_end_price = CellDouble(cells,idx_cycle_end_price);
         s.cycle_end_points = CellDouble(cells,idx_cycle_end_points);
         s.cycle_end_r = CellDouble(cells,idx_cycle_end_r);
         s.cycle_stop_hit = CGM_ToBool(Cell(cells,idx_cycle_stop_hit));
         s.plus1_points = CellDouble(cells,idx_plus1_points);
         s.plus1_r = CellDouble(cells,idx_plus1_r);
         s.plus2_points = CellDouble(cells,idx_plus2_points);
         s.plus2_r = CellDouble(cells,idx_plus2_r);
         s.plus3_points = CellDouble(cells,idx_plus3_points);
         s.plus3_r = CellDouble(cells,idx_plus3_r);
         s.day_end_points = CellDouble(cells,idx_day_end_points);
         s.day_end_r = CellDouble(cells,idx_day_end_r);
         s.mfe_points = CellDouble(cells,idx_mfe_points);
         s.mfe_r = CellDouble(cells,idx_mfe_r);
         s.mae_points = CellDouble(cells,idx_mae_points);
         s.mae_r = CellDouble(cells,idx_mae_r);
         s.stop_hit_intraday = CGM_ToBool(Cell(cells,idx_stop_hit_intraday));
         s.stop_hit_time = Cell(cells,idx_stop_hit_time);
         s.daily_range_points = CellDouble(cells,idx_daily_range);
         s.day_end_norm_daily_range = CellDouble(cells,idx_day_end_norm);
         s.mfe_norm_daily_range = CellDouble(cells,idx_mfe_norm);
         s.note = Cell(cells,idx_note);

         int n = ArraySize(samples);
         ArrayResize(samples,n+1);
         samples[n] = s;
         loaded++;
      }
      FileClose(h);
      diagnostic = "loaded_phase07_outcomes:" + IntegerToString(loaded);
      return true;
   }

   bool ReadRankings(const string file_name, SCGMRankRow &rows[], int &loaded, string &diagnostic)
   {
      loaded = 0;
      diagnostic = "";
      ArrayResize(rows,0);
      int h = FileOpen(file_name, FILE_READ | FILE_TXT | FILE_ANSI);
      if(h == INVALID_HANDLE)
      {
         diagnostic = "missing_ranking_file:" + file_name;
         return false;
      }
      if(FileIsEnding(h))
      {
         FileClose(h);
         diagnostic = "empty_ranking_file:" + file_name;
         return false;
      }
      string header_line = FileReadString(h);
      string headers[];
      SplitLine(header_line,headers);

      int idx_rank = HeaderIndex(headers,"rank");
      int idx_report = HeaderIndex(headers,"report_name");
      int idx_key = HeaderIndex(headers,"bucket_key");
      int idx_label = HeaderIndex(headers,"bucket_label");
      int idx_sample = HeaderIndex(headers,"sample_count");
      int idx_winrate = HeaderIndex(headers,"win_rate_percent");
      int idx_avg_r = HeaderIndex(headers,"avg_r");
      int idx_avg_points = HeaderIndex(headers,"avg_points");
      int idx_avg_norm = HeaderIndex(headers,"avg_normalized");
      int idx_stop_rate = HeaderIndex(headers,"stop_rate_percent");
      int idx_stop_streak = HeaderIndex(headers,"max_stop_streak");
      int idx_quality = HeaderIndex(headers,"quality_score");
      int idx_grade = HeaderIndex(headers,"grade");
      int idx_sample_conf = HeaderIndex(headers,"sample_confidence_score");
      int idx_shortlist = HeaderIndex(headers,"shortlist");
      int idx_red = HeaderIndex(headers,"red_flags");
      int idx_rec = HeaderIndex(headers,"recommendation");

      if(idx_key < 0 || idx_quality < 0)
      {
         FileClose(h);
         diagnostic = "invalid_ranking_header:" + file_name;
         return false;
      }

      while(!FileIsEnding(h))
      {
         string line = FileReadString(h);
         if(StringLen(CGM_Clean(line)) <= 0) continue;
         string cells[];
         SplitLine(line,cells);

         SCGMRankRow r;
         r.valid = true;
         r.rank = CellInt(cells,idx_rank);
         r.report_name = Cell(cells,idx_report);
         r.bucket_key = Cell(cells,idx_key);
         r.bucket_label = Cell(cells,idx_label);
         r.sample_count = CellInt(cells,idx_sample);
         r.win_rate_percent = CellDouble(cells,idx_winrate);
         r.avg_r = CellDouble(cells,idx_avg_r);
         r.avg_points = CellDouble(cells,idx_avg_points);
         r.avg_normalized = CellDouble(cells,idx_avg_norm);
         r.stop_rate_percent = CellDouble(cells,idx_stop_rate);
         r.max_stop_streak = CellInt(cells,idx_stop_streak);
         r.quality_score = CellDouble(cells,idx_quality);
         r.grade = Cell(cells,idx_grade);
         r.sample_confidence_score = CellDouble(cells,idx_sample_conf);
         r.shortlist = CGM_ToBool(Cell(cells,idx_shortlist));
         r.red_flags = Cell(cells,idx_red);
         r.recommendation = Cell(cells,idx_rec);

         int n = ArraySize(rows);
         ArrayResize(rows,n+1);
         rows[n] = r;
         loaded++;
      }
      FileClose(h);
      diagnostic = "loaded_rankings:" + file_name + ":" + IntegerToString(loaded);
      return true;
   }
};

#endif
