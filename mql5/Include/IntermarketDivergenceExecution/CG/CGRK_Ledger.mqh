//+------------------------------------------------------------------+
//| CGRK_Ledger.mqh                                                  |
//| Phase 09 — Ranking output writers                                |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGRK_LEDGER_MQH__
#define __CGRK_LEDGER_MQH__

#include <IntermarketDivergenceExecution/CG/CGRK_Types.mqh>

class CCGRK_Ledger
{
private:
   string Header()
   {
      return "rank,report_name,bucket_key,bucket_label,sample_count,win_rate_percent,avg_r,avg_points,avg_normalized,stop_rate_percent,max_stop_streak,quality_score,grade,sample_confidence_score,win_rate_score,expectancy_score,normalized_score,safety_score,opportunity_score,stability_score,shortlist,red_flags,recommendation";
   }

   string RowToCsv(const int rank, const SCGRKReportRow &r)
   {
      string line = IntegerToString(rank) + "," +
         CGRK_CsvEscape(r.report_name) + "," +
         CGRK_CsvEscape(r.bucket_key) + "," +
         CGRK_CsvEscape(r.bucket_label) + "," +
         IntegerToString(r.sample_count) + "," +
         DoubleToString(r.win_rate_percent, 2) + "," +
         DoubleToString(r.avg_r, 4) + "," +
         DoubleToString(r.avg_points, 2) + "," +
         DoubleToString(r.avg_normalized, 6) + "," +
         DoubleToString(r.stop_rate_percent, 2) + "," +
         IntegerToString(r.max_stop_streak) + "," +
         DoubleToString(r.quality_score, 2) + "," +
         CGRK_CsvEscape(r.grade) + "," +
         DoubleToString(r.sample_confidence_score, 2) + "," +
         DoubleToString(r.win_rate_score, 2) + "," +
         DoubleToString(r.expectancy_score, 2) + "," +
         DoubleToString(r.normalized_score, 2) + "," +
         DoubleToString(r.safety_score, 2) + "," +
         DoubleToString(r.opportunity_score, 2) + "," +
         DoubleToString(r.stability_score, 2) + "," +
         (r.eligible_for_shortlist ? "true" : "false") + "," +
         CGRK_CsvEscape(r.red_flag_text) + "," +
         CGRK_CsvEscape(r.recommendation_text);
      return line;
   }

   bool WriteRows(const string file_name, SCGRKReportRow &rows[], const int start, const int max_rows, const bool shortlist_only, const bool bottom_mode)
   {
      int handle = FileOpen(file_name, FILE_WRITE | FILE_TXT | FILE_ANSI);
      if(handle == INVALID_HANDLE)
         return false;

      FileWriteString(handle, Header() + "\r\n");
      int written = 0;
      int n = ArraySize(rows);

      if(bottom_mode)
      {
         for(int i=n-1; i>=0 && written < max_rows; i--)
         {
            if(shortlist_only && !rows[i].eligible_for_shortlist) continue;
            if(!shortlist_only && !rows[i].eligible_for_ranking) continue;
            FileWriteString(handle, RowToCsv(written + 1, rows[i]) + "\r\n");
            written++;
         }
      }
      else
      {
         for(int i=start; i<n && written < max_rows; i++)
         {
            if(shortlist_only && !rows[i].eligible_for_shortlist) continue;
            if(!shortlist_only && !rows[i].eligible_for_ranking) continue;
            FileWriteString(handle, RowToCsv(i + 1, rows[i]) + "\r\n");
            written++;
         }
      }

      FileClose(handle);
      return true;
   }

public:
   bool WriteAll(const string file_name, SCGRKReportRow &rows[])
   {
      return WriteRows(file_name, rows, 0, MathMax(1, ArraySize(rows)), false, false);
   }

   bool WriteTop(const string file_name, SCGRKReportRow &rows[], const int top_rows)
   {
      return WriteRows(file_name, rows, 0, MathMax(1, top_rows), false, false);
   }

