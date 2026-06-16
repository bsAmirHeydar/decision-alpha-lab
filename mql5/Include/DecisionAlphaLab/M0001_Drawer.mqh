//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0001 Debug Package Drawer                  |
//| Package-based visual audit layers for live RTV validation.        |
//+------------------------------------------------------------------+

string DAL_Sanitize(string value)
{
   StringReplace(value, "#", "IDX");
   StringReplace(value, ".", "_");
   StringReplace(value, "/", "_");
   StringReplace(value, "\\", "_");
   StringReplace(value, " ", "_");
   StringReplace(value, ":", "_");
   return value;
}

void DAL_DeleteObjects(string prefix)
{
   for(int i = ObjectsTotal(0, -1, -1) - 1; i >= 0; i--)
   {
      string name = ObjectName(0, i, -1, -1);
      if(StringFind(name, prefix) == 0)
         ObjectDelete(0, name);
   }
}

string DAL_TimeToId(datetime value)
{
   return IntegerToString((long)value);
}

string DAL_PriceText(double value)
{
   return DoubleToString(value, _Digits);
}

string DAL_RtvText(double value)
{
   return DoubleToString(value, 3);
}

color DAL_RtvColor(double rtv, bool open_event=false)
{
   if(open_event)
      return clrDodgerBlue;
   if(rtv >= 1.25)
      return clrGold;
   if(rtv <= 0.90)
      return clrDeepPink;
   return clrAqua;
}

color DAL_NodeColor(int node_type)
{
   if(node_type == DAL_NODE_LOW)
      return clrLime;
   return clrTomato;
}

string DAL_PresetName(int preset)
{
   if(preset == DAL_PRESET_CUSTOM)          return "0 Custom";
   if(preset == DAL_PRESET_STRUCTURAL)      return "1 Structural Node Audit";
   if(preset == DAL_PRESET_TERRITORY)       return "2 Territory Construction Audit";
   if(preset == DAL_PRESET_ENTRY_EXIT)      return "3 Event Entry Exit Audit";
   if(preset == DAL_PRESET_BASELINE_INSIDE) return "4 Baseline vs Inside Sample Audit";
   if(preset == DAL_PRESET_RTV_FORMULA)     return "5 RTV Formula Audit";
   if(preset == DAL_PRESET_HUNT)            return "6 Hunt Validation Audit";
   if(preset == DAL_PRESET_LIVE_OPEN)       return "7 Live Open Event Audit";
   if(preset == DAL_PRESET_CANDLE_CLASS)    return "8 Candle Classification Audit";
   if(preset == DAL_PRESET_STATE_MACHINE)   return "9 State Machine Audit";
   if(preset == DAL_PRESET_EVENT_INSPECTOR) return "10 Focused Event Inspector";
   if(preset == DAL_PRESET_OVERVIEW)        return "11 Multi Event Overview";
   if(preset == DAL_PRESET_FULL_LAB)        return "12 Full Research Lab";
   return "Unknown";
}

void DAL_ResetVisualFlags(DAL_DrawOptions &opt)
{
   opt.only_selected_event = false;
   opt.only_open_events = false;
   opt.only_closed_events = false;
   opt.only_hunted_events = false;
   opt.only_strong_rtv = false;

   opt.show_nodes = false;
   opt.show_node_labels = false;
   opt.show_node_price_line = false;
   opt.show_active_from_line = false;
   opt.show_confirmation_window = false;

   opt.show_expansion_extreme = false;
   opt.show_expansion_distance = false;
   opt.show_territory_bounds = false;
   opt.show_territory_fill = false;
   opt.show_zone_ratio_label = false;

   opt.show_event_window = false;
   opt.show_entry_marker = false;
   opt.show_exit_marker = false;
   opt.show_outside_counter = false;

   opt.show_before_candles = false;
   opt.show_inside_candles = false;
   opt.show_outside_active_candles = false;
   opt.show_sample_legend = false;

   opt.show_rtv_label = false;
   opt.show_formula_panel = false;
   opt.show_mean_inside = false;
   opt.show_mean_before = false;
   opt.show_medians = false;
   opt.show_counts = false;

   opt.show_hunt_marker = false;
   opt.show_hunt_label = false;

   opt.show_open_event = false;
   opt.show_live_rtv = false;
   opt.show_live_counts = false;

   opt.show_candle_table = false;
   opt.show_logmove_values = false;
   opt.show_classification_flags = false;

   opt.show_state_timeline = false;
   opt.show_state_labels = false;
   opt.show_transition_markers = false;
   opt.show_current_state = false;

   opt.show_inspector_card = false;
   opt.show_inspector_table = false;
   opt.auto_focus_chart = false;

   opt.show_summary_panel = false;
   opt.render_light_mode = false;
}

