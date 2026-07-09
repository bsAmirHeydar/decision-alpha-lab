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
      return s;
   }

   string Key(SCGCFinalSignal &signal,const string suffix)
   {
      return CGV_OBJECT_PREFIX + Sanitize(signal.signal_id) + "_" + suffix;
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

   string StatusText(SCGCFinalSignal &signal)
   {
      if(signal.status==CGC_STATUS_CONFIRMED_TRADEABLE) return "CONFIRMED";
      if(signal.status==CGC_STATUS_INVALIDATED_DOUBLE_HUNT) return "INVALIDATED";
      if(signal.status==CGC_STATUS_MISSING_DATA) return "MISSING";
      return "NONE";
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
      if(signal.hunter_reference_price<=0.0 || signal.confirmation_time_broker<=0)
         return false;
      return true;
   }

   void ApplyLineStyle(const string name,const color c)
   {
      ObjectSetInteger(0,name,OBJPROP_COLOR,c);
      ObjectSetInteger(0,name,OBJPROP_WIDTH,MathMax(1,m_config.line_width));
      ObjectSetInteger(0,name,OBJPROP_RAY_RIGHT,false);
      ObjectSetInteger(0,name,OBJPROP_SELECTABLE,true);
      ObjectSetInteger(0,name,OBJPROP_SELECTED,false);
      ObjectSetInteger(0,name,OBJPROP_BACK,false);
   }

public:
   void Configure(SCGVVisualLedgerConfig &config)
   {
      m_config=config;
      if(m_config.line_width<1)
         m_config.line_width=1;
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

      color c=SignalColor(signal);
      datetime reference_anchor_broker=NyToBroker(signal,signal.reference_cycle_end_ny);
      if(reference_anchor_broker<=0)
         reference_anchor_broker=signal.confirmation_time_broker;

      double price=signal.hunter_reference_price;
      string line_name=Key(signal,"line");
      ObjectDelete(0,line_name);
      if(!ObjectCreate(0,line_name,OBJ_TREND,0,reference_anchor_broker,price,signal.confirmation_time_broker,price))
         return false;
      ApplyLineStyle(line_name,c);

      string tooltip=StringFormat("EXP0017 Phase06 | %s %s | CG=%s | hunter=%s | clean=%s | ref #%d | confirm=%s",
                                  StatusText(signal),DirectionText(signal),signal.group_name,signal.hunter_symbol,signal.clean_symbol,
                                  signal.reference_cycle_number,TimeToString(signal.confirmation_time_broker,TIME_DATE|TIME_MINUTES));
      ObjectSetString(0,line_name,OBJPROP_TOOLTIP,tooltip);

      if(m_config.draw_reference_cycle_anchor)
      {
         string ref_name=Key(signal,"ref_anchor");
         ObjectDelete(0,ref_name);
         if(ObjectCreate(0,ref_name,OBJ_VLINE,0,reference_anchor_broker,0.0))
         {
            ObjectSetInteger(0,ref_name,OBJPROP_COLOR,c);
            ObjectSetInteger(0,ref_name,OBJPROP_STYLE,STYLE_DOT);
            ObjectSetInteger(0,ref_name,OBJPROP_WIDTH,1);
            ObjectSetString(0,ref_name,OBJPROP_TOOLTIP,"EXP0017 Phase06 reference-cycle anchor, not exact wick timestamp");
         }
      }

      if(m_config.draw_confirmation_marker)
      {
         string marker_name=Key(signal,"confirm");
         ObjectDelete(0,marker_name);
         if(ObjectCreate(0,marker_name,OBJ_VLINE,0,signal.confirmation_time_broker,0.0))
         {
            ObjectSetInteger(0,marker_name,OBJPROP_COLOR,c);
            ObjectSetInteger(0,marker_name,OBJPROP_STYLE,STYLE_SOLID);
            ObjectSetInteger(0,marker_name,OBJPROP_WIDTH,1);
            ObjectSetString(0,marker_name,OBJPROP_TOOLTIP,"EXP0017 Phase06 closed-candle confirmation boundary");
         }
      }

      if(m_config.draw_text_label)
      {
         string text_name=Key(signal,"label");
         ObjectDelete(0,text_name);
         double label_price=price;
         if(signal.direction==CGC_DIRECTION_BUY)
            label_price=price - 20*_Point;
         if(signal.direction==CGC_DIRECTION_SELL)
            label_price=price + 20*_Point;
         if(ObjectCreate(0,text_name,OBJ_TEXT,0,signal.confirmation_time_broker,label_price))
         {
            string label=StringFormat("%s %s %s | hunter %s | clean %s | ref #%d",
                                      signal.group_name,StatusText(signal),DirectionText(signal),signal.hunter_symbol,signal.clean_symbol,signal.reference_cycle_number);
            ObjectSetString(0,text_name,OBJPROP_TEXT,label);
            ObjectSetInteger(0,text_name,OBJPROP_COLOR,m_config.text_color);
            ObjectSetInteger(0,text_name,OBJPROP_FONTSIZE,8);
            ObjectSetString(0,text_name,OBJPROP_TOOLTIP,tooltip);
         }
      }
      return true;
   }
};

#endif
