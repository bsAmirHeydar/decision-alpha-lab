#ifndef __DAL_STC_DRAWING_MQH__
#define __DAL_STC_DRAWING_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_Persistence.mqh>

string STC_DrawingPrefix(STC_Config &cfg)
{
   string prefix = cfg.drawing_object_prefix;
   if(prefix == "") prefix = "DAL_STC_EXEC001";
   return STC_SafeId(prefix + "_" + cfg.symbol1 + "_" + cfg.symbol2 + "_" + IntegerToString(cfg.magic_number));
}

void STC_DeleteDrawingObjects(STC_Config &cfg)
{
   string prefix = STC_DrawingPrefix(cfg);
   int total = ObjectsTotal(0, 0, -1);
   for(int i = total - 1; i >= 0; i--)
   {
      string name = ObjectName(0, i, 0, -1);
      if(StringFind(name, prefix) == 0)
         ObjectDelete(0, name);
   }
}

bool STC_ChartPriceRange(double &pmin, double &pmax)
{
   pmin = 0.0;
   pmax = 0.0;
   bool ok_min = ChartGetDouble(0, CHART_PRICE_MIN, 0, pmin);
   bool ok_max = ChartGetDouble(0, CHART_PRICE_MAX, 0, pmax);
   if(!ok_min || !ok_max || pmax <= pmin)
   {
      double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
      if(bid <= 0.0) bid = SymbolInfoDouble(_Symbol, SYMBOL_LAST);
      if(bid <= 0.0) bid = 100.0;
      pmin = bid * 0.995;
      pmax = bid * 1.005;
   }
   if(pmax <= pmin)
      pmax = pmin + 1.0;
   return true;
}

bool STC_DrawingActiveSymbolSupported(STC_Config &cfg)
{
   return (_Symbol == cfg.symbol1 || _Symbol == cfg.symbol2);
}

bool STC_DrawingUseSymbol1(STC_Config &cfg)
{
   if(_Symbol == cfg.symbol2) return false;
   return true;
}

string STC_DrawName(STC_Config &cfg, const string suffix)
{
   return STC_DrawingPrefix(cfg) + "_" + STC_SafeId(suffix);
}

void STC_DrawSetCommon(const string name, const color clr, const int width, const ENUM_LINE_STYLE style, const bool back)
{
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_BACK, back);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTED, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
}

void STC_DrawRect(STC_Config &cfg, const string id, const datetime t1, const double p1, const datetime t2, const double p2, const color clr, const bool fill, const bool back)
{
   if(t1 <= 0 || t2 <= 0 || p1 <= 0.0 || p2 <= 0.0 || t2 <= t1) return;
   string name = STC_DrawName(cfg, id);
   if(ObjectFind(0, name) < 0)
      ObjectCreate(0, name, OBJ_RECTANGLE, 0, t1, p1, t2, p2);
   else
   {
      ObjectMove(0, name, 0, t1, p1);
      ObjectMove(0, name, 1, t2, p2);
   }
   STC_DrawSetCommon(name, clr, 1, STYLE_SOLID, back);
   ObjectSetInteger(0, name, OBJPROP_FILL, fill);
}

void STC_DrawTrend(STC_Config &cfg, const string id, const datetime t1, const double p1, const datetime t2, const double p2, const color clr, const int width, const ENUM_LINE_STYLE style)
{
   if(t1 <= 0 || t2 <= 0 || p1 <= 0.0 || p2 <= 0.0 || t2 <= t1) return;
   string name = STC_DrawName(cfg, id);
   if(ObjectFind(0, name) < 0)
      ObjectCreate(0, name, OBJ_TREND, 0, t1, p1, t2, p2);
   else
   {
      ObjectMove(0, name, 0, t1, p1);
      ObjectMove(0, name, 1, t2, p2);
   }
   STC_DrawSetCommon(name, clr, width, style, false);
   ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, false);
}

void STC_DrawVLine(STC_Config &cfg, const string id, const datetime t, const color clr, const ENUM_LINE_STYLE style)
{
   if(t <= 0) return;
   string name = STC_DrawName(cfg, id);
   if(ObjectFind(0, name) < 0)
      ObjectCreate(0, name, OBJ_VLINE, 0, t, 0.0);
   else
      ObjectMove(0, name, 0, t, 0.0);
   STC_DrawSetCommon(name, clr, 1, style, true);
}