void DAL_ApplyPreset(DAL_DrawOptions &opt)
{
   if(opt.view_preset == DAL_PRESET_CUSTOM)
      return;

   DAL_ResetVisualFlags(opt);

   if(opt.view_preset == DAL_PRESET_STRUCTURAL)
   {
      opt.show_nodes = true;
      opt.show_node_labels = true;
      opt.show_node_price_line = true;
      opt.show_active_from_line = true;
      opt.show_confirmation_window = true;
      opt.show_summary_panel = true;
      return;
   }

   if(opt.view_preset == DAL_PRESET_TERRITORY)
   {
      opt.only_selected_event = true;
      opt.show_nodes = true;
      opt.show_node_labels = true;
      opt.show_node_price_line = true;
      opt.show_expansion_extreme = true;
      opt.show_expansion_distance = true;
      opt.show_territory_bounds = true;
      opt.show_territory_fill = true;
      opt.show_zone_ratio_label = true;
      opt.show_inspector_card = true;
      return;
   }

   if(opt.view_preset == DAL_PRESET_ENTRY_EXIT)
   {
      opt.only_selected_event = true;
      opt.show_event_window = true;
      opt.show_entry_marker = true;
      opt.show_exit_marker = true;
      opt.show_outside_counter = true;
      opt.show_rtv_label = true;
      opt.show_inspector_card = true;
      return;
   }

   if(opt.view_preset == DAL_PRESET_BASELINE_INSIDE)
   {
      opt.only_selected_event = true;
      opt.show_event_window = true;
      opt.show_before_candles = true;
      opt.show_inside_candles = true;
      opt.show_outside_active_candles = true;
      opt.show_sample_legend = true;
      opt.show_counts = true;
      opt.show_inspector_card = true;
      return;
   }

   if(opt.view_preset == DAL_PRESET_RTV_FORMULA)
   {
      opt.only_selected_event = true;
      opt.show_event_window = true;
      opt.show_rtv_label = true;
      opt.show_formula_panel = true;
      opt.show_mean_inside = true;
      opt.show_mean_before = true;
      opt.show_medians = true;
      opt.show_counts = true;
      opt.show_inspector_card = true;
      return;
   }

   if(opt.view_preset == DAL_PRESET_HUNT)
   {
      opt.only_selected_event = true;
      opt.only_hunted_events = true;
      opt.focus_mode = DAL_FOCUS_LATEST_HUNTED;
      opt.show_event_window = true;
      opt.show_node_price_line = true;
      opt.show_hunt_marker = true;
      opt.show_hunt_label = true;
      opt.show_entry_marker = true;
      opt.show_exit_marker = true;
      opt.show_inspector_card = true;
      return;
   }

   if(opt.view_preset == DAL_PRESET_LIVE_OPEN)
   {
      opt.only_selected_event = true;
      opt.only_open_events = true;
      opt.focus_mode = DAL_FOCUS_LATEST_OPEN;
      opt.show_open_event = true;
      opt.show_live_rtv = true;
      opt.show_live_counts = true;
      opt.show_event_window = true;
      opt.show_rtv_label = true;
      opt.show_before_candles = true;
      opt.show_inside_candles = true;
      opt.show_outside_active_candles = true;
      opt.show_inspector_card = true;
      return;
   }

   if(opt.view_preset == DAL_PRESET_CANDLE_CLASS)
   {
      opt.only_selected_event = true;
      opt.show_event_window = true;
      opt.show_before_candles = true;
      opt.show_inside_candles = true;
      opt.show_outside_active_candles = true;
      opt.show_candle_table = true;
      opt.show_logmove_values = true;
      opt.show_classification_flags = true;
      opt.show_inspector_card = true;
      return;
   }

   if(opt.view_preset == DAL_PRESET_STATE_MACHINE)
   {
      opt.only_selected_event = true;
      opt.show_event_window = true;
      opt.show_state_timeline = true;
      opt.show_state_labels = true;
      opt.show_transition_markers = true;
      opt.show_current_state = true;
      opt.show_entry_marker = true;
      opt.show_exit_marker = true;
      opt.show_hunt_marker = true;
      opt.show_inspector_card = true;
      return;
   }

   if(opt.view_preset == DAL_PRESET_EVENT_INSPECTOR)
   {
      opt.only_selected_event = true;
      opt.show_nodes = true;
      opt.show_node_labels = true;
      opt.show_node_price_line = true;
      opt.show_expansion_extreme = true;
      opt.show_territory_bounds = true;
      opt.show_territory_fill = true;
      opt.show_event_window = true;
      opt.show_entry_marker = true;
      opt.show_exit_marker = true;
      opt.show_before_candles = true;
      opt.show_inside_candles = true;
      opt.show_outside_active_candles = true;
      opt.show_rtv_label = true;
      opt.show_formula_panel = true;
      opt.show_hunt_marker = true;
      opt.show_hunt_label = true;
      opt.show_candle_table = true;
      opt.show_state_timeline = true;
      opt.show_inspector_card = true;
      opt.show_inspector_table = true;
      return;
   }

   if(opt.view_preset == DAL_PRESET_OVERVIEW)
   {
      opt.show_nodes = true;
      opt.show_event_window = true;
      opt.show_rtv_label = true;
      opt.show_hunt_marker = true;
      opt.show_summary_panel = true;
      opt.only_strong_rtv = false;
      opt.render_light_mode = true;
      return;
   }

   if(opt.view_preset == DAL_PRESET_FULL_LAB)
   {
      opt.show_nodes = true;
      opt.show_node_labels = true;
      opt.show_node_price_line = true;
      opt.show_active_from_line = true;
      opt.show_confirmation_window = true;
      opt.show_expansion_extreme = true;
      opt.show_expansion_distance = true;
      opt.show_territory_bounds = true;
      opt.show_territory_fill = true;
      opt.show_zone_ratio_label = true;
      opt.show_event_window = true;
      opt.show_entry_marker = true;
      opt.show_exit_marker = true;
      opt.show_outside_counter = true;
      opt.show_before_candles = true;
      opt.show_inside_candles = true;
      opt.show_outside_active_candles = true;
      opt.show_sample_legend = true;
      opt.show_rtv_label = true;
      opt.show_formula_panel = true;
      opt.show_mean_inside = true;
      opt.show_mean_before = true;
      opt.show_medians = true;
      opt.show_counts = true;
      opt.show_hunt_marker = true;
      opt.show_hunt_label = true;
      opt.show_open_event = true;
      opt.show_live_rtv = true;
      opt.show_live_counts = true;
      opt.show_candle_table = true;
      opt.show_logmove_values = true;
      opt.show_classification_flags = true;
      opt.show_state_timeline = true;
      opt.show_state_labels = true;
      opt.show_transition_markers = true;
      opt.show_current_state = true;
      opt.show_inspector_card = true;
      opt.show_inspector_table = true;
      opt.show_summary_panel = true;
      return;
   }
}

