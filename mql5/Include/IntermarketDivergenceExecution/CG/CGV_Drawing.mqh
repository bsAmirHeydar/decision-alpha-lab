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
      return s;
   }

   string Key(SCGCFinalSignal &signal,const string suffix)
   {
      return CGV_OBJECT_PREFIX + Sanitize(signal.signal_id) + "_" + suffix;
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

   string AnchorSymbol(SCGCFinalSignal &signal,const ECGVAnchorSymbolMode mode)
   {
      if(mode==CGV_ANCHOR_SYMBOL_CLEAN) return signal.clean_symbol;
      if(mode==CGV_ANCHOR_SYMBOL_CHART) return _Symbol;
      if(mode==CGV_ANCHOR_SYMBOL_A)     return m_config.symbol_a;
      if(mode==CGV_ANCHOR_SYMBOL_B)     return m_config.symbol_b;
      return signal.hunter_symbol;
   }

   double AnchorPrice(SCGCFinalSignal &signal,const ECGVAnchorPriceMode mode)
   {
      if(mode==CGV_ANCHOR_PRICE_HUNTER_CURRENT_EXTREME)
         return signal.hunter_current_extreme;
      if(mode==CGV_ANCHOR_PRICE_CLEAN_REFERENCE)
         return signal.clean_reference_price;
      if(mode==CGV_ANCHOR_PRICE_CLEAN_CURRENT_EXTREME)
         return signal.clean_current_extreme;
      if(mode==CGV_ANCHOR_PRICE_CLEAN_STOP_REFERENCE)
         return signal.clean_stop_reference_price;
      return signal.hunter_reference_price;
   }

   datetime MidTime(const datetime a,const datetime b)
   {
      if(a<=0 || b<=0 || b<a)
         return a;
      return (datetime)(a + (b-a)/2);
   }

   datetime FindExtremeTimeM1(const string symbol,const datetime start_broker,const datetime end_broker,const ECGCSignalSide side,const datetime fallback_time)
   {
      if(!ValidSymbolName(symbol) || start_broker<=0 || end_broker<=0 || end_broker<start_broker)
         return fallback_time;

      MqlRates rates[];
      ArraySetAsSeries(rates,false);
      int copied=CopyRates(symbol,PERIOD_M1,start_broker,end_broker,rates);
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
         return FindExtremeTimeM1(anchor_symbol,ref_start,ref_end,signal.side,fallback_time);
      if(mode==CGV_ANCHOR_TIME_EXACT_CURRENT_EXTREME)
      {
         datetime end_time=signal.confirmation_time_broker;
         if(end_time<=0 || (cur_end>0 && end_time>cur_end))
            end_time=cur_end;
         return FindExtremeTimeM1(anchor_symbol,cur_start,end_time,signal.side,fallback_time);
      }
      return fallback_time;
   }

   bool ShouldDraw(SCGCFinalSignal &signal)
   {
      if(!m_config.enable_drawing)
         return false;
      if(signal.status==CGC_STATUS_CONFIRMED_TRADEABLE && !m_config.draw_confirmed_tradeable)
         return false;
      if(signal.status==CGC_STATUS_INVALIDATED_DOUBLE_HUNT && !m_config.draw_invalidated_double_hunts)
         return false;
      if(m_config.draw_only_when_chart_is_hunter_symbol && _Symbol!=signal.hunter_symbol)
         return false;
      if(signal.confirmation_time_broker<=0)
         return false;
      return true;
   }

   void ApplyCommonObjectState(const string name,const string tooltip)
   {
      ObjectSetInteger(0,name,OBJPROP_SELECTABLE,true);
      ObjectSetInteger(0,name,OBJPROP_SELECTED,false);
      ObjectSetInteger(0,name,OBJPROP_BACK,false);
      ObjectSetString(0,name,OBJPROP_TOOLTIP,tooltip);
   }

   bool DrawTrend(const string name,const datetime t1,const double p1,const datetime t2,const double p2,const color c,const int width,const ECGVVisualLineStyle style,const string tooltip)
   {
      if(t1<=0 || t2<=0 || p1<=0.0 || p2<=0.0)
         return false;
      ObjectDelete(0,name);
      if(!ObjectCreate(0,name,OBJ_TREND,0,t1,p1,t2,p2))
         return false;
      ObjectSetInteger(0,name,OBJPROP_COLOR,c);
      ObjectSetInteger(0,name,OBJPROP_WIDTH,MathMax(1,width));
      ObjectSetInteger(0,name,OBJPROP_STYLE,StyleFromEnum(style));
      ObjectSetInteger(0,name,OBJPROP_RAY_RIGHT,false);
      ApplyCommonObjectState(name,tooltip);
      return true;
   }

   bool DrawVertical(const string name,const datetime t,const color c,const ECGVVisualLineStyle style,const string tooltip)
   {
      if(t<=0)
         return false;
      ObjectDelete(0,name);
      if(!ObjectCreate(0,name,OBJ_VLINE,0,t,0.0))
         return false;
      ObjectSetInteger(0,name,OBJPROP_COLOR,c);
      ObjectSetInteger(0,name,OBJPROP_STYLE,StyleFromEnum(style));
      ObjectSetInteger(0,name,OBJPROP_WIDTH,1);
      ApplyCommonObjectState(name,tooltip);
      return true;
   }

   bool DrawMarker(const string name,const datetime t,const double p,const color c,const int arrow_code,const int width,const string tooltip)
   {
      if(t<=0 || p<=0.0)
         return false;
      ObjectDelete(0,name);
      if(!ObjectCreate(0,name,OBJ_ARROW,0,t,p))
         return false;
      ObjectSetInteger(0,name,OBJPROP_COLOR,c);
      ObjectSetInteger(0,name,OBJPROP_ARROWCODE,arrow_code);
      ObjectSetInteger(0,name,OBJPROP_WIDTH,MathMax(1,width));
      ApplyCommonObjectState(name,tooltip);
      return true;
   }

   bool DrawText(const string name,const datetime t,const double p,const string label,const color c,const string tooltip)
   {
      if(t<=0 || p<=0.0)
         return false;
      ObjectDelete(0,name);
      if(!ObjectCreate(0,name,OBJ_TEXT,0,t,p))
         return false;
      ObjectSetString(0,name,OBJPROP_TEXT,label);
      ObjectSetInteger(0,name,OBJPROP_COLOR,c);
      ObjectSetInteger(0,name,OBJPROP_FONTSIZE,MathMax(6,m_config.label_font_size));
      ApplyCommonObjectState(name,tooltip);
      return true;
   }

   string Tooltip(SCGCFinalSignal &signal,const string visual_part,const datetime origin_time,const double origin_price,const datetime destination_time,const double destination_price)
   {
      return StringFormat("EXP0017 Phase06 Visual Language | %s | %s %s %s | side=%s | CG=%s | hunter=%s | clean=%s | ref #%d | origin=%s @ %s | destination=%s @ %s | note=%s",
                          visual_part,
                          StatusText(signal),DirectionText(signal),signal.status==CGC_STATUS_CONFIRMED_TRADEABLE ? "TRADEABLE_PREVIEW" : "NO_PERMISSION",
                          SideText(signal),signal.group_name,signal.hunter_symbol,signal.clean_symbol,signal.reference_cycle_number,
                          TimeToString(origin_time,TIME_DATE|TIME_MINUTES),DoubleToString(origin_price,CGC_PRICE_DIGITS),
                          TimeToString(destination_time,TIME_DATE|TIME_MINUTES),DoubleToString(destination_price,CGC_PRICE_DIGITS),signal.note);
   }

   int DrawConfirmedVisualLanguage(SCGCFinalSignal &signal)
   {
      int drawn=0;
      color c=SignalColor(signal);
      string origin_symbol=AnchorSymbol(signal,m_config.divergence_origin_symbol_mode);
      string destination_symbol=AnchorSymbol(signal,m_config.divergence_destination_symbol_mode);

      datetime origin_fallback=NyToBroker(signal,signal.reference_cycle_end_ny);
      datetime destination_fallback=signal.confirmation_time_broker;
      datetime origin_time=AnchorTime(signal,m_config.divergence_origin_time_mode,origin_symbol,origin_fallback);
      datetime destination_time=AnchorTime(signal,m_config.divergence_destination_time_mode,destination_symbol,destination_fallback);
      double origin_price=AnchorPrice(signal,m_config.divergence_origin_price_mode);
      double destination_price=AnchorPrice(signal,m_config.divergence_destination_price_mode);

      string base_tooltip=Tooltip(signal,"main divergence origin-to-destination",origin_time,origin_price,destination_time,destination_price);

      if(m_config.draw_divergence_origin_destination_line)
      {
         if(DrawTrend(Key(signal,"divergence_origin_to_destination"),origin_time,origin_price,destination_time,destination_price,c,m_config.divergence_line_width,m_config.divergence_line_style,base_tooltip))
            drawn++;
      }

      if(m_config.draw_origin_marker)
      {
         if(DrawMarker(Key(signal,"origin_marker"),origin_time,origin_price,m_config.origin_marker_color,m_config.origin_marker_arrow_code,m_config.origin_marker_width,base_tooltip))
            drawn++;
      }

      if(m_config.draw_destination_marker)
      {
         if(DrawMarker(Key(signal,"destination_marker"),destination_time,destination_price,m_config.destination_marker_color,m_config.destination_marker_arrow_code,m_config.destination_marker_width,base_tooltip))
            drawn++;
      }

      if(m_config.draw_origin_vertical)
      {
         if(DrawVertical(Key(signal,"origin_vertical"),origin_time,m_config.origin_marker_color,CGV_VISUAL_STYLE_DOT,"EXP0017 divergence origin time"))
            drawn++;
      }

      if(m_config.draw_destination_vertical || m_config.draw_confirmation_marker)
      {
         datetime vertical_time=(m_config.draw_destination_vertical ? destination_time : signal.confirmation_time_broker);
         if(DrawVertical(Key(signal,"destination_or_confirmation_vertical"),vertical_time,m_config.destination_marker_color,CGV_VISUAL_STYLE_SOLID,"EXP0017 divergence destination / confirmation boundary"))
            drawn++;
      }

      if(m_config.draw_hunter_reference_guide)
      {
         if(DrawTrend(Key(signal,"hunter_reference_guide"),origin_time,signal.hunter_reference_price,destination_time,signal.hunter_reference_price,m_config.guide_color,m_config.guide_line_width,m_config.guide_line_style,"EXP0017 hunter reference horizontal guide"))
            drawn++;
      }

      if(m_config.draw_hunter_current_extreme_guide)
      {
         if(DrawTrend(Key(signal,"hunter_current_extreme_guide"),origin_time,signal.hunter_current_extreme,destination_time,signal.hunter_current_extreme,m_config.guide_color,m_config.guide_line_width,m_config.guide_line_style,"EXP0017 hunter current-cycle extreme guide"))
            drawn++;
      }

      if(m_config.draw_clean_reference_guide)
      {
         if(DrawTrend(Key(signal,"clean_reference_guide"),origin_time,signal.clean_reference_price,destination_time,signal.clean_reference_price,m_config.clean_comparison_color,m_config.guide_line_width,m_config.guide_line_style,"EXP0017 clean reference guide; scale is valid only on clean-symbol chart"))
            drawn++;
      }

      if(m_config.draw_clean_stop_reference_guide)
      {
         if(DrawTrend(Key(signal,"clean_stop_reference_guide"),origin_time,signal.clean_stop_reference_price,destination_time,signal.clean_stop_reference_price,m_config.clean_comparison_color,m_config.guide_line_width,m_config.guide_line_style,"EXP0017 clean stop-reference guide; scale is valid only on clean-symbol chart"))
            drawn++;
      }

      if(m_config.draw_clean_comparison_line)
      {
         if(!m_config.draw_clean_comparison_only_when_chart_is_clean_symbol || _Symbol==signal.clean_symbol)
         {
            datetime clean_origin_time=AnchorTime(signal,CGV_ANCHOR_TIME_EXACT_REFERENCE_EXTREME,signal.clean_symbol,origin_fallback);
            datetime clean_destination_time=AnchorTime(signal,CGV_ANCHOR_TIME_EXACT_CURRENT_EXTREME,signal.clean_symbol,destination_fallback);
            if(DrawTrend(Key(signal,"clean_reference_to_current_comparison"),clean_origin_time,signal.clean_reference_price,clean_destination_time,signal.clean_current_extreme,m_config.clean_comparison_color,m_config.guide_line_width,CGV_VISUAL_STYLE_DASH,"EXP0017 clean symbol reference-to-current comparison line; not a trade line"))
               drawn++;
         }
      }

      if(m_config.draw_text_label)
      {
         double label_price=destination_price;
         double offset=m_config.label_offset_points*_Point;
         if(offset<=0.0)
            offset=20*_Point;
         if(signal.direction==CGC_DIRECTION_BUY)
            label_price=destination_price - offset;
         if(signal.direction==CGC_DIRECTION_SELL)
            label_price=destination_price + offset;
         string label=StringFormat("%s %s %s | %s -> %s | H:%s C:%s | R#%d C#%d",
                                   signal.group_name,StatusText(signal),DirectionText(signal),
                                   TimeToString(origin_time,TIME_MINUTES),TimeToString(destination_time,TIME_MINUTES),
                                   signal.hunter_symbol,signal.clean_symbol,signal.reference_cycle_number,signal.current_cycle_number);
         if(DrawText(Key(signal,"visual_label"),destination_time,label_price,label,m_config.text_color,base_tooltip))
            drawn++;
      }

      return drawn;
   }

   int DrawInvalidatedVisualLanguage(SCGCFinalSignal &signal)
   {
      int drawn=0;
      color c=m_config.invalidated_color;
      datetime t=signal.confirmation_time_broker;
      double price=0.0;
      if(signal.hunter_reference_price>0.0)
         price=signal.hunter_reference_price;
      else if(signal.clean_reference_price>0.0)
         price=signal.clean_reference_price;
      else if(signal.clean_stop_reference_price>0.0)
         price=signal.clean_stop_reference_price;

      if(m_config.draw_confirmation_marker)
      {
         if(DrawVertical(Key(signal,"invalidated_confirmation_vertical"),t,c,CGV_VISUAL_STYLE_DASH,"EXP0017 invalidated double-hunt confirmation boundary"))
            drawn++;
      }

      if(m_config.draw_text_label && price>0.0)
      {
         string label=StringFormat("%s INVALIDATED %s | double hunt | ref #%d",signal.group_name,DirectionText(signal),signal.reference_cycle_number);
         if(DrawText(Key(signal,"invalidated_label"),t,price,label,c,"EXP0017 invalidated double-hunt state"))
            drawn++;
      }
      return drawn;
   }

public:
   void Configure(SCGVVisualLedgerConfig &config)
   {
      m_config=config;
      if(m_config.line_width<1)
         m_config.line_width=1;
      if(m_config.divergence_line_width<1)
         m_config.divergence_line_width=m_config.line_width;
      if(m_config.guide_line_width<1)
         m_config.guide_line_width=1;
      if(m_config.origin_marker_width<1)
         m_config.origin_marker_width=1;
      if(m_config.destination_marker_width<1)
         m_config.destination_marker_width=1;
      if(m_config.label_font_size<6)
         m_config.label_font_size=8;
      if(m_config.label_offset_points<=0.0)
         m_config.label_offset_points=20.0;
   }

   int ClearPhaseObjects()
   {
      int removed=0;
      for(int i=ObjectsTotal(0,0,-1)-1;i>=0;i--)
      {
         string name=ObjectName(0,i,0,-1);
         if(StringFind(name,CGV_OBJECT_PREFIX)==0)
         {
            if(ObjectDelete(0,name))
               removed++;
         }
      }
      return removed;
   }

   bool DrawSignal(SCGCFinalSignal &signal)
   {
      if(!ShouldDraw(signal))
         return false;

      int drawn=0;
      if(signal.status==CGC_STATUS_CONFIRMED_TRADEABLE)
         drawn+=DrawConfirmedVisualLanguage(signal);
      else if(signal.status==CGC_STATUS_INVALIDATED_DOUBLE_HUNT)
         drawn+=DrawInvalidatedVisualLanguage(signal);

      return (drawn>0);
   }
};

#endif