void STC_DrawText(STC_Config &cfg, const string id, const datetime t, const double price, const string text, const color clr, const int font_size)
{
   if(t <= 0 || price <= 0.0) return;
   string name = STC_DrawName(cfg, id);
   if(ObjectFind(0, name) < 0)
      ObjectCreate(0, name, OBJ_TEXT, 0, t, price);
   else
      ObjectMove(0, name, 0, t, price);
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetString(0, name, OBJPROP_FONT, "Consolas");
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
}

void STC_DrawLabel(STC_Config &cfg, const string id, const int x, const int y, const string text, const color clr)
{
   string name = STC_DrawName(cfg, id);
   if(ObjectFind(0, name) < 0)
      ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0.0);
   ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetString(0, name, OBJPROP_FONT, "Consolas");
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 9);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
}

color STC_DrawMColor(const STC_MCycle m)
{
   if(m == STC_M1) return clrAliceBlue;
   if(m == STC_M2) return clrLavender;
   if(m == STC_M3) return clrHoneydew;
   return clrWhiteSmoke;
}

color STC_DrawSignalColor(const STC_Direction dir)
{
   if(dir == STC_DIR_BUY) return clrLimeGreen;
   if(dir == STC_DIR_SELL) return clrTomato;
   return clrSilver;
}

void STC_DrawZones(STC_Config &cfg, STC_TimeSnapshot &snap, int &created)
{
   if(snap.stc_day_start_ny <= 0) return;
   double pmin, pmax;
   STC_ChartPriceRange(pmin, pmax);
   double span = pmax - pmin;
   double top = pmax - span * 0.02;
   double bottom = pmin + span * 0.02;

   for(int mi = 1; mi <= 3; mi++)
   {
      STC_MCycle m = (STC_MCycle)mi;
      int ms = STC_WLevel_MStartElapsed(m);
      int me = ms + 360;
      datetime st_ny = (datetime)((long)snap.stc_day_start_ny + ms * 60);
      datetime en_ny = (datetime)((long)snap.stc_day_start_ny + me * 60);
      datetime st = STC_NewYorkToServerUsingSnapshot(cfg, snap, st_ny);
      datetime en = STC_NewYorkToServerUsingSnapshot(cfg, snap, en_ny);
      STC_DrawRect(cfg, "ZONE_" + STC_MCycleText(m), st, top, en, bottom, STC_DrawMColor(m), true, true);
      STC_DrawText(cfg, "TXT_" + STC_MCycleText(m), st, top, STC_MCycleText(m), clrDimGray, 8);
      created += 2;
   }

   for(int serial = 0; serial < 12; serial++)
   {
      STC_MCycle m;
      STC_WCycle w;
      if(!STC_WLevel_FromSerial(serial, m, w)) continue;
      int ws = STC_WLevel_StartElapsed(m, w);
      int we = STC_WLevel_EndElapsed(m, w);
      datetime st_ny = (datetime)((long)snap.stc_day_start_ny + ws * 60);
      datetime en_ny = (datetime)((long)snap.stc_day_start_ny + we * 60);
      datetime st = STC_NewYorkToServerUsingSnapshot(cfg, snap, st_ny);
      datetime en = STC_NewYorkToServerUsingSnapshot(cfg, snap, en_ny);
      STC_DrawVLine(cfg, "W_START_" + IntegerToString(serial), st, clrSilver, STYLE_DOT);
      STC_DrawText(cfg, "W_TXT_" + IntegerToString(serial), st, bottom, STC_MCycleText(m) + "/" + STC_WCycleText(w), clrGray, 7);
      if(serial == 11) STC_DrawVLine(cfg, "W_END_LAST", en, clrSilver, STYLE_DOT);
      created += 2;
   }

   datetime hard_ny = (datetime)((long)snap.stc_day_start_ny + 1170 * 60);
   datetime hard_server = STC_NewYorkToServerUsingSnapshot(cfg, snap, hard_ny);
   STC_DrawVLine(cfg, "HARD_CLOSE_1530", hard_server, clrRed, STYLE_DASH);
   STC_DrawText(cfg, "HARD_CLOSE_1530_TXT", hard_server, top, "15:30 HARD CLOSE", clrRed, 8);
   created += 2;
}