datetime DAL_CandleEndTime(MqlRates &rates[], int bars, int index)
{
   if(index + 1 < bars)
      return rates[index + 1].time;
   int sec = PeriodSeconds(_Period);
   if(sec <= 0)
      sec = 60;
   return rates[index].time + sec;
}

void DAL_DrawTextAt(string name, datetime time, double price, string text, color clr, int font_size=8, int anchor=ANCHOR_CENTER)
{
   ObjectCreate(0, name, OBJ_TEXT, 0, time, price);
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetString(0, name, OBJPROP_FONT, "Consolas");
   ObjectSetInteger(0, name, OBJPROP_ANCHOR, anchor);
}

void DAL_DrawPanel(string name, int corner, int x, int y, string text, color clr=clrAqua, int font_size=9)
{
   ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0);
   ObjectSetInteger(0, name, OBJPROP_CORNER, corner);
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetString(0, name, OBJPROP_FONT, "Consolas");
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetString(0, name, OBJPROP_TEXT, text);
}

void DAL_DrawVerticalLine(string name, datetime time, color clr, int style=STYLE_DOT, int width=1)
{
   ObjectCreate(0, name, OBJ_VLINE, 0, time, 0);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   ObjectSetInteger(0, name, OBJPROP_BACK, true);
}

void DAL_DrawPriceSegment(string name, datetime t1, datetime t2, double price, color clr, int style=STYLE_SOLID, int width=1, bool back=true)
{
   ObjectCreate(0, name, OBJ_TREND, 0, t1, price, t2, price);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, false);
   ObjectSetInteger(0, name, OBJPROP_RAY_LEFT, false);
   ObjectSetInteger(0, name, OBJPROP_BACK, back);
}

