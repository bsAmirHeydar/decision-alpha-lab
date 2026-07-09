//+------------------------------------------------------------------+
//| CGS_CsvReader.mqh                                                |
//| EXP0017 Phase 08 — Outcome CSV Reader                            |
//+------------------------------------------------------------------+
#ifndef __EXP0017_CGS_CSV_READER_MQH__
#define __EXP0017_CGS_CSV_READER_MQH__

#include <IntermarketDivergenceExecution/CG/CGS_Types.mqh>

class CCGS_CsvReader
{
private:
   string m_headers[];
   ushort m_delimiter;

   int HeaderIndex(const string name) const
   {
      for(int i=0;i<ArraySize(m_headers);i++)
      {
         if(m_headers[i] == name)
            return i;
      }
      return -1;
   }

   string Cell(const string &cells[], const string name) const
   {
      int idx = HeaderIndex(name);
      if(idx < 0 || idx >= ArraySize(cells))
         return "";
      return cells[idx];
   }

   double DCell(const string &cells[], const string name) const
   {
      return CGS_StrToDoubleSafe(Cell(cells,name));
   }

   bool BCell(const string &cells[], const string name) const
   {
      return CGS_StrToBoolSafe(Cell(cells,name));
   }

   int SplitLine(const string line, string &cells[])
   {
      return StringSplit(line, m_delimiter, cells);
   }

   void NormalizeHeaders()
   {
      for(int i=0;i<ArraySize(m_headers);i++)
      {
         StringTrimLeft(m_headers[i]);
         StringTrimRight(m_headers[i]);
      }
   }

public:
   CCGS_CsvReader()
   {
      m_delimiter = ',';
   }

   void SetDelimiter(const string delimiter)
   {
      if(StringLen(delimiter) > 0)
         m_delimiter = (ushort)StringGetCharacter(delimiter,0);
      else
         m_delimiter = ',';
   }

   bool LoadOutcomeSamples(const string file_name,const bool common_folder,const int max_rows,SCGSOutcomeSample &samples[])
   {
      ArrayResize(samples,0);
      int flags = FILE_READ | FILE_TXT | FILE_ANSI;
      if(common_folder)
         flags |= FILE_COMMON;

      int handle = FileOpen(file_name, flags);
      if(handle == INVALID_HANDLE)
      {
         Print("EXP0017 Phase08: cannot open outcome CSV: ", file_name, " error=", GetLastError());
         return false;
      }

      if(FileIsEnding(handle))
      {
         FileClose(handle);
         return false;
      }

      string header_line = FileReadString(handle);
      if(StringLen(header_line) <= 0)
      {
         FileClose(handle);
         return false;
      }
      SplitLine(header_line, m_headers);
      NormalizeHeaders();

      int rows = 0;
      while(!FileIsEnding(handle))
      {
         string line = FileReadString(handle);
         if(StringLen(line) <= 0)
            continue;

         string cells[];
         int n = SplitLine(line, cells);
         if(n <= 0)
            continue;

         SCGSOutcomeSample s;
         s.signal_id             = Cell(cells,"signal_id");
         s.trading_day           = Cell(cells,"trading_day");
         s.confirmation_time     = Cell(cells,"confirmation_time");
         s.cg_name               = Cell(cells,"cg_name");
         s.direction             = Cell(cells,"direction");
         s.side                  = Cell(cells,"side");
         s.hunter_symbol         = Cell(cells,"hunter_symbol");
         s.clean_symbol          = Cell(cells,"clean_symbol");
         s.role_key              = s.hunter_symbol + "_hunter__" + s.clean_symbol + "_clean";

         s.stop_distance_points  = DCell(cells,"stop_distance_points");

         s.cycle_end_points      = DCell(cells,"cycle_end_points");
         s.cycle_end_r           = DCell(cells,"cycle_end_R");
         s.plus1_points          = DCell(cells,"plus1_cycle_points");
         s.plus1_r               = DCell(cells,"plus1_cycle_R");
         s.plus2_points          = DCell(cells,"plus2_cycle_points");
         s.plus2_r               = DCell(cells,"plus2_cycle_R");
         s.plus3_points          = DCell(cells,"plus3_cycle_points");
         s.plus3_r               = DCell(cells,"plus3_cycle_R");
         s.day_end_points        = DCell(cells,"day_end_points");
         s.day_end_r             = DCell(cells,"day_end_R");

         s.mfe_points            = DCell(cells,"MFE_points");
         s.mfe_r                 = DCell(cells,"MFE_R");
         s.mae_points            = DCell(cells,"MAE_points");
         s.mae_r                 = DCell(cells,"MAE_R");

         s.stop_hit              = BCell(cells,"stop_hit_intraday");
         s.stop_hit_time         = Cell(cells,"stop_hit_time");

         s.daily_range_points    = DCell(cells,"daily_range_points");
         s.day_end_normalized    = DCell(cells,"day_end_normalized_by_daily_range");
         s.mfe_normalized        = DCell(cells,"MFE_normalized_by_daily_range");
         s.valid                 = (s.signal_id != "" && s.cg_name != "" && s.direction != "");

         if(!s.valid)
            continue;

         int size = ArraySize(samples);
         ArrayResize(samples, size+1);
         samples[size] = s;
         rows++;

         if(max_rows > 0 && rows >= max_rows)
            break;
      }

      FileClose(handle);
      return (ArraySize(samples) > 0);
   }
};

#endif
