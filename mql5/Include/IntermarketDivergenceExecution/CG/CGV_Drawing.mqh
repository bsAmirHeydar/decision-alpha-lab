#ifndef __CGV_DRAWING_MQH__
#define __CGV_DRAWING_MQH__

#include <IntermarketDivergenceExecution/CG/CGV_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGC_ConfirmationField.mqh>

class CCGV_Drawing
{
private:
   SCGVVisualLedgerConfig m_config;

   string Sanitize(const string raw)
   {
      string s=raw;
      StringReplace(s,":","_");
      StringReplace(s,".","_");
      StringReplace(s," ","_");
      StringReplace(s,"-","_");
      StringReplace(s,"|","_");
      StringReplace(s,"/","_");
      return s;
   }

   string Key(SCGCFinalSignal &signal,const string symbol,const string suffix)
   {
      return CGV_OBJECT_PREFIX + Sanitize(signal.signal_id) + "_" + Sanitize(symbol) + "_" + suffix;
   }

   bool ValidSymbolName(const string symbol)
   {
      if(symbol=="" || symbol=="NONE" || symbol=="BOTH_SYMBOLS")
         return false;
      return true;
   }

   color SignalColor(SCGCFinalSignal &signal)
   {
      if(signal.status==CGC_STATUS_INVALIDATED_DOUBLE_HUNT)
         return m_config.invalidated_color;
      if(signal.direction==CGC_DIRECTION_BUY)
         return m_config.buy_color;
      if(signal.direction==CGC_DIRECTION_SELL)
         return m_config.sell_color;
      return m_config.invalidated_color;
   }

   int StyleFromEnum(const ECGVVisualLineStyle style)
   {
      if(style==CGV_VISUAL_STYLE_DASH)       return STYLE_DASH;
      if(style==CGV_VISUAL_STYLE_DOT)        return STYLE_DOT;
      if(style==CGV_VISUAL_STYLE_DASHDOT)    return STYLE_DASHDOT;
      if(style==CGV_VISUAL_STYLE_DASHDOTDOT) return STYLE_DASHDOTDOT;
      return STYLE_SOLID;
   }

   ENUM_TIMEFRAMES VisualChartTimeframe()
   {
      if(m_config.visual_chart_timeframe==PERIOD_CURRENT)
         return (ENUM_TIMEFRAMES)_Period;
      return m_config.visual_chart_timeframe;
   }

   long FindChartForSymbol(const string symbol)
   {
      long chart_id=ChartFirst();
      while(chart_id>=0)
      {
         if(ChartSymbol(chart_id)==symbol)
            return chart_id;
         chart_id=ChartNext(chart_id);
      }

      if(m_config.open_missing_input_symbol_charts && ValidSymbolName(symbol))
      {
         SymbolSelect(symbol,true);
         long opened=ChartOpen(symbol,VisualChartTimeframe());
         return opened;
      }
      return -1;
   }

   int BrokerNyOffsetSeconds(SCGCFinalSignal &signal)
   {
      if(signal.confirmation_time_broker<=0 || signal.confirmation_time_ny<=0)
         return 0;
      return (int)(signal.confirmation_time_broker - signal.confirmation_time_ny);
   }

   datetime NyToBroker(SCGCFinalSignal &signal,const datetime ny_time)
   {
      if(ny_time<=0)
         return signal.confirmation_time_broker;
      return (datetime)(ny_time + BrokerNyOffsetSeconds(signal));
   }

   string DirectionText(SCGCFinalSignal &signal)
   {
      if(signal.direction==CGC_DIRECTION_BUY) return "BUY";
      if(signal.direction==CGC_DIRECTION_SELL) return "SELL";
      return "NONE";
   }

   string SideText(SCGCFinalSignal &signal)
   {
      if(signal.side==CGC_SIDE_HIGH) return "HIGH";
      if(signal.side==CGC_SIDE_LOW) return "LOW";
      return "NONE";
   }

   string StatusText(SCGCFinalSignal &signal)
   {
      if(signal.status==CGC_STATUS_CONFIRMED_TRADEABLE) return "CONFIRMED";
      if(signal.status==CGC_STATUS_INVALIDATED_DOUBLE_HUNT) return "INVALIDATED";
      if(signal.status==CGC_STATUS_MISSING_DATA) return "MISSING";
      return "NONE";
   }

   datetime MidTime(const datetime a,const datetime b)
   {
      if(a<=0 || b<=0 || b<a)
         return a;
      return (datetime)(a + (b-a)/2);
   }