void DAL_DrawBox(string name, datetime t1, datetime t2, double upper, double lower, color clr, int style=STYLE_SOLID, int width=1, bool fill=false, bool back=true)
{
   ObjectCreate(0, name, OBJ_RECTANGLE, 0, t1, upper, t2, lower);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   ObjectSetInteger(0, name, OBJPROP_BACK, back);
   ObjectSetInteger(0, name, OBJPROP_FILL, fill);
}

void DAL_DrawArrow(string name, datetime time, double price, int code, color clr, int width=1, string tooltip="")
{
   ObjectCreate(0, name, OBJ_ARROW, 0, time, price);
   ObjectSetInteger(0, name, OBJPROP_ARROWCODE, code);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   if(tooltip != "")
      ObjectSetString(0, name, OBJPROP_TOOLTIP, tooltip);
}

void DAL_DrawNodeBasic(string prefix, DAL_Node &node, MqlRates &rates[], int bars, DAL_DrawOptions &opt)
{
   if(node.index < 0 || node.index >= bars)
      return;

   string base = prefix + "P1_NODE_" + IntegerToString(node.id) + "_";
   int arrow = (node.type == DAL_NODE_LOW ? 233 : 234);
   DAL_DrawArrow(base + "ARROW", node.time, node.price, arrow, DAL_NodeColor(node.type), 1,
                 "node_id=" + IntegerToString(node.id) + " type=" + DAL_NodeTypeText(node.type));

   if(opt.show_node_labels)
      DAL_DrawTextAt(base + "LABEL", node.time, node.price, "N" + IntegerToString(node.id) + " " + DAL_NodeTypeText(node.type), DAL_NodeColor(node.type), 7, ANCHOR_LEFT);

   if(opt.show_node_price_line)
      DAL_DrawPriceSegment(base + "PRICE", node.time, rates[bars - 1].time, node.price, DAL_NodeColor(node.type), STYLE_DOT, 1, true);

   if(opt.show_active_from_line && node.active_from >= 0 && node.active_from < bars)
   {
      DAL_DrawVerticalLine(base + "ACTIVE", rates[node.active_from].time, clrDodgerBlue, STYLE_DOT, 1);
      DAL_DrawTextAt(base + "ACTIVE_LABEL", rates[node.active_from].time, node.price, "active_from", clrDodgerBlue, 7, ANCHOR_LEFT);
   }

   if(opt.show_confirmation_window && node.active_from > node.index && node.active_from < bars)
   {
      double hi = rates[node.index].high;
      double lo = rates[node.index].low;
      for(int i = node.index; i <= node.active_from && i < bars; i++)
      {
         hi = MathMax(hi, rates[i].high);
         lo = MathMin(lo, rates[i].low);
      }
      DAL_DrawBox(base + "CONFIRM", rates[node.index].time, rates[node.active_from].time, hi, lo, clrDimGray, STYLE_DOT, 1, false, true);
   }
}

int DAL_FindFocusEvent(DAL_Event &events[], DAL_DrawOptions &opt)
{
   int total = ArraySize(events);
   if(total <= 0)
      return -1;

   if(opt.selected_node_id >= 0)
   {
      for(int i = total - 1; i >= 0; i--)
      {
         if(events[i].node_id != opt.selected_node_id)
            continue;
         if(opt.selected_revisit_id >= 0 && events[i].revisit_id != opt.selected_revisit_id)
            continue;
         return i;
      }
   }

   if(opt.focus_mode == DAL_FOCUS_LATEST_OPEN)
   {
      for(int i = total - 1; i >= 0; i--)
         if(events[i].is_open)
            return i;
   }

   if(opt.focus_mode == DAL_FOCUS_LATEST_HUNTED)
   {
      for(int i = total - 1; i >= 0; i--)
         if(events[i].hunted)
            return i;
   }

   if(opt.focus_mode == DAL_FOCUS_STRONGEST_RTV)
   {
      int best = -1;
      double best_rtv = -1.0;
      for(int i = 0; i < total; i++)
      {
         if(events[i].rtv > best_rtv)
         {
            best_rtv = events[i].rtv;
            best = i;
         }
      }
      return best;
   }

   if(opt.focus_mode == DAL_FOCUS_LATEST_CLOSED)
   {
      for(int i = total - 1; i >= 0; i--)
         if(!events[i].is_open)
            return i;
   }

   return total - 1;
}