   bool WriteBottom(const string file_name, SCGRKReportRow &rows[], const int bottom_rows)
   {
      return WriteRows(file_name, rows, 0, MathMax(1, bottom_rows), false, true);
   }

   bool WriteShortlist(const string file_name, SCGRKReportRow &rows[])
   {
      return WriteRows(file_name, rows, 0, MathMax(1, ArraySize(rows)), true, false);
   }

   bool WriteDiagnostics(const string file_name, string &diagnostics[])
   {
      int handle = FileOpen(file_name, FILE_WRITE | FILE_TXT | FILE_ANSI);
      if(handle == INVALID_HANDLE)
         return false;
      FileWriteString(handle, "row,diagnostic\r\n");
      for(int i=0; i<ArraySize(diagnostics); i++)
         FileWriteString(handle, IntegerToString(i+1) + "," + CGRK_CsvEscape(diagnostics[i]) + "\r\n");
      FileClose(handle);
      return true;
   }

   bool WriteHtmlDashboard(const string file_name, SCGRKReportRow &rows[], const int top_rows)
   {
      int handle = FileOpen(file_name, FILE_WRITE | FILE_TXT | FILE_ANSI);
      if(handle == INVALID_HANDLE)
         return false;

      string html = "";
      html += "<!doctype html><html><head><meta charset='utf-8'>";
      html += "<title>EXP0017 Phase09 Ranking Dashboard</title>";
      html += "<style>body{font-family:Arial,sans-serif;background:#111;color:#eee;padding:24px;}table{border-collapse:collapse;width:100%;font-size:13px;}th,td{border:1px solid #444;padding:6px;}th{background:#222;}tr:nth-child(even){background:#181818}.A{color:#6f6}.B{color:#9f9}.C{color:#ff6}.D{color:#fa6}.F{color:#f66}</style>";
      html += "</head><body>";
      html += "<h1>EXP0017 Phase 09 — Statistical Ranking Dashboard</h1>";
      html += "<p>This dashboard is research evidence only. It does not change the strategy, place orders, filter cycle groups, alter risk, or authorize execution.</p>";
      html += "<table><tr><th>Rank</th><th>Report</th><th>Bucket</th><th>Samples</th><th>Win%</th><th>Avg R</th><th>Stop%</th><th>Stop Streak</th><th>Quality</th><th>Grade</th><th>Shortlist</th><th>Flags</th></tr>";

      int n = MathMin(top_rows, ArraySize(rows));
      int rank = 0;
      for(int i=0; i<ArraySize(rows) && rank<n; i++)
      {
         if(!rows[i].eligible_for_ranking) continue;
         rank++;
         string grade_class = rows[i].grade;
         html += "<tr>";
         html += "<td>" + IntegerToString(rank) + "</td>";
         html += "<td>" + rows[i].report_name + "</td>";
         html += "<td>" + rows[i].bucket_key + "</td>";
         html += "<td>" + IntegerToString(rows[i].sample_count) + "</td>";
         html += "<td>" + DoubleToString(rows[i].win_rate_percent,2) + "</td>";
         html += "<td>" + DoubleToString(rows[i].avg_r,4) + "</td>";
         html += "<td>" + DoubleToString(rows[i].stop_rate_percent,2) + "</td>";
         html += "<td>" + IntegerToString(rows[i].max_stop_streak) + "</td>";
         html += "<td>" + DoubleToString(rows[i].quality_score,2) + "</td>";
         html += "<td class='" + grade_class + "'>" + rows[i].grade + "</td>";
         html += "<td>" + (rows[i].eligible_for_shortlist ? "yes" : "no") + "</td>";
         html += "<td>" + rows[i].red_flag_text + "</td>";
         html += "</tr>";
      }

      html += "</table></body></html>";
      FileWriteString(handle, html);
      FileClose(handle);
      return true;
   }
};

#endif