   datetime FindExtremeTimeM1(const string symbol,const datetime start_broker,const datetime end_broker_exclusive,const ECGCSignalSide side,const datetime fallback_time)
   {
      if(!ValidSymbolName(symbol) || start_broker<=0 || end_broker_exclusive<=start_broker)
         return fallback_time;

      MqlRates rates[];
      ArraySetAsSeries(rates,false);
      // All Phase 06 cycle and confirmation boundaries are exclusive. Including
      // the bar that opens exactly at the boundary can anchor an NDX line to the
      // next cycle even though its price belongs to the prior interval.
      int copied=CopyRates(symbol,PERIOD_M1,start_broker,end_broker_exclusive-1,rates);
      if(copied<=0)
         return fallback_time;

      bool initialized=false;
      double best=0.0;
      datetime best_time=fallback_time;
      for(int i=0;i<copied;i++)
      {
         double value=(side==CGC_SIDE_LOW ? rates[i].low : rates[i].high);
         if(!initialized)
         {
            best=value;
            best_time=rates[i].time;
            initialized=true;
            continue;
         }
         if(side==CGC_SIDE_LOW)
         {
            if(value<best)
            {
               best=value;
               best_time=rates[i].time;
            }
         }
         else
         {
            if(value>best)
            {
               best=value;
               best_time=rates[i].time;
            }
         }
      }
      return best_time;
   }

   datetime SymbolReferenceTimeBroker(SCGCFinalSignal &signal,const string symbol)
   {
      if(symbol==m_config.symbol_a) return signal.symbol_a_reference_time_broker;
      if(symbol==m_config.symbol_b) return signal.symbol_b_reference_time_broker;
      return 0;
   }

   datetime SymbolCurrentExtremeTimeBroker(SCGCFinalSignal &signal,const string symbol)
   {
      if(symbol==m_config.symbol_a) return signal.symbol_a_current_extreme_time_broker;
      if(symbol==m_config.symbol_b) return signal.symbol_b_current_extreme_time_broker;
      return 0;
   }

   datetime AnchorTime(SCGCFinalSignal &signal,const ECGVAnchorTimeMode mode,const string anchor_symbol,const datetime fallback_time)
   {
      datetime ref_start=NyToBroker(signal,signal.reference_cycle_start_ny);
      datetime ref_end=NyToBroker(signal,signal.reference_cycle_end_ny);
      datetime cur_start=NyToBroker(signal,signal.current_cycle_start_ny);
      datetime cur_end=NyToBroker(signal,signal.current_cycle_end_ny);

      if(mode==CGV_ANCHOR_TIME_REFERENCE_CYCLE_START)  return ref_start;
      if(mode==CGV_ANCHOR_TIME_REFERENCE_CYCLE_MIDDLE) return MidTime(ref_start,ref_end);
      if(mode==CGV_ANCHOR_TIME_REFERENCE_CYCLE_END)    return ref_end;
      if(mode==CGV_ANCHOR_TIME_CURRENT_CYCLE_START)    return cur_start;
      if(mode==CGV_ANCHOR_TIME_CURRENT_CYCLE_END)      return cur_end;
      if(mode==CGV_ANCHOR_TIME_CONFIRMATION_CLOSE)     return signal.confirmation_time_broker;
      if(mode==CGV_ANCHOR_TIME_EXACT_REFERENCE_EXTREME)
      {
         datetime stored_reference_time=SymbolReferenceTimeBroker(signal,anchor_symbol);
         if(stored_reference_time>0)
            return stored_reference_time;
         return FindExtremeTimeM1(anchor_symbol,ref_start,ref_end,signal.side,fallback_time);
      }
      if(mode==CGV_ANCHOR_TIME_EXACT_CURRENT_EXTREME)
      {
         datetime stored_current_time=SymbolCurrentExtremeTimeBroker(signal,anchor_symbol);
         if(stored_current_time>0)
            return stored_current_time;
         datetime end_time=signal.confirmation_time_broker;
         if(end_time<=0 || (cur_end>0 && end_time>cur_end))
            end_time=cur_end;
         return FindExtremeTimeM1(anchor_symbol,cur_start,end_time,signal.side,fallback_time);
      }
      return fallback_time;
   }

   double SymbolReferencePrice(SCGCFinalSignal &signal,const string symbol)
   {
      if(symbol==m_config.symbol_a) return signal.symbol_a_reference_price;
      if(symbol==m_config.symbol_b) return signal.symbol_b_reference_price;
      if(symbol==signal.hunter_symbol) return signal.hunter_reference_price;
      if(symbol==signal.clean_symbol) return signal.clean_reference_price;
      return 0.0;
   }

   double SymbolCurrentExtreme(SCGCFinalSignal &signal,const string symbol)
   {
      if(symbol==m_config.symbol_a) return signal.symbol_a_current_extreme;
      if(symbol==m_config.symbol_b) return signal.symbol_b_current_extreme;
      if(symbol==signal.hunter_symbol) return signal.hunter_current_extreme;
      if(symbol==signal.clean_symbol) return signal.clean_current_extreme;
      return 0.0;
   }

