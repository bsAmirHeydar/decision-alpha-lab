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
   if(t <= 0 || price <= 0.0 || text == "") return;
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

bool STC_DrawActiveCheckPrices(STC_Config &cfg,
                               STC_CheckCandleAudit &check,
                               double &open_price,
                               double &high_price,
                               double &low_price,
                               double &close_price)
{
   if(!STC_DrawingActiveSymbolSupported(cfg)) return false;
   if(_Symbol == cfg.symbol1)
   {
      open_price = check.symbol1.open;
      high_price = check.symbol1.high;
      low_price = check.symbol1.low;
      close_price = check.symbol1.close;
      return (high_price > 0.0 && low_price > 0.0);
   }
   if(_Symbol == cfg.symbol2)
   {
      open_price = check.symbol2.open;
      high_price = check.symbol2.high;
      low_price = check.symbol2.low;
      close_price = check.symbol2.close;
      return (high_price > 0.0 && low_price > 0.0);
   }
   return false;
}

void STC_DrawNoEntryZone(STC_Config &cfg,
                         STC_TimeSnapshot &snap,
                         const string id,
                         const int start_elapsed_minutes,
                         const int end_elapsed_minutes,
                         const string label,
                         const color clr,
                         const double top,
                         const double bottom,
                         int &created)
{
   datetime st_ny = (datetime)((long)snap.stc_day_start_ny + start_elapsed_minutes * 60);
   datetime en_ny = (datetime)((long)snap.stc_day_start_ny + end_elapsed_minutes * 60);
   datetime st = STC_NewYorkToServerUsingSnapshot(cfg, snap, st_ny);
   datetime en = STC_NewYorkToServerUsingSnapshot(cfg, snap, en_ny);
   STC_DrawRect(cfg, id, st, top, en, bottom, clr, true, true);
   STC_DrawText(cfg, id + "_TXT", st, bottom, label, clrGray, 7);
   created += 2;
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
      STC_DrawText(cfg, "TXT_" + STC_MCycleText(m), st, top, STC_MCycleText(m) + " ACTIVE", clrDimGray, 8);
      created += 2;
   }

   STC_DrawNoEntryZone(cfg, snap, "GAP_0200_0300", 360, 420, "GAP no detect/entry", clrWhiteSmoke, top, bottom, created);
   STC_DrawNoEntryZone(cfg, snap, "GAP_0900_0930", 780, 810, "GAP no detect/entry", clrWhiteSmoke, top, bottom, created);
   STC_DrawNoEntryZone(cfg, snap, "POST_1530_2000", 1170, 1440, "POST 15:30 manage/closed", clrWhiteSmoke, top, bottom, created);

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
      string wtxt = STC_MCycleText(m) + "/" + STC_WCycleText(w);
      if(w == STC_W1) wtxt = wtxt + " no-signal";
      STC_DrawText(cfg, "W_TXT_" + IntegerToString(serial), st, bottom, wtxt, clrGray, 7);
      if(serial == 11) STC_DrawVLine(cfg, "W_END_LAST", en, clrSilver, STYLE_DOT);
      created += 2;
   }

   datetime hard_ny = (datetime)((long)snap.stc_day_start_ny + STC_DAY_ACTIVE_MINUTES * 60);
   datetime hard_server = STC_NewYorkToServerUsingSnapshot(cfg, snap, hard_ny);
   STC_DrawVLine(cfg, "HARD_CLOSE_1530", hard_server, clrRed, STYLE_DASH);
   STC_DrawText(cfg, "HARD_CLOSE_1530_TXT", hard_server, top, "15:30 NY HARD CLOSE", clrRed, 8);
   created += 2;
}