bool DAL_EventPassesFilter(DAL_Event &event, DAL_DrawOptions &opt, int event_index, int focus_index)
{
   if(opt.only_selected_event && event_index != focus_index)
      return false;
   if(opt.only_open_events && !event.is_open)
      return false;
   if(opt.only_closed_events && event.is_open)
      return false;
   if(opt.only_hunted_events && !event.hunted)
      return false;
   if(opt.only_strong_rtv && event.rtv < opt.strong_rtv_threshold)
      return false;
   if(opt.min_rtv > 0.0 && event.rtv < opt.min_rtv)
      return false;
   if(opt.max_rtv > 0.0 && event.rtv > opt.max_rtv)
      return false;
   return true;
}

bool DAL_IndexInEvent(int index, DAL_Event &event)
{
   return index >= event.entry_index && index <= event.exit_index;
}

void DAL_DrawEventCore(string prefix, DAL_Event &event, MqlRates &rates[], int bars, DAL_DrawOptions &opt, bool focused)
{
   string base = prefix + "EV_" + IntegerToString(event.node_id) + "_" + IntegerToString(event.revisit_id) + "_" + DAL_TimeToId(event.entry_time) + "_";
   datetime t1 = event.entry_time;
   datetime t2 = event.exit_time;
   if(event.exit_index >= 0 && event.exit_index < bars)
      t2 = DAL_CandleEndTime(rates, bars, event.exit_index);

   color rtv_clr = DAL_RtvColor(event.rtv, event.is_open);
   int width = focused ? 2 : 1;

   if(opt.show_territory_fill)
      DAL_DrawBox(base + "TERR_FILL", t1, t2, event.territory_upper, event.territory_lower, clrDarkSlateGray, STYLE_SOLID, 1, false, true);

   if(opt.show_territory_bounds)
   {
      DAL_DrawPriceSegment(base + "TERR_UPPER", t1, t2, event.territory_upper, clrAqua, STYLE_DOT, 1, true);
      DAL_DrawPriceSegment(base + "TERR_LOWER", t1, t2, event.territory_lower, clrAqua, STYLE_DOT, 1, true);
   }

   if(opt.show_event_window)
      DAL_DrawBox(base + "WINDOW", t1, t2, event.territory_upper, event.territory_lower, rtv_clr, focused ? STYLE_SOLID : STYLE_DASH, width, false, false);

   if(opt.show_node_price_line)
      DAL_DrawPriceSegment(base + "NODE_PRICE", rates[event.node_index].time, t2, event.node_price, DAL_NodeColor(event.node_type), STYLE_DOT, focused ? 2 : 1, true);

   if(opt.show_expansion_extreme)
   {
      DAL_DrawPriceSegment(base + "EXTREME", rates[event.node_index].time, t1, event.expansion_extreme, clrOrange, STYLE_SOLID, 1, true);
      DAL_DrawTextAt(base + "EXTREME_LABEL", t1, event.expansion_extreme, "extreme " + DAL_PriceText(event.expansion_extreme), clrOrange, 7, ANCHOR_LEFT);
   }

   if(opt.show_expansion_distance)
   {
      datetime mid = rates[event.node_index].time + (t1 - rates[event.node_index].time) / 2;
      double mid_price = (event.expansion_extreme + event.node_price) * 0.5;
      DAL_DrawTextAt(base + "DIST", mid, mid_price, "dist=" + DAL_PriceText(MathAbs(event.expansion_extreme - event.node_price)), clrOrange, 7, ANCHOR_CENTER);
   }

   if(opt.show_zone_ratio_label)
      DAL_DrawTextAt(base + "ZONE_RATIO", t1, event.territory_lower, "zone ratio active", clrAqua, 7, ANCHOR_UPPER);

   if(opt.show_entry_marker)
   {
      double p = (event.node_type == DAL_NODE_LOW ? rates[event.entry_index].low : rates[event.entry_index].high);
      DAL_DrawArrow(base + "ENTRY", event.entry_time, p, 159, clrLime, focused ? 2 : 1, "ENTRY wick touched territory");
      DAL_DrawTextAt(base + "ENTRY_LABEL", event.entry_time, p, "ENTRY", clrLime, 7, ANCHOR_RIGHT);
   }

   if(opt.show_exit_marker)
   {
      double p = (event.node_type == DAL_NODE_LOW ? rates[event.exit_index].low : rates[event.exit_index].high);
      DAL_DrawArrow(base + "EXIT", event.exit_time, p, 159, clrOrangeRed, focused ? 2 : 1, "EXIT outside_count >= exit_gap");
      DAL_DrawTextAt(base + "EXIT_LABEL", event.exit_time, p, "EXIT", clrOrangeRed, 7, ANCHOR_LEFT);
   }

   if(opt.show_rtv_label)
   {
      datetime mid_time = event.entry_time + (event.exit_time - event.entry_time) / 2;
      string live = event.is_open ? "LIVE " : "";
      DAL_DrawTextAt(base + "RTV", mid_time, event.territory_upper, live + "RTV " + DoubleToString(event.rtv, 2), rtv_clr, focused ? 10 : 8, ANCHOR_LOWER);
   }

   if(opt.show_hunt_marker && event.hunted && event.hunt_time > 0)
   {
      DAL_DrawArrow(base + "HUNT", event.hunt_time, event.hunt_price, 251, clrRed, focused ? 3 : 2, "HUNT first breach");
      if(opt.show_hunt_label)
         DAL_DrawTextAt(base + "HUNT_LABEL", event.hunt_time, event.hunt_price, "HUNT", clrRed, 8, ANCHOR_LEFT);
   }
}