   bool IsHunterChart(SCGCFinalSignal &signal,const string symbol)
   {
      return (ValidSymbolName(signal.hunter_symbol) && symbol==signal.hunter_symbol);
   }

   bool IsCleanChart(SCGCFinalSignal &signal,const string symbol)
   {
      return (ValidSymbolName(signal.clean_symbol) && symbol==signal.clean_symbol);
   }

   bool SymbolVisualDataIsReady(SCGCFinalSignal &signal,const string symbol)
   {
      if(symbol==m_config.symbol_a)
         return signal.symbol_a_visual_data_ready;
      if(symbol==m_config.symbol_b)
         return signal.symbol_b_visual_data_ready;
      return false;
   }

   bool SymbolReferenceIsFrontier(SCGCFinalSignal &signal,const string symbol)
   {
      if(!m_config.enable_extreme_frontier_reference_filter)
         return true;
      if(symbol==m_config.symbol_a)
         return signal.symbol_a_reference_frontier;
      if(symbol==m_config.symbol_b)
         return signal.symbol_b_reference_frontier;
      return false;
   }

   bool ShouldDraw(SCGCFinalSignal &signal)
   {
      if(!m_config.enable_drawing)
         return false;
      if(signal.status==CGC_STATUS_CONFIRMED_TRADEABLE && !m_config.draw_confirmed_tradeable)
         return false;
      if(signal.status==CGC_STATUS_INVALIDATED_DOUBLE_HUNT && !m_config.draw_invalidated_double_hunts)
         return false;
      if(!m_config.draw_on_both_input_symbol_charts && m_config.draw_only_when_chart_is_hunter_symbol && _Symbol!=signal.hunter_symbol)
         return false;
      if(signal.confirmation_time_broker<=0)
         return false;
      return true;
   }

   void ApplyCommonObjectState(const long chart_id,const string name,const string tooltip)
   {
      ObjectSetInteger(chart_id,name,OBJPROP_SELECTABLE,true);
      ObjectSetInteger(chart_id,name,OBJPROP_SELECTED,false);
      ObjectSetInteger(chart_id,name,OBJPROP_BACK,false);
      ObjectSetInteger(chart_id,name,OBJPROP_HIDDEN,false);
      ObjectSetInteger(chart_id,name,OBJPROP_TIMEFRAMES,OBJ_ALL_PERIODS);
      ObjectSetInteger(chart_id,name,OBJPROP_ZORDER,1000);
      ObjectSetString(chart_id,name,OBJPROP_TOOLTIP,tooltip);
   }

   int SafeVisualSpanSeconds()
   {
      ENUM_TIMEFRAMES tf=VisualChartTimeframe();
      int seconds=PeriodSeconds(tf);
      if(seconds<=0)
         seconds=PeriodSeconds((ENUM_TIMEFRAMES)_Period);
      if(seconds<=0)
         seconds=60;
      return MathMax(60,seconds*3);
   }

   void NormalizeVisualSegment(datetime &t1,double &p1,datetime &t2,double &p2)
   {
      if(t1<=0 && t2>0)
         t1=(datetime)(t2-SafeVisualSpanSeconds());
      if(t2<=0 && t1>0)
         t2=(datetime)(t1+SafeVisualSpanSeconds());
      if(t1>0 && t2>0 && t2<=t1)
         t2=(datetime)(t1+SafeVisualSpanSeconds());
   }

   bool DrawTrend(const long chart_id,const string name,const datetime in_t1,const double in_p1,const datetime in_t2,const double in_p2,const color c,const int width,const ECGVVisualLineStyle style,const string tooltip)
   {
      datetime t1=in_t1;
      datetime t2=in_t2;
      double p1=in_p1;
      double p2=in_p2;
      NormalizeVisualSegment(t1,p1,t2,p2);
      if(chart_id<0 || t1<=0 || t2<=0 || p1<=0.0 || p2<=0.0)
         return false;
      ObjectDelete(chart_id,name);
      if(!ObjectCreate(chart_id,name,OBJ_TREND,0,t1,p1,t2,p2))
         return false;
      ObjectSetInteger(chart_id,name,OBJPROP_COLOR,c);
      ObjectSetInteger(chart_id,name,OBJPROP_WIDTH,MathMax(1,width));
      ObjectSetInteger(chart_id,name,OBJPROP_STYLE,StyleFromEnum(style));
      ObjectSetInteger(chart_id,name,OBJPROP_RAY_LEFT,false);
      ObjectSetInteger(chart_id,name,OBJPROP_RAY_RIGHT,false);
      ObjectSetInteger(chart_id,name,OBJPROP_HIDDEN,false);
      ObjectSetInteger(chart_id,name,OBJPROP_TIMEFRAMES,OBJ_ALL_PERIODS);
      ObjectSetInteger(chart_id,name,OBJPROP_ZORDER,1000);
      ApplyCommonObjectState(chart_id,name,tooltip);
      return true;
   }