void STC_DrawCurrentCheck(STC_Config &cfg, STC_TimeSnapshot &snap, int &created)
{
   if(snap.check_start_ny <= 0 || snap.check_end_ny <= 0) return;
   double pmin, pmax;
   STC_ChartPriceRange(pmin, pmax);
   datetime check_start_server = STC_NewYorkToServerUsingSnapshot(cfg, snap, snap.check_start_ny);
   datetime check_end_server = STC_NewYorkToServerUsingSnapshot(cfg, snap, snap.check_end_ny);
   color c = snap.check_entry_allowed_at_close ? clrGold : clrTomato;
   STC_DrawRect(cfg, "CURRENT_CHECK", check_start_server, pmax, check_end_server, pmin, c, false, false);
   string txt = "CHK " + IntegerToString(snap.check_index) + " " + STC_MCycleText(snap.m_cycle) + "/" + STC_WCycleText(snap.w_cycle);
   if(snap.final_check_of_m) txt = txt + " FINAL-NO-ENTRY";
   if(snap.phase == STC_PHASE_M_GAP) txt = txt + " GAP";
   if(snap.hard_close_due) txt = txt + " HARD-CLOSE-DUE";
   STC_DrawText(cfg, "CURRENT_CHECK_TXT", check_start_server, pmax, txt, c, 8);
   created += 2;
}