void DAL_DrawSampleCandles(string prefix, DAL_Event &event, MqlRates &rates[], int bars, DAL_DrawOptions &opt)
{
   string base = prefix + "SAMPLE_" + IntegerToString(event.node_id) + "_" + IntegerToString(event.revisit_id) + "_" + DAL_TimeToId(event.entry_time) + "_";
   int n = event.event_length;
   if(n <= 0)
      n = MathMax(1, event.exit_index - event.entry_index + 1);

   int before_start = MathMax(0, event.entry_index - n);
   int before_end = event.entry_index - 1;

   if(opt.show_before_candles)
   {
      for(int i = before_start; i <= before_end && i < bars; i++)
         DAL_DrawBox(base + "BEFORE_" + IntegerToString(i), rates[i].time, DAL_CandleEndTime(rates, bars, i), rates[i].high, rates[i].low, clrViolet, STYLE_DOT, 1, false, true);
   }

   int outside_count = 0;
   for(int i = event.entry_index; i <= event.exit_index && i < bars; i++)
   {
      bool inside = DAL_InZone(rates[i].high, rates[i].low, event.territory_lower, event.territory_upper);
      if(inside)
      {
         outside_count = 0;
         if(opt.show_inside_candles)
            DAL_DrawBox(base + "INSIDE_" + IntegerToString(i), rates[i].time, DAL_CandleEndTime(rates, bars, i), rates[i].high, rates[i].low, clrAqua, STYLE_SOLID, 2, false, false);
      }
      else
      {
         outside_count++;
         if(opt.show_outside_active_candles)
            DAL_DrawBox(base + "OUTSIDE_" + IntegerToString(i), rates[i].time, DAL_CandleEndTime(rates, bars, i), rates[i].high, rates[i].low, clrOrange, STYLE_DASH, 1, false, false);
         if(opt.show_outside_counter)
            DAL_DrawTextAt(base + "OUTCNT_" + IntegerToString(i), rates[i].time, rates[i].high, "out=" + IntegerToString(outside_count), clrOrange, 7, ANCHOR_LOWER);
      }
   }
}

void DAL_DrawStateTimeline(string prefix, DAL_Event &event, MqlRates &rates[], int bars, DAL_DrawOptions &opt)
{
   string base = prefix + "STATE_" + IntegerToString(event.node_id) + "_" + IntegerToString(event.revisit_id) + "_";
   double y = event.territory_upper + (event.territory_upper - event.territory_lower) * 0.35;

   if(opt.show_transition_markers)
   {
      if(event.node_index >= 0 && event.node_index < bars)
         DAL_DrawVerticalLine(base + "NODE", rates[event.node_index].time, clrDimGray, STYLE_DOT, 1);
      DAL_DrawVerticalLine(base + "ENTRY", event.entry_time, clrLime, STYLE_DASH, 1);
      DAL_DrawVerticalLine(base + "EXIT", event.exit_time, clrOrangeRed, STYLE_DASH, 1);
   }

   if(opt.show_state_labels)
   {
      if(event.node_index >= 0 && event.node_index < bars)
         DAL_DrawTextAt(base + "NODE_L", rates[event.node_index].time, y, "NODE", clrDimGray, 7, ANCHOR_LOWER);
      DAL_DrawTextAt(base + "ENTRY_L", event.entry_time, y, "EVENT_ENTERED", clrLime, 7, ANCHOR_LOWER);
      if(event.hunted)
         DAL_DrawTextAt(base + "HUNT_L", event.hunt_time, y, "HUNTED", clrRed, 7, ANCHOR_LOWER);
      DAL_DrawTextAt(base + "EXIT_L", event.exit_time, y, event.is_open ? "OPEN" : "EXITED", event.is_open ? clrDodgerBlue : clrOrangeRed, 7, ANCHOR_LOWER);
   }

   if(opt.show_state_timeline)
      DAL_DrawPriceSegment(base + "LINE", event.entry_time, event.exit_time, y, clrSilver, STYLE_DOT, 1, true);
}