   bool DrawMainLegWithShadow(const long chart_id,const string name,const datetime t1,const double p1,const datetime t2,const double p2,const color c,const int width,const ECGVVisualLineStyle style,const string tooltip)
   {
      bool shadow=false;
      bool main=false;
      string shadow_name=name+"_shadow";
      shadow=DrawTrend(chart_id,shadow_name,t1,p1,t2,p2,clrBlack,MathMax(width+2,4),CGV_VISUAL_STYLE_SOLID,tooltip+" | shadow");
      main=DrawTrend(chart_id,name,t1,p1,t2,p2,c,MathMax(width,3),style,tooltip);
      return (main || shadow);
   }

   bool DrawVertical(const long chart_id,const string name,const datetime t,const color c,const ECGVVisualLineStyle style,const string tooltip)
   {
      if(chart_id<0 || t<=0)
         return false;
      ObjectDelete(chart_id,name);
      if(!ObjectCreate(chart_id,name,OBJ_VLINE,0,t,0.0))
         return false;
      ObjectSetInteger(chart_id,name,OBJPROP_COLOR,c);
      ObjectSetInteger(chart_id,name,OBJPROP_STYLE,StyleFromEnum(style));
      ObjectSetInteger(chart_id,name,OBJPROP_WIDTH,1);
      ApplyCommonObjectState(chart_id,name,tooltip);
      return true;
   }

   bool DrawMarker(const long chart_id,const string name,const datetime t,const double p,const color c,const int arrow_code,const int width,const string tooltip)
   {
      if(chart_id<0 || t<=0 || p<=0.0)
         return false;
      ObjectDelete(chart_id,name);
      if(!ObjectCreate(chart_id,name,OBJ_ARROW,0,t,p))
         return false;
      ObjectSetInteger(chart_id,name,OBJPROP_COLOR,c);
      ObjectSetInteger(chart_id,name,OBJPROP_ARROWCODE,arrow_code);
      ObjectSetInteger(chart_id,name,OBJPROP_WIDTH,MathMax(1,width));
      ApplyCommonObjectState(chart_id,name,tooltip);
      return true;
   }

   bool DrawText(const long chart_id,const string name,const datetime t,const double p,const string label,const color c,const string tooltip)
   {
      if(m_config.suppress_all_text_objects)
         return false;
      if(chart_id<0 || t<=0 || p<=0.0)
         return false;
      ObjectDelete(chart_id,name);
      if(!ObjectCreate(chart_id,name,OBJ_TEXT,0,t,p))
         return false;
      ObjectSetString(chart_id,name,OBJPROP_TEXT,label);
      ObjectSetInteger(chart_id,name,OBJPROP_COLOR,c);
      ObjectSetInteger(chart_id,name,OBJPROP_FONTSIZE,MathMax(6,m_config.label_font_size));
      ApplyCommonObjectState(chart_id,name,tooltip);
      return true;
   }

   string Tooltip(SCGCFinalSignal &signal,const string visual_part,const string chart_symbol,const datetime origin_time,const double origin_price,const datetime destination_time,const double destination_price)
   {
      return StringFormat("EXP0017 Phase06 Dual Visual | %s | chart_symbol=%s | %s %s | side=%s | CG=%s | hunter=%s | clean=%s | ref #%d | local_data=%s | local_frontier=%s | origin=%s @ %s | destination=%s @ %s | note=%s",
                          visual_part,chart_symbol,StatusText(signal),DirectionText(signal),SideText(signal),signal.group_name,signal.hunter_symbol,signal.clean_symbol,signal.reference_cycle_number,
                          (SymbolVisualDataIsReady(signal,chart_symbol) ? "true" : "false"),
                          (SymbolReferenceIsFrontier(signal,chart_symbol) ? "true" : "false"),
                          TimeToString(origin_time,TIME_DATE|TIME_MINUTES),DoubleToString(origin_price,CGC_PRICE_DIGITS),
                          TimeToString(destination_time,TIME_DATE|TIME_MINUTES),DoubleToString(destination_price,CGC_PRICE_DIGITS),signal.note);
   }