void STC_DrawCheckHistory(STC_Config &cfg, STC_TimeSnapshot &snap, int &created)
{
   if(!STC_DrawingActiveSymbolSupported(cfg)) return;
   int closed_index = STC_LastClosedCheckIndex(snap);
   if(closed_index < 0) return;
   int lookback = cfg.drawing_history_checks;
   if(lookback < 1) lookback = 1;
   if(lookback > 120) lookback = 120;
   int start_index = closed_index - lookback + 1;
   if(start_index < 0) start_index = 0;

   for(int idx = start_index; idx <= closed_index; idx++)
   {
      STC_CheckCandleAudit check;
      STC_BuildCheckCandleAudit(cfg, snap, idx, check);
      if(!check.start_inside_active_m || !check.pair_data_complete) continue;
      double o, h, l, cprice;
      if(!STC_DrawActiveCheckPrices(cfg, check, o, h, l, cprice)) continue;
      color c = clrSilver;
      if(check.final_check_of_m) c = clrTomato;
      else if(check.w_cycle == STC_W1) c = clrGray;
      else if(check.detection_allowed_for_signal) c = clrDimGray;
      string id = "CHKBOX_" + IntegerToString(idx) + "_" + _Symbol;
      STC_DrawRect(cfg, id, check.check_start_server, h, check.check_end_server, l, c, false, false);
      created++;

      int w_start_elapsed = STC_WLevel_StartElapsed(check.m_cycle, check.w_cycle);
      if(check.check_start_elapsed_minutes == w_start_elapsed)
      {
         string note = STC_MCycleText(check.m_cycle) + "/" + STC_WCycleText(check.w_cycle);
         if(check.w_cycle == STC_W1) note = note + " W1 no signal";
         STC_DrawText(cfg, id + "_WTXT", check.check_start_server, h, note, c, 7);
         created++;
      }
      if(check.final_check_of_m)
      {
         STC_DrawText(cfg, id + "_FINAL", check.check_end_server, h, "FINAL no entry", clrTomato, 7);
         created++;
      }
   }
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

void STC_DrawingPrepareReplayState(STC_RuntimeState &state)
{
   state.paper_trade_count_m1 = 0;
   state.paper_trade_count_m2 = 0;
   state.paper_trade_count_m3 = 0;
   state.paper_direction_lock_m1 = STC_DIR_NONE;
   state.paper_direction_lock_m2 = STC_DIR_NONE;
   state.paper_direction_lock_m3 = STC_DIR_NONE;
   state.started_server_time = 0;
}

void STC_DrawOutcomeForPaper(STC_Config &cfg,
                             STC_TimeSnapshot &snap,
                             STC_PaperEntryAudit &paper,
                             const int closed_index,
                             const string base,
                             int &created)
{
   if(!paper.is_paper_entry) return;
   STC_PaperOutcomeAudit outcome;
   STC_SimulateOutcomeFromPaper(cfg, snap, paper, closed_index, outcome);
   if(outcome.outcome_status == STC_OUTCOME_TP_HIT || outcome.outcome_status == STC_OUTCOME_SL_HIT || outcome.outcome_status == STC_OUTCOME_AMBIGUOUS_SL_TP_SAME_CHECK)
   {
      datetime exit_server = STC_NewYorkToServerUsingSnapshot(cfg, snap, outcome.exit_check_end_ny);
      double y = outcome.exit_price;
      string label = "";
      color c = clrSilver;
      if(outcome.outcome_status == STC_OUTCOME_TP_HIT)
      {
         label = "TP hit";
         c = clrLimeGreen;
      }
      else if(outcome.outcome_status == STC_OUTCOME_SL_HIT)
      {
         label = "SL hit";
         c = clrRed;
      }
      else
      {
         label = "AMBIG SL+TP";
         c = clrMagenta;
         y = paper.entry_price;
      }
      STC_DrawVLine(cfg, base + "_OUTCOME_V", exit_server, c, STYLE_DASHDOT);
      STC_DrawText(cfg, base + "_OUTCOME_TXT", exit_server, y, label, c, 8);
      created += 2;
   }
   else if(outcome.outcome_status == STC_OUTCOME_OPEN_UNRESOLVED)
   {
      datetime t = snap.server_time;
      if(t <= paper.entry_check_start_server) t = paper.entry_check_end_server;
      STC_DrawText(cfg, base + "_OPEN_TXT", t, paper.entry_price, "OPEN unresolved", clrSilver, 7);
      created++;
   }
}

void STC_DrawPaperEntryFromCandidate(STC_Config &cfg,
                                     STC_RuntimeState &replay_state,
                                     STC_TimeSnapshot &snap,
                                     STC_SMTCandidateAudit &candidate,
                                     const int closed_index,
                                     int &created)
{
   if(!candidate.is_trade_candidate) return;
   if(candidate.trade_symbol != _Symbol) return;

   STC_SignalAudit signal;
   STC_FinalizeSignalFromCandidate(cfg, replay_state, candidate, signal);
   STC_PaperEntryAudit paper;
   STC_FillPaperFromSignal(cfg, replay_state, snap, signal, paper);

   color c = STC_DrawSignalColor(candidate.direction);
   string base = "PAPER_" + IntegerToString(candidate.check_index) + "_" + STC_DirectionText(candidate.direction) + "_" + candidate.trade_symbol;
   string sig_txt = "SMT " + STC_DirectionText(candidate.direction) + " clean=" + candidate.clean_symbol + " hunted=" + candidate.hunted_symbol + " ref=" + STC_WCycleText(candidate.selected_reference_w_cycle);
   STC_DrawText(cfg, base + "_SIGNAL", candidate.check_end_server, candidate.selected_reference_price, sig_txt, c, 8);
   STC_DrawVLine(cfg, base + "_CONFIRM", candidate.check_end_server, c, STYLE_DOT);
   created += 2;

   STC_WLevelAudit ref_w;
   STC_BuildWLevelAudit(cfg, snap, candidate.selected_reference_w_serial, ref_w);
   if(ref_w.w_start_server > 0 && ref_w.w_end_server > 0)
   {
      STC_DrawTrend(cfg, base + "_SELECTED_REF", ref_w.w_start_server, candidate.selected_reference_price, candidate.check_end_server, candidate.selected_reference_price, c, 2, STYLE_DASHDOT);
      created++;
   }

   if(!paper.is_paper_entry)
   {
      STC_DrawText(cfg, base + "_REJECTED", candidate.check_end_server, candidate.selected_reference_price, "PLAN REJECTED: " + paper.status, clrOrange, 7);
      created++;
      return;
   }

   datetime line_end = snap.server_time;
   if(line_end <= paper.entry_check_start_server)
      line_end = paper.entry_check_end_server;

   string txt = STC_DirectionText(paper.direction) + " ENTRY " + paper.trade_symbol + " R=" + DoubleToString(cfg.final_reward_r, 1);
   STC_DrawText(cfg, base + "_ENTRY", paper.entry_check_start_server, paper.entry_price, txt, c, 9);
   STC_DrawTrend(cfg, base + "_SL", paper.entry_check_start_server, paper.stop_price, line_end, paper.stop_price, clrRed, 1, STYLE_DASH);
   STC_DrawTrend(cfg, base + "_TP", paper.entry_check_start_server, paper.take_profit_price, line_end, paper.take_profit_price, clrLimeGreen, 1, STYLE_DASH);
   STC_DrawTrend(cfg, base + "_ENTRY_LINE", paper.entry_check_start_server, paper.entry_price, line_end, paper.entry_price, c, 1, STYLE_DOT);
   STC_DrawText(cfg, base + "_SLTXT", paper.entry_check_start_server, paper.stop_price, "SL selected W ref", clrRed, 7);
   STC_DrawText(cfg, base + "_TPTXT", paper.entry_check_start_server, paper.take_profit_price, "TP " + DoubleToString(cfg.final_reward_r, 1) + "R", clrLimeGreen, 7);
   created += 6;

   if(cfg.partial_enabled && paper.m_cycle != STC_M3)
   {
      int partial_elapsed = STC_WLevel_EndElapsed(paper.m_cycle, STC_W4);
      if(partial_elapsed > 0)
      {
         datetime partial_ny = (datetime)((long)snap.stc_day_start_ny + partial_elapsed * 60);
         datetime partial_server = STC_NewYorkToServerUsingSnapshot(cfg, snap, partial_ny);
         STC_DrawVLine(cfg, base + "_PARTIAL_V", partial_server, clrDarkOrange, STYLE_DOT);
         STC_DrawText(cfg, base + "_PARTIAL", partial_server, paper.entry_price, "W4 partial 50%", clrDarkOrange, 8);
         created += 2;
      }
   }
   else if(paper.m_cycle == STC_M3)
   {
      STC_DrawText(cfg, base + "_NO_M3_PARTIAL", paper.entry_check_start_server, paper.entry_price, "M3: no partial; 15:30 HC", clrDarkOrange, 7);
      created++;
   }

   datetime hard_ny = (datetime)((long)snap.stc_day_start_ny + STC_DAY_ACTIVE_MINUTES * 60);
   datetime hard_server = STC_NewYorkToServerUsingSnapshot(cfg, snap, hard_ny);
   STC_DrawText(cfg, base + "_HC_MARK", hard_server, paper.entry_price, "HC if open", clrRed, 7);
   created++;

   STC_DrawOutcomeForPaper(cfg, snap, paper, closed_index, base, created);
}

void STC_DrawRawHuntMarker(STC_Config &cfg,
                           STC_ReferenceHuntAudit &raw,
                           const bool high_side,
                           const bool active_hunted,
                           const bool exactly_one,
                           const bool active_is_clean,
                           const bool both_hunted,
                           const double ref_price,
                           int &created)
{
   if(ref_price <= 0.0) return;
   string side_txt = high_side ? "H" : "L";
   color c = high_side ? clrTomato : clrLimeGreen;
   string id = "HUNT_" + IntegerToString(raw.check_index) + "_R" + IntegerToString(raw.reference_rank) + "_" + side_txt + "_" + _Symbol;
   string txt = "";
   if(both_hunted)
      txt = "BOTH " + side_txt + " no SMT";
   else if(active_hunted)
      txt = side_txt + " HUNT ref=" + STC_WCycleText(raw.reference_w_cycle) + " " + (high_side ? STC_HuntPatternText(raw.high_hunt_pattern) : STC_HuntPatternText(raw.low_hunt_pattern));
   else if(active_is_clean)
      txt = "CLEAN " + (high_side ? "SELL" : "BUY") + " ref=" + STC_WCycleText(raw.reference_w_cycle);
   else if(exactly_one)
      txt = "OTHER hunted; " + _Symbol + " clean?";

   if(txt == "") return;
   STC_DrawTrend(cfg, id + "_REF", raw.check_start_server, ref_price, raw.check_end_server, ref_price, c, 1, STYLE_DOT);
   STC_DrawText(cfg, id + "_TXT", raw.check_end_server, ref_price, txt, c, 7);
   created += 2;
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

   STC_RuntimeState replay_state = state;
   STC_DrawingPrepareReplayState(replay_state);
   bool use_s1 = STC_DrawingUseSymbol1(cfg);

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
         if(!raw.pair_data_complete) continue;

         bool active_high_hunt = use_s1 ? raw.s1_high_hunt : raw.s2_high_hunt;
         bool active_low_hunt = use_s1 ? raw.s1_low_hunt : raw.s2_low_hunt;
         double active_ref_high = use_s1 ? raw.s1_reference_high : raw.s2_reference_high;
         double active_ref_low = use_s1 ? raw.s1_reference_low : raw.s2_reference_low;
         bool active_clean_high = (raw.high_exactly_one_hunted && raw.high_clean_symbol == _Symbol);
         bool active_clean_low = (raw.low_exactly_one_hunted && raw.low_clean_symbol == _Symbol);
         bool both_high = (raw.high_hunt_pattern == STC_HUNT_BOTH);
         bool both_low = (raw.low_hunt_pattern == STC_HUNT_BOTH);

         STC_DrawRawHuntMarker(cfg, raw, true, active_high_hunt, raw.high_exactly_one_hunted, active_clean_high, both_high, active_ref_high, created);
         STC_DrawRawHuntMarker(cfg, raw, false, active_low_hunt, raw.low_exactly_one_hunted, active_clean_low, both_low, active_ref_low, created);

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
         STC_DrawVLine(cfg, "AMBIG_V_" + IntegerToString(idx), check_audit.check_end_server, clrMagenta, STYLE_DASHDOT);
         STC_DrawText(cfg, "AMBIG_" + IntegerToString(idx), check_audit.check_end_server, pmax - (pmax - pmin) * 0.15, "BUY+SELL same check: FORGET", clrMagenta, 8);
         created += 2;
         continue;
      }
      if(high_count > 0)
      {
         if(has_sell_s1) STC_DrawPaperEntryFromCandidate(cfg, replay_state, snap, best_sell_s1, closed_index, created);
         if(has_sell_s2) STC_DrawPaperEntryFromCandidate(cfg, replay_state, snap, best_sell_s2, closed_index, created);
      }
      else if(low_count > 0)
      {
         if(has_buy_s1) STC_DrawPaperEntryFromCandidate(cfg, replay_state, snap, best_buy_s1, closed_index, created);
         if(has_buy_s2) STC_DrawPaperEntryFromCandidate(cfg, replay_state, snap, best_buy_s2, closed_index, created);
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
   string chart_note = "level21_visual_audit_only_no_strategy_decisions_no_orders; replay_scratch_state_does_not_mutate_runtime";
   STC_DrawZones(cfg, snap, created);
   STC_DrawCurrentCheck(cfg, snap, created);

   if(STC_DrawingActiveSymbolSupported(cfg))
   {
      STC_DrawCheckHistory(cfg, snap, created);
      STC_DrawWLevelSegments(cfg, snap, created);
      STC_DrawRecentSMT(cfg, state, snap, created);
   }
   else
   {
      chart_note = chart_note + "; chart_symbol_not_symbol1_or_symbol2_price_layers_suppressed";
   }

   string dashboard = "DAL STC LEVEL21 | " + cfg.symbol1 + "/" + cfg.symbol2
      + " | chart=" + _Symbol
      + " | NY=" + STC_TimeText(snap.ny_time)
      + " | day=" + snap.stc_day_id
      + " | " + STC_MCycleText(snap.m_cycle) + "/" + STC_WCycleText(snap.w_cycle)
      + " | CHK=" + IntegerToString(snap.check_index)
      + " | mode=" + STC_RuntimeModeText(cfg.runtime_mode);
   STC_DrawLabel(cfg, "DASHBOARD", 8, 18, dashboard, STC_DrawingActiveSymbolSupported(cfg) ? clrWhite : clrOrange);
   string sub = "visual: M/W zones + gaps + check boxes + W H/L + raw hunts + SMT plan + SL/TP + partial + outcome | real transports are input-gated";
   STC_DrawLabel(cfg, "DASHBOARD_RULES", 8, 36, sub, clrSilver);
   if(!STC_DrawingActiveSymbolSupported(cfg))
      STC_DrawLabel(cfg, "DASHBOARD_WARN", 8, 54, "Chart symbol is not Symbol1/Symbol2: price-specific W/SMT drawings suppressed.", clrOrange);
   created += STC_DrawingActiveSymbolSupported(cfg) ? 2 : 3;

   state.drawing_objects_created = created;
   state.drawing_refresh_count++;
   STC_AppendDrawingAuditCsv(cfg, state, snap, created, chart_note);
   ChartRedraw(0);
}

#endif