void DAL_DrawInspector(string prefix, DAL_Event &event, MqlRates &rates[], int bars, DAL_DrawOptions &opt)
{
   if(!opt.show_inspector_card && !opt.show_formula_panel && !opt.show_candle_table && !opt.show_state_timeline)
      return;

   string status = event.is_open ? "OPEN/LIVE" : "CLOSED";
   string hunted = event.hunted ? "yes" : "no";
   string text = "M0001 EVENT INSPECTOR"
               + "\nstatus=" + status
               + " | node=" + IntegerToString(event.node_id) + " " + DAL_NodeTypeText(event.node_type)
               + " | revisit=" + IntegerToString(event.revisit_id)
               + "\nentry=" + TimeToString(event.entry_time, TIME_DATE | TIME_MINUTES)
               + " | exit=" + TimeToString(event.exit_time, TIME_DATE | TIME_MINUTES)
               + "\nnode_price=" + DAL_PriceText(event.node_price)
               + " | extreme=" + DAL_PriceText(event.expansion_extreme)
               + "\nterritory=[" + DAL_PriceText(event.territory_lower) + ", " + DAL_PriceText(event.territory_upper) + "]"
               + "\ninside_n=" + IntegerToString(event.event_length)
               + " | before_n=" + IntegerToString(event.event_length)
               + "\nmean_inside=" + DoubleToString(event.mean_inside, 5)
               + " | mean_before=" + DoubleToString(event.mean_before, 5)
               + "\nmedian_inside=" + DoubleToString(event.median_inside, 5)
               + " | median_before=" + DoubleToString(event.median_before, 5)
               + "\nRTV = " + DoubleToString(event.rtv, 5)
               + "\nhunted=" + hunted;
   if(event.hunted)
      text += " | hunt_idx=" + IntegerToString(event.hunt_index) + " | hunt_price=" + DAL_PriceText(event.hunt_price);

   if(opt.show_inspector_card || opt.show_formula_panel)
      DAL_DrawPanel(prefix + "INSPECTOR", CORNER_LEFT_UPPER, 12, 78, text, clrWhite, 9);
}

void DAL_DrawCandleTable(string prefix, DAL_Event &event, MqlRates &rates[], int bars, DAL_DrawOptions &opt)
{
   if(!opt.show_candle_table)
      return;

   int max_rows = opt.max_candles_in_panel;
   if(max_rows <= 0)
      max_rows = 24;

   string text = "CANDLE CLASSIFICATION"
               + "\nidx | range | log | flags";

   int rows = 0;
   int before_start = MathMax(0, event.entry_index - event.event_length);
   int end = event.exit_index;
   int start = before_start;
   if(end - start + 1 > max_rows)
      start = MathMax(before_start, end - max_rows + 1);

   int outside_count = 0;
   for(int i = event.entry_index; i <= event.exit_index && i < bars; i++)
   {
      bool inside = DAL_InZone(rates[i].high, rates[i].low, event.territory_lower, event.territory_upper);
      if(inside) outside_count = 0; else outside_count++;
   }

   outside_count = 0;
   for(int i = start; i <= end && i < bars && rows < max_rows; i++)
   {
      bool before = (i < event.entry_index);
      bool in_zone = DAL_InZone(rates[i].high, rates[i].low, event.territory_lower, event.territory_upper);
      string flags = "";
      if(before)
         flags += "B";
      else if(in_zone)
      {
         flags += "I";
         outside_count = 0;
      }
      else
      {
         outside_count++;
         flags += "O" + IntegerToString(outside_count);
      }
      if(event.hunted && i == event.hunt_index)
         flags += " HUNT";

      double range = MathAbs(rates[i].high - rates[i].low);
      double logv = DAL_LogMove(rates[i].high, rates[i].low);
      text += "\n" + IntegerToString(i) + " | " + DoubleToString(range, _Digits) + " | " + DoubleToString(logv, 3) + " | " + flags;
      rows++;
   }

   DAL_DrawPanel(prefix + "CANDLE_TABLE", CORNER_RIGHT_UPPER, 24, 78, text, clrLightSteelBlue, 8);
}