   int DrawSymbolLocalVisualPackage(SCGCFinalSignal &signal,const string chart_symbol)
   {
      if(!ValidSymbolName(chart_symbol))
         return 0;

      // Hotfix010: local rendering requires both complete M1 evidence and a
      // fresh local frontier. Pair-level confirmation alone cannot authorize a
      // Nasdaq companion leg when NDX history is partial or not synchronized.
      if(!SymbolVisualDataIsReady(signal,chart_symbol))
         return 0;
      if(!SymbolReferenceIsFrontier(signal,chart_symbol))
         return 0;

      long chart_id=FindChartForSymbol(chart_symbol);
      if(chart_id<0)
         return 0;

      bool is_hunter=IsHunterChart(signal,chart_symbol);
      bool is_clean=IsCleanChart(signal,chart_symbol);
      bool is_invalidated=(signal.status==CGC_STATUS_INVALIDATED_DOUBLE_HUNT);
      if(signal.status==CGC_STATUS_CONFIRMED_TRADEABLE && !is_hunter && !is_clean)
         return 0;

      double reference_price=SymbolReferencePrice(signal,chart_symbol);
      double current_extreme=SymbolCurrentExtreme(signal,chart_symbol);
      if(reference_price<=0.0 && is_hunter) reference_price=signal.hunter_reference_price;
      if(reference_price<=0.0 && is_clean)  reference_price=signal.clean_reference_price;
      if(current_extreme<=0.0 && is_hunter) current_extreme=signal.hunter_current_extreme;
      if(current_extreme<=0.0 && is_clean)  current_extreme=signal.clean_current_extreme;

      datetime origin_fallback=NyToBroker(signal,signal.reference_cycle_end_ny);
      datetime destination_fallback=signal.confirmation_time_broker;
      datetime origin_time=AnchorTime(signal,m_config.divergence_origin_time_mode,chart_symbol,origin_fallback);
      datetime destination_time=AnchorTime(signal,m_config.divergence_destination_time_mode,chart_symbol,destination_fallback);

      color package_color=SignalColor(signal);
      string role="HUNTER";
      if(is_clean)
      {
         package_color=m_config.clean_comparison_color;
         role="CLEAN";
      }
      if(is_invalidated)
      {
         package_color=m_config.invalidated_color;
         role="DOUBLE_HUNT";
      }

      string base_tooltip=Tooltip(signal,role + " symbol-local divergence leg",chart_symbol,origin_time,reference_price,destination_time,current_extreme);
      string primary_leg_name=Key(signal,chart_symbol,"origin_to_destination_"+role);

      // Hotfix005: historical backfill is processed oldest-to-newest.
      // If this signal id already has its primary visual leg, keep the first visual placement
      // so later bars in the same CG cycle do not drag the drawing forward.
      if(m_config.keep_first_visual_for_same_signal_id && ObjectFind(chart_id,primary_leg_name)>=0)
         return 0;

      int drawn=0;

      if(m_config.draw_divergence_origin_destination_line)
      {
         if(DrawMainLegWithShadow(chart_id,primary_leg_name,origin_time,reference_price,destination_time,current_extreme,package_color,m_config.divergence_line_width,m_config.divergence_line_style,base_tooltip))
            drawn++;
      }

      if(m_config.draw_origin_marker)
      {
         if(DrawMarker(chart_id,Key(signal,chart_symbol,"origin_marker_"+role),origin_time,reference_price,m_config.origin_marker_color,m_config.origin_marker_arrow_code,m_config.origin_marker_width,base_tooltip))
            drawn++;
      }

      if(m_config.draw_destination_marker)
      {
         if(DrawMarker(chart_id,Key(signal,chart_symbol,"destination_marker_"+role),destination_time,current_extreme,m_config.destination_marker_color,m_config.destination_marker_arrow_code,m_config.destination_marker_width,base_tooltip))
            drawn++;
      }

      if(m_config.draw_origin_vertical)
      {
         if(DrawVertical(chart_id,Key(signal,chart_symbol,"origin_vertical_"+role),origin_time,m_config.origin_marker_color,CGV_VISUAL_STYLE_DOT,"EXP0017 origin time for "+role+" leg"))
            drawn++;
      }

      if(m_config.draw_destination_vertical)
      {
         if(DrawVertical(chart_id,Key(signal,chart_symbol,"destination_vertical_"+role),destination_time,m_config.destination_marker_color,CGV_VISUAL_STYLE_SOLID,"EXP0017 destination/extreme time for "+role+" leg"))
            drawn++;
      }

      if(m_config.draw_confirmation_marker)
      {
         if(DrawVertical(chart_id,Key(signal,chart_symbol,"confirmation_close_vertical_"+role),signal.confirmation_time_broker,package_color,CGV_VISUAL_STYLE_DASH,"EXP0017 closed-candle confirmation boundary"))
            drawn++;
      }

      bool draw_reference_guide=(is_hunter && m_config.draw_hunter_reference_guide) || (is_clean && m_config.draw_clean_reference_guide) || is_invalidated;
      if(draw_reference_guide)
      {
         if(DrawTrend(chart_id,Key(signal,chart_symbol,"reference_guide_"+role),origin_time,reference_price,destination_time,reference_price,m_config.guide_color,m_config.guide_line_width,m_config.guide_line_style,"EXP0017 symbol-local reference guide"))
            drawn++;
      }

      if((is_hunter && m_config.draw_hunter_current_extreme_guide) || (is_clean && m_config.draw_clean_comparison_line) || is_invalidated)
      {
         if(DrawTrend(chart_id,Key(signal,chart_symbol,"current_extreme_guide_"+role),origin_time,current_extreme,destination_time,current_extreme,m_config.guide_color,m_config.guide_line_width,m_config.guide_line_style,"EXP0017 symbol-local current-cycle extreme guide"))
            drawn++;
      }

      if(is_clean && m_config.draw_clean_stop_reference_guide && signal.clean_stop_reference_price>0.0)
      {
         if(DrawTrend(chart_id,Key(signal,chart_symbol,"clean_stop_reference_guide"),origin_time,signal.clean_stop_reference_price,destination_time,signal.clean_stop_reference_price,m_config.clean_comparison_color,m_config.guide_line_width,m_config.guide_line_style,"EXP0017 clean stop-reference guide"))
            drawn++;
      }

      if(m_config.draw_reference_cycle_anchor)
      {
         datetime ref_start=NyToBroker(signal,signal.reference_cycle_start_ny);
         datetime ref_end=NyToBroker(signal,signal.reference_cycle_end_ny);
         if(DrawTrend(chart_id,Key(signal,chart_symbol,"reference_cycle_anchor_"+role),ref_start,reference_price,ref_end,reference_price,m_config.guide_color,m_config.guide_line_width,CGV_VISUAL_STYLE_DASHDOT,"EXP0017 full reference-cycle anchor"))
            drawn++;
      }

      if(m_config.draw_text_label)
      {
         double label_price=current_extreme;
         double point=SymbolInfoDouble(chart_symbol,SYMBOL_POINT);
         if(point<=0.0) point=_Point;
         double offset=m_config.label_offset_points*point;
         if(offset<=0.0) offset=20*point;
         if(signal.direction==CGC_DIRECTION_BUY)
            label_price=current_extreme - offset;
         if(signal.direction==CGC_DIRECTION_SELL)
            label_price=current_extreme + offset;
         string label=StringFormat("%s %s %s %s | %s | ref#%d cur#%d",
                                   signal.group_name,StatusText(signal),DirectionText(signal),role,chart_symbol,signal.reference_cycle_number,signal.current_cycle_number);
         if(DrawText(chart_id,Key(signal,chart_symbol,"visual_label_"+role),destination_time,label_price,label,m_config.text_color,base_tooltip))
            drawn++;
      }

      ChartRedraw(chart_id);
      return drawn;
   }