void STC_DrawCurrentCheck(STC_Config &cfg, STC_TimeSnapshot &snap, int &created)
{
   if(snap.check_start_ny <= 0 || snap.check_end_ny <= 0) return;
   double pmin, pmax;
   STC_ChartPriceRange(pmin, pmax);
   datetime check_start_server = STC_NewYorkToServerUsingSnapshot(cfg, snap, snap.check_start_ny);
   datetime check_end_server = STC_NewYorkToServerUsingSnapshot(cfg, snap, snap.check_end_ny);
   STC_DrawRect(cfg, "CURRENT_CHECK", check_start_server, pmax, check_end_server, pmin, clrGold, false, false);
   STC_DrawText(cfg, "CURRENT_CHECK_TXT", check_start_server, pmax, "CHK " + IntegerToString(snap.check_index) + " " + STC_MCycleText(snap.m_cycle) + "/" + STC_WCycleText(snap.w_cycle), clrGold, 8);
   created += 2;
}

void STC_DrawWLevelSegments(STC_Config &cfg, STC_TimeSnapshot &snap, int &created)
{
   if(!STC_DrawingActiveSymbolSupported(cfg)) return;
   int last_serial = STC_LastClosedWSerial(snap);
   if(last_serial < 0) return;
   int lookback = cfg.drawing_history_w_levels;
   if(lookback < 1) lookback = 1;
   if(lookback > 12) lookback = 12;
   int start_serial = last_serial - lookback + 1;
   if(start_serial < 0) start_serial = 0;
   bool use_s1 = STC_DrawingUseSymbol1(cfg);

   for(int serial = start_serial; serial <= last_serial; serial++)
   {
      STC_WLevelAudit w;
      STC_BuildWLevelAudit(cfg, snap, serial, w);
      if(!w.pair_data_complete) continue;
      double hi = use_s1 ? w.symbol1.high : w.symbol2.high;
      double lo = use_s1 ? w.symbol1.low : w.symbol2.low;
      color c = (w.w_cycle == STC_W1 ? clrDodgerBlue : (w.w_cycle == STC_W2 ? clrMediumPurple : (w.w_cycle == STC_W3 ? clrOrange : clrSlateGray)));
      string base = "WLEVEL_" + IntegerToString(serial) + "_" + _Symbol;
      STC_DrawTrend(cfg, base + "_HI", w.w_start_server, hi, w.w_end_server, hi, c, 2, STYLE_SOLID);
      STC_DrawTrend(cfg, base + "_LO", w.w_start_server, lo, w.w_end_server, lo, c, 2, STYLE_SOLID);
      STC_DrawText(cfg, base + "_HITXT", w.w_end_server, hi, STC_MCycleText(w.m_cycle) + "/" + STC_WCycleText(w.w_cycle) + " H", c, 7);
      STC_DrawText(cfg, base + "_LOTXT", w.w_end_server, lo, STC_MCycleText(w.m_cycle) + "/" + STC_WCycleText(w.w_cycle) + " L", c, 7);
      created += 4;
   }
}

