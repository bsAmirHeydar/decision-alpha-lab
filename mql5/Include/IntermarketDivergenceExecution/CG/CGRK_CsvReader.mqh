//+------------------------------------------------------------------+
//| CGRK_CsvReader.mqh                                               |
//| Phase 09 — Reads Phase 08 report rows                            |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGRK_CSV_READER_MQH__
#define __CGRK_CSV_READER_MQH__

#include <IntermarketDivergenceExecution/CG/CGRK_Types.mqh>

class CCGRK_CsvReader
{
private:
   int HeaderIndex(string &headers[], const string name)
   {
      for(int i=0; i<ArraySize(headers); i++)
      {
         if(StringCompare(CGRK_Clean(headers[i]), name, false) == 0)
            return i;
      }
      return -1;
   }

   string Cell(string &cells[], const int index)
   {
      if(index < 0 || index >= ArraySize(cells))
         return "";
      return CGRK_Clean(cells[index]);
   }

   int CellInt(string &cells[], const int index)
   {
      string v = Cell(cells, index);
      if(v == "") return 0;
      return (int)StringToInteger(v);
   }

   double CellDouble(string &cells[], const int index)
   {
      string v = Cell(cells, index);
      if(v == "") return 0.0;
      return StringToDouble(v);
   }

   void SplitLine(const string line, string &parts[])
   {
      ushort sep = StringGetCharacter(",", 0);
      StringSplit(line, sep, parts);
   }

public:
   bool ReadReport(const string file_name, const ECGRKReportKind kind, SCGRKReportRow &rows[], int &loaded_count, string &diagnostic)
   {
      loaded_count = 0;
      diagnostic = "";

      int handle = FileOpen(file_name, FILE_READ | FILE_TXT | FILE_ANSI);
      if(handle == INVALID_HANDLE)
      {
         diagnostic = "missing_file:" + file_name;
         return false;
      }

      if(FileIsEnding(handle))
      {
         FileClose(handle);
         diagnostic = "empty_file:" + file_name;
         return false;
      }

      string header_line = FileReadString(handle);
      string headers[];
      SplitLine(header_line, headers);

      int idx_bucket_key      = HeaderIndex(headers, "bucket_key");
      int idx_bucket_label    = HeaderIndex(headers, "bucket_label");
      int idx_sample_count    = HeaderIndex(headers, "sample_count");
      int idx_win_count       = HeaderIndex(headers, "win_count");
      int idx_loss_count      = HeaderIndex(headers, "loss_count");
      int idx_zero_count      = HeaderIndex(headers, "zero_count");
      int idx_win_rate        = HeaderIndex(headers, "win_rate_percent");
      int idx_stop_count      = HeaderIndex(headers, "stop_count");
      int idx_stop_rate       = HeaderIndex(headers, "stop_rate_percent");
      int idx_stop_streak     = HeaderIndex(headers, "max_stop_streak");
      int idx_avg_r           = HeaderIndex(headers, "avg_r");
      int idx_avg_points      = HeaderIndex(headers, "avg_points");
      int idx_avg_norm        = HeaderIndex(headers, "avg_normalized");
      int idx_avg_mfe_r       = HeaderIndex(headers, "avg_mfe_r");
      int idx_avg_mae_r       = HeaderIndex(headers, "avg_mae_r");
      int idx_avg_stop        = HeaderIndex(headers, "avg_stop_distance_points");
      int idx_max_r           = HeaderIndex(headers, "max_r");
      int idx_min_r           = HeaderIndex(headers, "min_r");
      int idx_max_points      = HeaderIndex(headers, "max_points");
      int idx_min_points      = HeaderIndex(headers, "min_points");

      // Some Phase 08 outputs may use group_key rather than bucket_key.
      if(idx_bucket_key < 0) idx_bucket_key = HeaderIndex(headers, "group_key");
      if(idx_bucket_label < 0) idx_bucket_label = HeaderIndex(headers, "group_label");

      if(idx_sample_count < 0)
      {
         FileClose(handle);
         diagnostic = "invalid_header_no_sample_count:" + file_name;
         return false;
      }

      while(!FileIsEnding(handle))
      {
         string line = FileReadString(handle);
         if(StringLen(CGRK_Clean(line)) <= 0)
            continue;

         string cells[];
         SplitLine(line, cells);

         SCGRKReportRow row;
         row.valid                 = true;
         row.eligible_for_ranking  = false;
         row.eligible_for_shortlist= false;
         row.report_kind           = kind;
         row.report_name           = CGRK_ReportKindToString(kind);
         row.bucket_key            = Cell(cells, idx_bucket_key);
         row.bucket_label          = Cell(cells, idx_bucket_label);
         if(row.bucket_key == "") row.bucket_key = row.bucket_label;
         if(row.bucket_label == "") row.bucket_label = row.bucket_key;

         row.sample_count          = CellInt(cells, idx_sample_count);
         row.win_count             = CellInt(cells, idx_win_count);
         row.loss_count            = CellInt(cells, idx_loss_count);
         row.zero_count            = CellInt(cells, idx_zero_count);
         row.stop_count            = CellInt(cells, idx_stop_count);
         row.max_stop_streak       = CellInt(cells, idx_stop_streak);

         row.win_rate_percent      = CellDouble(cells, idx_win_rate);
         row.stop_rate_percent     = CellDouble(cells, idx_stop_rate);
         row.avg_r                 = CellDouble(cells, idx_avg_r);
         row.avg_points            = CellDouble(cells, idx_avg_points);
         row.avg_normalized        = CellDouble(cells, idx_avg_norm);
         row.avg_mfe_r             = CellDouble(cells, idx_avg_mfe_r);
         row.avg_mae_r             = CellDouble(cells, idx_avg_mae_r);
         row.avg_stop_distance_points = CellDouble(cells, idx_avg_stop);
         row.max_r                 = CellDouble(cells, idx_max_r);
         row.min_r                 = CellDouble(cells, idx_min_r);
         row.max_points            = CellDouble(cells, idx_max_points);
         row.min_points            = CellDouble(cells, idx_min_points);

         row.sample_confidence_score = 0.0;
         row.win_rate_score          = 0.0;
         row.expectancy_score        = 0.0;
         row.normalized_score        = 0.0;
         row.safety_score            = 0.0;
         row.quality_score           = 0.0;
         row.opportunity_score       = 0.0;
         row.stability_score         = 0.0;
         row.grade                   = "UNRANKED";
         row.red_flag_text           = "";
         row.recommendation_text     = "";

         int n = ArraySize(rows);
         ArrayResize(rows, n + 1);
         rows[n] = row;
         loaded_count++;
      }

      FileClose(handle);
      diagnostic = "loaded:" + file_name + ":" + IntegerToString(loaded_count);
      return true;
   }
};

#endif