   int DrawSingleChartLegacyPackage(SCGCFinalSignal &signal)
   {
      // Single-chart fallback retained for audit/debug modes. In normal Hotfix003 use, dual-symbol drawing is enabled.
      string symbol=_Symbol;
      if(signal.status==CGC_STATUS_CONFIRMED_TRADEABLE)
      {
         if(symbol!=signal.hunter_symbol && symbol!=signal.clean_symbol)
            symbol=signal.hunter_symbol;
      }
      else
      {
         symbol=_Symbol;
      }
      return DrawSymbolLocalVisualPackage(signal,symbol);
   }

   int CountOwnedObjectsOnChart(const long chart_id)
   {
      if(chart_id<0)
         return 0;

      int count=0;
      int total=ObjectsTotal(chart_id,0,-1);
      for(int i=0;i<total;i++)
      {
         string name=ObjectName(chart_id,i,0,-1);
         if(StringFind(name,CGV_OBJECT_PREFIX)==0)
            count++;
      }
      return count;
   }

   int QueueOwnedObjectDeletePass(const long chart_id)
   {
      if(chart_id<0)
         return 0;

      int queued=0;
      int total=ObjectsTotal(chart_id,0,-1);
      for(int i=total-1;i>=0;i--)
      {
         string name=ObjectName(chart_id,i,0,-1);
         if(StringFind(name,CGV_OBJECT_PREFIX)==0)
         {
            if(ObjectDelete(chart_id,name))
               queued++;
         }
      }
      return queued;
   }

   int ClearObjectsOnChart(const long chart_id)
   {
      if(chart_id<0)
         return 0;

      int initial_count=CountOwnedObjectsOnChart(chart_id);
      if(initial_count<=0)
         return 0;

      // Hotfix011: use the prefix overload as the primary authoritative cleanup.
      // Foreign-chart object commands can otherwise leave orphaned NDX legs.
      ObjectsDeleteAll(chart_id,CGV_OBJECT_PREFIX,-1,-1);
      ChartRedraw(chart_id);
      int remaining=CountOwnedObjectsOnChart(chart_id);

      for(int pass=0;pass<4 && remaining>0;pass++)
      {
         QueueOwnedObjectDeletePass(chart_id);
         ChartRedraw(chart_id);
         remaining=CountOwnedObjectsOnChart(chart_id);
      }

      if(remaining>0)
         Print(StringFormat("EXP0017 Phase06 Hotfix011: %d owned objects remained on chart %s (%s) after authoritative cleanup.",remaining,IntegerToString(chart_id),ChartSymbol(chart_id)));

      return MathMax(0,initial_count-remaining);
   }