void STC_DrawPaperEntryFromCandidate(STC_Config &cfg,
                                     STC_RuntimeState &state,
                                     STC_TimeSnapshot &snap,
                                     STC_SMTCandidateAudit &candidate,
                                     int &created)
{
   if(!candidate.is_trade_candidate) return;
   if(candidate.trade_symbol != _Symbol) return;

   STC_RuntimeState tmp_state = state;
   STC_SignalAudit signal;
   STC_FinalizeSignalFromCandidate(cfg, tmp_state, candidate, signal);
   STC_PaperEntryAudit paper;
   STC_FillPaperFromSignal(cfg, tmp_state, snap, signal, paper);
   if(!paper.is_paper_entry) return;

   color c = STC_DrawSignalColor(paper.direction);
   string base = "PAPER_" + IntegerToString(paper.check_index) + "_" + STC_DirectionText(paper.direction) + "_" + paper.trade_symbol;
   string txt = STC_DirectionText(paper.direction) + " " + paper.trade_symbol + " " + STC_WCycleText(paper.selected_reference_w_cycle);
   STC_DrawText(cfg, base + "_ENTRY", paper.entry_check_start_server, paper.entry_price, txt, c, 9);
   STC_DrawTrend(cfg, base + "_SL", paper.entry_check_start_server, paper.stop_price, snap.server_time, paper.stop_price, clrRed, 1, STYLE_DASH);
   STC_DrawTrend(cfg, base + "_TP", paper.entry_check_start_server, paper.take_profit_price, snap.server_time, paper.take_profit_price, clrLimeGreen, 1, STYLE_DASH);
   STC_DrawTrend(cfg, base + "_ENTRY_LINE", paper.entry_check_start_server, paper.entry_price, snap.server_time, paper.entry_price, c, 1, STYLE_DOT);
   STC_DrawText(cfg, base + "_SLTXT", paper.entry_check_start_server, paper.stop_price, "SL", clrRed, 7);
   STC_DrawText(cfg, base + "_TPTXT", paper.entry_check_start_server, paper.take_profit_price, "TP " + DoubleToString(cfg.final_reward_r, 1) + "R", clrLimeGreen, 7);

   if(cfg.partial_enabled && paper.m_cycle != STC_M3)
   {
      int partial_elapsed = STC_WLevel_EndElapsed(paper.m_cycle, STC_W4);
      if(partial_elapsed > 0)
      {
         datetime partial_ny = (datetime)((long)snap.stc_day_start_ny + partial_elapsed * 60);
         datetime partial_server = STC_NewYorkToServerUsingSnapshot(cfg, snap, partial_ny);
         STC_DrawText(cfg, base + "_PARTIAL", partial_server, paper.entry_price, "P50", clrDarkOrange, 8);
      }
   }
   created += 7;
}

void STC_DrawRecentSMT(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, int &created)
{
   if(!STC_DrawingActiveSymbolSupported(cfg)) return;
   int closed_index = STC_LastClosedCheckIndex(snap);
   if(closed_index < 0) return;
   int lookback = cfg.drawing_history_checks;
   if(lookback < 1) lookback = 1;
   if(lookback > 500) lookback = 500;
   int start_index = closed_index - lookback + 1;
   if(start_index < 0) start_index = 0;

   for(int idx = start_index; idx <= closed_index; idx++)
   {
      STC_CheckCandleAudit check_audit;
      STC_BuildCheckCandleAudit(cfg, snap, idx, check_audit);
      int legal_refs = STC_HuntReferenceCount(check_audit.w_cycle);
      if(legal_refs <= 0 || !check_audit.detection_allowed_for_signal || !check_audit.pair_data_complete)
         continue;

      int high_count = 0;
      int low_count = 0;
      bool has_sell_s1 = false, has_sell_s2 = false, has_buy_s1 = false, has_buy_s2 = false;
      STC_SMTCandidateAudit best_sell_s1, best_sell_s2, best_buy_s1, best_buy_s2;
      STC_ResetSMTCandidateAudit(best_sell_s1);
      STC_ResetSMTCandidateAudit(best_sell_s2);
      STC_ResetSMTCandidateAudit(best_buy_s1);
      STC_ResetSMTCandidateAudit(best_buy_s2);

      for(int rank = 0; rank < legal_refs; rank++)
      {
         STC_ReferenceHuntAudit raw;
         STC_BuildReferenceHuntAudit(cfg, snap, idx, rank, raw);
         if(raw.high_exactly_one_hunted)
         {
            high_count++;
            STC_SMTCandidateAudit c;
            if(STC_BuildCandidateFromRaw(cfg, snap, check_audit, raw, STC_SIDE_HIGH, c))
            {
               if(c.trade_symbol == cfg.symbol1) STC_ConsiderBestCandidate(c, has_sell_s1, best_sell_s1);
               else STC_ConsiderBestCandidate(c, has_sell_s2, best_sell_s2);
            }
         }
         if(raw.low_exactly_one_hunted)
         {
            low_count++;
            STC_SMTCandidateAudit c;
            if(STC_BuildCandidateFromRaw(cfg, snap, check_audit, raw, STC_SIDE_LOW, c))
            {
               if(c.trade_symbol == cfg.symbol1) STC_ConsiderBestCandidate(c, has_buy_s1, best_buy_s1);
               else STC_ConsiderBestCandidate(c, has_buy_s2, best_buy_s2);
            }
         }
      }

      if(high_count > 0 && low_count > 0)
      {
         double pmin, pmax; STC_ChartPriceRange(pmin, pmax);
         STC_DrawText(cfg, "AMBIG_" + IntegerToString(idx), check_audit.check_end_server, pmax - (pmax - pmin) * 0.15, "AMBIG BUY+SELL FORGOT", clrMagenta, 8);
         created++;
         continue;
      }
      if(high_count > 0)
      {
         if(has_sell_s1) STC_DrawPaperEntryFromCandidate(cfg, state, snap, best_sell_s1, created);
         if(has_sell_s2) STC_DrawPaperEntryFromCandidate(cfg, state, snap, best_sell_s2, created);
      }
      else if(low_count > 0)
      {
         if(has_buy_s1) STC_DrawPaperEntryFromCandidate(cfg, state, snap, best_buy_s1, created);
         if(has_buy_s2) STC_DrawPaperEntryFromCandidate(cfg, state, snap, best_buy_s2, created);
      }
   }
}