void DAL_DrawSampleLegend(string prefix)
{
   string text = "SAMPLE LEGEND\nB before baseline = violet\nI inside sample = cyan\nO outside-active = orange\nHUNT first breach = red";
   DAL_DrawPanel(prefix + "LEGEND", CORNER_LEFT_LOWER, 12, 32, text, clrSilver, 8);
}

void DAL_DrawSummary(string prefix, MqlRates &rates[], int bars, DAL_Node &nodes[], DAL_Event &events[], DAL_DrawOptions &opt, int focus_index)
{
   int total = ArraySize(events);
   int hunted = 0;
   int open = 0;
   double sum = 0.0;
   double max_rtv = -1.0;
   double min_rtv = 999999.0;

   for(int i = 0; i < total; i++)
   {
      if(events[i].hunted) hunted++;
      if(events[i].is_open) open++;
      sum += events[i].rtv;
      if(events[i].rtv > max_rtv) max_rtv = events[i].rtv;
      if(events[i].rtv < min_rtv) min_rtv = events[i].rtv;
   }

   double mean = total > 0 ? sum / total : 0.0;
   string focus = focus_index >= 0 ? ("focus: node=" + IntegerToString(events[focus_index].node_id) + " rev=" + IntegerToString(events[focus_index].revisit_id) + " RTV=" + DoubleToString(events[focus_index].rtv, 3)) : "focus: none";

   string text = "Decision Alpha Lab | M0001 LIVE"
               + "\nPreset: " + DAL_PresetName(opt.view_preset)
               + "\nSymbol: " + _Symbol + " " + EnumToString(_Period)
               + "\nBars=" + IntegerToString(bars)
               + " | Nodes=" + IntegerToString(ArraySize(nodes))
               + " | Events=" + IntegerToString(total)
               + " | Open=" + IntegerToString(open)
               + "\nHunted=" + IntegerToString(hunted)
               + " | mean_RTV=" + DoubleToString(mean, 3)
               + " | min=" + DoubleToString(min_rtv, 3)
               + " | max=" + DoubleToString(max_rtv, 3)
               + "\n" + focus;

   if(bars > 0)
      text += "\nLast closed bar: " + TimeToString(rates[bars - 1].time, TIME_DATE | TIME_MINUTES);

   DAL_DrawPanel(prefix + "DASHBOARD", CORNER_LEFT_UPPER, 12, 16, text, clrAqua, 9);
}

int DAL_DrawRecentState(
   string prefix,
   MqlRates &rates[],
   int bars,
   DAL_Node &nodes[],
   DAL_Event &events[],
   DAL_DrawOptions &opt
)
{
   DAL_ApplyPreset(opt);

   int drawn = 0;
   int focus_index = DAL_FindFocusEvent(events, opt);

   if(opt.show_summary_panel)
   {
      DAL_DrawSummary(prefix, rates, bars, nodes, events, opt, focus_index);
      drawn++;
   }

   if(opt.show_nodes)
   {
      int nodes_total = ArraySize(nodes);
      int max_nodes = opt.max_nodes_to_draw;
      if(max_nodes <= 0)
         max_nodes = 100;
      int first_node = MathMax(0, nodes_total - max_nodes);
      for(int i = first_node; i < nodes_total; i++)
      {
         DAL_DrawNodeBasic(prefix, nodes[i], rates, bars, opt);
         drawn++;
      }
   }

   int total = ArraySize(events);
   int max_events = opt.max_events_to_draw;
   if(max_events <= 0)
      max_events = 80;

   int first_event = MathMax(0, total - max_events);
   for(int i = first_event; i < total; i++)
   {
      if(!DAL_EventPassesFilter(events[i], opt, i, focus_index))
         continue;

      bool focused = (i == focus_index);
      DAL_DrawEventCore(prefix, events[i], rates, bars, opt, focused);
      drawn++;

      if(focused || opt.only_selected_event)
      {
         DAL_DrawSampleCandles(prefix, events[i], rates, bars, opt);
         DAL_DrawStateTimeline(prefix, events[i], rates, bars, opt);
         DAL_DrawInspector(prefix, events[i], rates, bars, opt);
         DAL_DrawCandleTable(prefix, events[i], rates, bars, opt);
         if(opt.show_sample_legend)
            DAL_DrawSampleLegend(prefix);
      }
   }

   return drawn;
}