   int ClearTextObjectsOnChart(const long chart_id)
   {
      if(chart_id<0)
         return 0;
      int removed=0;
      for(int i=ObjectsTotal(chart_id,0,-1)-1;i>=0;i--)
      {
         string name=ObjectName(chart_id,i,0,-1);
         if(StringFind(name,CGV_OBJECT_PREFIX)==0)
         {
            ENUM_OBJECT type=(ENUM_OBJECT)ObjectGetInteger(chart_id,name,OBJPROP_TYPE);
            bool is_text=(type==OBJ_TEXT || type==OBJ_LABEL);
            bool is_visual_label=(StringFind(name,"visual_label")>=0);
            if(is_text || is_visual_label)
            {
               if(ObjectDelete(chart_id,name))
                  removed++;
            }
         }
      }
      ChartRedraw(chart_id);
      return removed;
   }

   int ClearPhaseTextObjects()
   {
      int removed=0;
      long chart_id=ChartFirst();
      while(chart_id>=0)
      {
         string s=ChartSymbol(chart_id);
         if(!m_config.draw_on_both_input_symbol_charts || s==_Symbol || s==m_config.symbol_a || s==m_config.symbol_b)
            removed+=ClearTextObjectsOnChart(chart_id);
         chart_id=ChartNext(chart_id);
      }
      return removed;
   }

   void ApplyMinimalLinesOnlyVisualMode()
   {
      m_config.enable_drawing=true;
      m_config.draw_on_both_input_symbol_charts=true;
      m_config.open_missing_input_symbol_charts=true;
      m_config.draw_confirmed_tradeable=true;
      // Invalidated double hunts are not divergences in the base doctrine. Keep them optional but off in minimal mode.
      m_config.draw_invalidated_double_hunts=false;
      m_config.draw_divergence_origin_destination_line=true;
      m_config.draw_origin_marker=false;
      m_config.draw_destination_marker=false;
      m_config.draw_origin_vertical=false;
      m_config.draw_destination_vertical=false;
      m_config.draw_confirmation_marker=false;
      m_config.draw_reference_cycle_anchor=false;
      m_config.draw_hunter_reference_guide=false;
      m_config.draw_hunter_current_extreme_guide=false;
      m_config.draw_clean_reference_guide=false;
      m_config.draw_clean_stop_reference_guide=false;
      m_config.draw_clean_comparison_line=false;
      m_config.draw_text_label=false;
      m_config.suppress_all_text_objects=true;
   }

   void ApplyLinesAndMarkersVisualMode()
   {
      m_config.enable_drawing=true;
      m_config.draw_on_both_input_symbol_charts=true;
      m_config.open_missing_input_symbol_charts=true;
      m_config.draw_confirmed_tradeable=true;
      m_config.draw_divergence_origin_destination_line=true;
      m_config.draw_origin_marker=true;
      m_config.draw_destination_marker=true;
      m_config.draw_origin_vertical=false;
      m_config.draw_destination_vertical=false;
      m_config.draw_confirmation_marker=false;
      m_config.draw_reference_cycle_anchor=false;
      m_config.draw_hunter_reference_guide=false;
      m_config.draw_hunter_current_extreme_guide=false;
      m_config.draw_clean_reference_guide=false;
      m_config.draw_clean_stop_reference_guide=false;
      m_config.draw_clean_comparison_line=false;
      m_config.draw_text_label=false;
      m_config.suppress_all_text_objects=true;
   }

   void ApplyStructuralLinesVisualMode()
   {
      m_config.enable_drawing=true;
      m_config.draw_on_both_input_symbol_charts=true;
      m_config.open_missing_input_symbol_charts=true;
      m_config.draw_confirmed_tradeable=true;
      m_config.draw_divergence_origin_destination_line=true;
      m_config.draw_origin_marker=false;
      m_config.draw_destination_marker=false;
      m_config.draw_origin_vertical=true;
      m_config.draw_destination_vertical=true;
      m_config.draw_confirmation_marker=true;
      m_config.draw_reference_cycle_anchor=false;
      m_config.draw_hunter_reference_guide=false;
      m_config.draw_hunter_current_extreme_guide=false;
      m_config.draw_clean_reference_guide=false;
      m_config.draw_clean_stop_reference_guide=false;
      m_config.draw_clean_comparison_line=false;
      m_config.draw_text_label=false;
      m_config.suppress_all_text_objects=true;
   }