bool STC_AppendDrawingAuditCsv(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, const int objects_drawn, const string note)
{
   if(!cfg.write_drawing_audit) return true;
   bool exists = FileIsExist(state.drawing_audit_file_common, FILE_COMMON);
   int h = FileOpen(state.drawing_audit_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append drawing audit CSV ", state.drawing_audit_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h, "server_write_time", "strategy_id", "run_id", "chart_symbol", "symbol1", "symbol2", "stc_day_id", "ny_time", "m_cycle", "w_cycle", "check_index", "objects_drawn", "drawing_enabled", "chart_symbol_supported", "note");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h, STC_TimeText(TimeCurrent()), cfg.strategy_id, cfg.run_id, _Symbol, cfg.symbol1, cfg.symbol2, snap.stc_day_id, STC_TimeText(snap.ny_time), STC_MCycleText(snap.m_cycle), STC_WCycleText(snap.w_cycle), snap.check_index, objects_drawn, STC_BoolText(cfg.enable_drawing), STC_BoolText(STC_DrawingActiveSymbolSupported(cfg)), note);
   FileClose(h);
   return true;
}

void STC_DrawAuditLayer(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, const bool force)
{
   if(!cfg.enable_drawing) return;
   if(snap.stc_day_id == "") return;
   if(!force && state.last_drawing_server_time > 0 && snap.server_time - state.last_drawing_server_time < cfg.drawing_refresh_seconds)
      return;

   state.last_drawing_server_time = snap.server_time;
   STC_DeleteDrawingObjects(cfg);

   int created = 0;
   string chart_note = "level13_audit_drawing_no_strategy_decisions_no_orders";
   STC_DrawZones(cfg, snap, created);
   STC_DrawCurrentCheck(cfg, snap, created);

   if(STC_DrawingActiveSymbolSupported(cfg))
   {
      STC_DrawWLevelSegments(cfg, snap, created);
      STC_DrawRecentSMT(cfg, state, snap, created);
   }
   else
   {
      chart_note = chart_note + "; chart_symbol_not_symbol1_or_symbol2_price_layers_suppressed";
   }

   string dashboard = "DAL STC LEVEL13 | " + cfg.symbol1 + "/" + cfg.symbol2
      + " | chart=" + _Symbol
      + " | NY=" + STC_TimeText(snap.ny_time)
      + " | day=" + snap.stc_day_id
      + " | " + STC_MCycleText(snap.m_cycle) + "/" + STC_WCycleText(snap.w_cycle)
      + " | CHK=" + IntegerToString(snap.check_index)
      + " | no real orders";
   STC_DrawLabel(cfg, "DASHBOARD", 8, 18, dashboard, STC_DrawingActiveSymbolSupported(cfg) ? clrWhite : clrOrange);
   if(!STC_DrawingActiveSymbolSupported(cfg))
      STC_DrawLabel(cfg, "DASHBOARD_WARN", 8, 36, "Chart symbol is not Symbol1/Symbol2: price-specific W/SMT drawings suppressed.", clrOrange);
   created++;

   state.drawing_objects_created = created;
   state.drawing_refresh_count++;
   STC_AppendDrawingAuditCsv(cfg, state, snap, created, chart_note);
   ChartRedraw(0);
}

#endif