   void ApplyFullAuditVisualMode()
   {
      m_config.enable_drawing=true;
      m_config.draw_on_both_input_symbol_charts=true;
      m_config.open_missing_input_symbol_charts=true;
      m_config.draw_confirmed_tradeable=true;
      m_config.draw_invalidated_double_hunts=true;
      m_config.draw_divergence_origin_destination_line=true;
      m_config.draw_origin_marker=true;
      m_config.draw_destination_marker=true;
      m_config.draw_origin_vertical=true;
      m_config.draw_destination_vertical=true;
      m_config.draw_confirmation_marker=true;
      m_config.draw_reference_cycle_anchor=true;
      m_config.draw_hunter_reference_guide=true;
      m_config.draw_hunter_current_extreme_guide=true;
      m_config.draw_clean_reference_guide=true;
      m_config.draw_clean_stop_reference_guide=true;
      m_config.draw_clean_comparison_line=true;
      m_config.draw_text_label=true;
      m_config.suppress_all_text_objects=false;
   }

   void ApplyVisualModePreset()
   {
      if(m_config.visual_mode==CGV_VISUAL_MODE_MINIMAL_LINES_ONLY)
      {
         ApplyMinimalLinesOnlyVisualMode();
         return;
      }
      if(m_config.visual_mode==CGV_VISUAL_MODE_LINES_AND_MARKERS)
      {
         ApplyLinesAndMarkersVisualMode();
         return;
      }
      if(m_config.visual_mode==CGV_VISUAL_MODE_STRUCTURAL_LINES)
      {
         ApplyStructuralLinesVisualMode();
         return;
      }
      if(m_config.visual_mode==CGV_VISUAL_MODE_FULL_AUDIT)
      {
         ApplyFullAuditVisualMode();
         return;
      }
   }

public:
   void Configure(SCGVVisualLedgerConfig &config)
   {
      m_config=config;
      if(m_config.keep_first_visual_for_same_signal_id==false)
      {
         // Explicit false is allowed. This block exists only to make the field visible in the configuration contract.
      }

      // Visual mode is the primary authority. This prevents older saved .set files with
      // InpForceAllVisualObjectsOn=true from overriding the new minimal line-only mode.
      ApplyVisualModePreset();
      if(m_config.force_all_visual_objects_on && m_config.visual_mode==CGV_VISUAL_MODE_FULL_AUDIT)
         ApplyFullAuditVisualMode();

      // Final text-suppression safety. This wins over saved .set files and older visual defaults.
      if(m_config.suppress_all_text_objects)
      {
         m_config.draw_text_label=false;
         if(m_config.delete_text_objects_when_suppressed)
            ClearPhaseTextObjects();
      }
      if(m_config.line_width<1) m_config.line_width=1;
      if(m_config.divergence_line_width<1) m_config.divergence_line_width=m_config.line_width;
      if(m_config.divergence_line_width<3) m_config.divergence_line_width=3;
      if(m_config.guide_line_width<1) m_config.guide_line_width=1;
      if(m_config.origin_marker_width<1) m_config.origin_marker_width=1;
      if(m_config.destination_marker_width<1) m_config.destination_marker_width=1;
      if(m_config.label_font_size<6) m_config.label_font_size=8;
      if(m_config.label_offset_points<=0.0) m_config.label_offset_points=20.0;
   }

   int ClearPhaseObjects()
   {
      int removed=0;
      long chart_id=ChartFirst();
      while(chart_id>=0)
      {
         string s=ChartSymbol(chart_id);
         if(!m_config.draw_on_both_input_symbol_charts || s==_Symbol || s==m_config.symbol_a || s==m_config.symbol_b)
            removed+=ClearObjectsOnChart(chart_id);
         chart_id=ChartNext(chart_id);
      }
      return removed;
   }

   bool DrawSignal(SCGCFinalSignal &signal)
   {
      if(!ShouldDraw(signal))
         return false;

      // In strict pair mode, both local references and both local M1 ranges must
      // be proven before either chart receives a line. This keeps SPX and NDX
      // rendering sets mechanically identical at the signal boundary.
      if(m_config.require_symbol_local_frontier_for_both_symbols)
      {
         if(!signal.symbol_a_visual_data_ready || !signal.symbol_b_visual_data_ready)
            return false;
         if(m_config.enable_extreme_frontier_reference_filter &&
            (!signal.symbol_a_reference_frontier || !signal.symbol_b_reference_frontier))
            return false;
      }

      int drawn=0;
      if(m_config.draw_on_both_input_symbol_charts)
      {
         drawn+=DrawSymbolLocalVisualPackage(signal,m_config.symbol_a);
         if(m_config.symbol_b!=m_config.symbol_a)
            drawn+=DrawSymbolLocalVisualPackage(signal,m_config.symbol_b);
      }
      else
      {
         drawn+=DrawSingleChartLegacyPackage(signal);
      }
      return (drawn>0);
   }
};

#endif
